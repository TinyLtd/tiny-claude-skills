#!/usr/bin/env python3
"""
csv_intake.py — turn a filled board-pack spreadsheet into a board model JSON.

Parses `assets/board-template-BLANK.csv` (or a copy a finance analyst filled in
Excel/Google Sheets and pasted/exported). Handles comma- OR tab-separated
input, quoted fields with embedded commas, parenthesised negatives, thousands
separators, and `%` signs. Only RAW INPUTS are read — margins, totals, %,
deltas, mix, bridge endpoints, EV etc. are auto-computed downstream by
compute.py, so they are never in this file.

Usage:
    python csv_intake.py <filled.csv> <out_model.json> [--base <model.json>]

  --base   deep-merge the parsed sections over an existing model (so a partial
           paste only updates the sections present).

The parser is forgiving: anything it can't read is skipped with a warning to
stderr; it always emits valid JSON. Section layout mirrors the template's
`=== SECTION ===` headers exactly.
"""
import csv
import io
import json
import re
import sys


# ---- low-level helpers ----------------------------------------------------
def _num(s):
    """'1,234' -> 1234 ; '(252)' -> -252 ; '27%' -> 27 ; '' -> None."""
    if s is None:
        return None
    t = str(s).strip().replace(",", "").replace("$", "").replace("%", "")
    if t == "" or t in ("-", "—"):
        return None
    neg = False
    if t.startswith("(") and t.endswith(")"):
        neg = True
        t = t[1:-1]
    try:
        v = float(t)
    except ValueError:
        return None
    if v == int(v):
        v = int(v)
    return -v if neg else v


def _spark(s):
    if not s:
        return []
    return [(_num(x) or 0) for x in str(s).replace("|", ";").split(";") if x.strip() != ""]


def _is_header(cell, *needles):
    c = (cell or "").strip().lower()
    return any(n in c for n in needles)


def _read_rows(path):
    """Read a CSV/TSV file into a list of row-lists. Auto-detect delimiter."""
    raw = open(path, encoding="utf-8-sig").read()
    first = next((ln for ln in raw.splitlines() if ln.strip()), "")
    delim = "\t" if ("\t" in first and first.count("\t") >= first.count(",")) else ","
    return list(csv.reader(io.StringIO(raw), delimiter=delim))


def _section_name(cell):
    """'=== MONTHLY TREND (13 months...) ===' -> 'monthly trend'."""
    c = (cell or "").strip()
    if not c.startswith("==="):
        return None
    c = c.strip("=").strip()
    c = re.sub(r"\s*\(.*?\)\s*", " ", c)  # drop only the (parenthetical) qualifier
    return c.strip().lower()


# ---- section helpers ------------------------------------------------------
def _kv(rows):
    """Field,Value rows -> dict (skips the 'Field,Value' header row)."""
    out = {}
    for r in rows:
        if len(r) < 2:
            continue
        k = (r[0] or "").strip()
        if not k or _is_header(k, "field"):
            continue
        out[k] = r[1]
    return out


def _commentary(kv):
    items = []
    for i in range(1, 9):
        v = (kv.get(f"commentary_{i}", "") or "").strip()
        if v:
            items.append(v)
    return items


def _bc_month(body):
    out = []
    for r in body:
        c0 = (r[0] or "").strip()
        if _is_header(c0, "company") or not c0:
            continue
        if len(r) >= 6:
            out.append({"name": c0, "color": (r[1] or "#2B28F5").strip(),
                        "cur": _num(r[2]) or 0, "priorMo": _num(r[3]) or 0,
                        "priorYr": _num(r[4]) or 0, "ttm": _num(r[5]) or 0,
                        "spark": _spark(r[6] if len(r) > 6 else "")})
    return out


# ---- main parse -----------------------------------------------------------
def parse(rows, model, warn):
    sections, cur = [], None
    for r in rows:
        if not r or all((c or "").strip() == "" for c in r):
            continue
        name = _section_name(r[0])
        if name is not None:
            cur = (name, [])
            sections.append(cur)
        elif cur is not None:
            cur[1].append(r)
        # rows before the first section header (the intro line) are ignored
    for name, body in sections:
        try:
            _dispatch(name, body, model, warn)
        except Exception as e:
            warn(f"section '{name}' failed: {e}")


def _dispatch(name, body, model, warn):
    if "period" in name and "label" in name:
        kv = _kv(body)
        model.setdefault("meta", {}).update({k: v for k, v in kv.items() if (v or "") != ""})

    elif "monthly trend" in name:
        months, rev, ebt = [], [], []
        for r in body:
            if len(r) < 3 or _is_header(r[0], "month"):
                continue
            if not (r[0] or "").strip():
                continue
            months.append((r[0] or "").strip())
            rev.append(_num(r[1]) or 0)
            ebt.append(_num(r[2]) or 0)
        if months:
            model["trend"] = {"months": months, "revenue": rev, "ebitda": ebt}

    elif "pro forma" in name or "as reported" in name:
        kv = _kv(body)
        key = "proForma" if "pro forma" in name else "asReported"
        s = {"basis": kv.get("basis", "")}
        for f in ("monthRevPriorMo", "monthRevPriorYr", "monthEbtPriorMo", "monthEbtPriorYr"):
            if f in kv:
                s[f] = _num(kv[f])
        s["ytd"] = {"rev": _num(kv.get("ytd_rev")), "revPriorYr": _num(kv.get("ytd_revPriorYr")),
                    "ebitda": _num(kv.get("ytd_ebitda")), "ebitdaPriorYr": _num(kv.get("ytd_ebitdaPriorYr"))}
        s["ltm"] = {"rev": _num(kv.get("ltm_rev")), "revPriorYr": _num(kv.get("ltm_revPriorYr")),
                    "ebitda": _num(kv.get("ltm_ebitda")), "ebitdaPriorYr": _num(kv.get("ltm_ebitdaPriorYr"))}
        c = _commentary(kv)
        if c:
            s["commentary"] = c
        model.setdefault("summary", {})[key] = s

    elif name.startswith("p&l"):
        comps, extra, mode = {}, {}, "main"
        for r in body:
            c0 = (r[0] or "").strip()
            if _is_header(c0, "company") and _is_header(r[1] if len(r) > 1 else "", "short"):
                mode = "main"; continue
            if _is_header(c0, "p&l extra") or (_is_header(c0, "company") and _is_header(r[1] if len(r) > 1 else "", "subs")):
                mode = "extra"; continue
            if not c0:
                continue
            if mode == "main" and len(r) >= 8:
                comps[c0] = {"name": c0, "short": (r[1] or c0).strip(), "color": (r[2] or "#2B28F5").strip(),
                             "rev": _num(r[3]) or 0, "cos": _num(r[4]) or 0, "staff": _num(r[5]) or 0,
                             "prof": _num(r[6]) or 0, "sm": _num(r[7]) or 0}
            elif mode == "extra" and len(r) >= 3:
                extra[c0] = {"subs": _num(r[1]) or 0, "ebitda": _num(r[2]) or 0}
        for nm, e in extra.items():
            if nm in comps:
                comps[nm].update(e)
        if comps:
            for c in comps.values():
                c.setdefault("subs", 0); c.setdefault("ebitda", 0)
            model.setdefault("pnl", {})["companies"] = list(comps.values())

    elif "by company" in name and "month" in name and "revenue" in name:
        model.setdefault("byCompanyMonth", {})["revenue"] = _bc_month(body)
    elif "by company" in name and "month" in name and "ebitda" in name:
        model.setdefault("byCompanyMonth", {})["ebitda"] = _bc_month(body)

    elif "by company" in name and "ytd" in name:
        rows_out, scalars, mode = [], {}, "rows"
        for r in body:
            c0 = (r[0] or "").strip()
            if _is_header(c0, "ytd scalars"):
                mode = "scalars"; continue
            if _is_header(c0, "company") or _is_header(c0, "field"):
                continue
            if not c0:
                continue
            if mode == "rows" and len(r) >= 6:
                rows_out.append({"name": c0, "color": (r[1] or "#2B28F5").strip(),
                                 "rev": _num(r[2]) or 0, "revYoY": _num(r[3]),
                                 "ebitda": _num(r[4]) or 0, "ebitdaYoY": _num(r[5]),
                                 "spark": _spark(r[6] if len(r) > 6 else "")})
            else:
                scalars[c0] = r[1] if len(r) > 1 else ""
        y = model.setdefault("byCompanyYTD", {})
        if rows_out:
            y["rows"] = rows_out
        for f in ("consolRevYoY", "consolEbitdaYoY", "budgetRev", "budgetEbitda"):
            if f in scalars:
                y[f] = _num(scalars[f])
        c = _commentary(scalars)
        if c:
            y["commentary"] = c

    elif "revenue trend commentary" in name:
        c = _commentary(_kv(body))
        if c:
            model.setdefault("revenueTrend", {})["commentary"] = c
    elif "ebitda trend commentary" in name:
        c = _commentary(_kv(body))
        if c:
            model.setdefault("ebitdaTrend", {})["commentary"] = c

    elif "ebitda bridge" in name:
        items, kv = [], {}
        for r in body:
            c0 = (r[0] or "").strip()
            if _is_header(c0, "driver label") or _is_header(c0, "bridge commentary"):
                continue
            if c0.startswith("commentary_"):
                kv[c0] = r[1] if len(r) > 1 else ""
            elif c0 and len(r) >= 2 and _num(r[1]) is not None:
                items.append({"label": c0, "value": _num(r[1])})
        b = model.setdefault("bridge", {})
        if items:
            b["items"] = items
        c = _commentary(kv)
        if c:
            b["commentary"] = c

    elif "portfolio mix" in name:
        kv = _kv(body)
        if kv.get("note"):
            model.setdefault("mix", {})["note"] = kv["note"]

    elif "value-creation matrix" in name or "value creation matrix" in name:
        pts, axis = [], {}
        for r in body:
            c0 = (r[0] or "").strip()
            if _is_header(c0, "company") or _is_header(c0, "axis"):
                continue
            if c0.lower().startswith("xrange"):
                axis["xRange"] = _spark(r[1]) if len(r) > 1 else None
            elif c0.lower().startswith("yrange"):
                axis["yRange"] = _spark(r[1]) if len(r) > 1 else None
            elif c0 and len(r) >= 5:
                pts.append({"label": c0, "color": (r[1] or "#2B28F5").strip(),
                            "x": _num(r[2]) or 0, "y": _num(r[3]) or 0, "size": _num(r[4]) or 1})
        m = model.setdefault("matrix", {})
        if pts:
            m["points"] = pts
        axis = {k: v for k, v in axis.items() if v}
        if axis:
            m["axis"] = axis

    elif name.startswith("fcf"):
        lines, kv = [], {}
        for r in body:
            c0 = (r[0] or "").strip()
            if _is_header(c0, "line") and _is_header(r[2] if len(r) > 2 else "", "kind"):
                continue
            if _is_header(c0, "fcf commentary"):
                continue
            if c0.startswith("commentary_") or c0 == "note":
                kv[c0] = r[1] if len(r) > 1 else ""
            elif c0 and len(r) >= 3:
                kind = (r[2] or "line").strip()
                ln = {"label": c0, "kind": kind}
                if kind == "line":
                    ln["value"] = _num(r[1]) or 0
                lines.append(ln)
        f = model.setdefault("fcf", {})
        if lines:
            f["lines"] = lines
        c = _commentary(kv)
        if c:
            f["commentary"] = c
        if kv.get("note"):
            f["note"] = kv["note"]

    elif "fund holdings" in name:
        holds, scalars, mode = [], {}, "rows"
        for r in body:
            c0 = (r[0] or "").strip()
            if _is_header(c0, "fund scalars"):
                mode = "scalars"; continue
            if _is_header(c0, "holding") or _is_header(c0, "field"):
                continue
            if not c0:
                continue
            if mode == "rows" and len(r) >= 5:
                holds.append({"name": c0, "color": (r[1] or "#2B28F5").strip(),
                              "rev": _num(r[2]) or 0, "ebitda": _num(r[3]) or 0,
                              "ownership": _num(r[4]) or 0})
            else:
                scalars[c0] = r[1] if len(r) > 1 else ""
        fd = model.setdefault("fund", {})
        if holds:
            fd["holdings"] = holds
        if "tinyLPInterest" in scalars:
            fd["tinyLPInterest"] = _num(scalars["tinyLPInterest"])
        c = _commentary(scalars)
        if c:
            fd["commentary"] = c

    elif "sum-of-the-parts" in name or "sum of the parts" in name:
        segs, scalars, mode = [], {}, "rows"
        for r in body:
            c0 = (r[0] or "").strip()
            if _is_header(c0, "sotp scalars"):
                mode = "scalars"; continue
            if _is_header(c0, "segment") or _is_header(c0, "field"):
                continue
            if not c0:
                continue
            if mode == "rows" and len(r) >= 4:
                segs.append({"name": c0, "color": (r[1] or "#1A1980").strip(),
                             "ttmEbitda": _num(r[2]) or 0, "multiple": _num(r[3]) or 0})
            else:
                scalars[c0] = r[1] if len(r) > 1 else ""
        st = model.setdefault("sotp", {})
        if segs:
            st["segments"] = segs
        for f in ("netDebt", "tinyEquityPct"):
            if f in scalars:
                st[f] = _num(scalars[f])
        if scalars.get("note"):
            st["note"] = scalars["note"]

    else:
        warn(f"unknown section '{name}' skipped")


def _merge(base, overlay):
    for k, v in overlay.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            _merge(base[k], v)
        else:
            base[k] = v
    return base


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    csv_path, out_path = sys.argv[1], sys.argv[2]
    base = None
    if "--base" in sys.argv:
        base = json.load(open(sys.argv[sys.argv.index("--base") + 1]))

    warnings = []
    rows = _read_rows(csv_path)
    parsed = {}
    parse(rows, parsed, warnings.append)
    model = _merge(base, parsed) if base else parsed
    json.dump(model, open(out_path, "w"), indent=2)

    if warnings:
        print(f"[csv_intake] {len(warnings)} note(s) (non-fatal):", file=sys.stderr)
        for w in warnings[:12]:
            print(f"  - {w}", file=sys.stderr)
    sec = [k for k in ("meta", "trend", "summary", "pnl", "byCompanyMonth",
                       "byCompanyYTD", "bridge", "matrix", "fcf", "fund", "sotp")
           if k in model]
    print(f"✓ parsed sections: {', '.join(sec)} -> {out_path}")


if __name__ == "__main__":
    main()
