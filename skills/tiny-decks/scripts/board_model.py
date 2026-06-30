#!/usr/bin/env python3
"""
board_model.py — the data-driven monthly board pack.

Reads a monthly data model (JSON; see references/data-schema.md), runs the
single-source compute() engine, and emits a deck spec (the same JSON build.py
consumes). Every KPI, table, chart and donut is derived from ONE set of figures,
so the pack reconciles with itself.

Usage:
    python board_model.py <model.json> <spec.json>      # write the spec
    python board_model.py <model.json> <out.pptx> --pptx # straight to pptx

Reconciliation warnings (e.g. P&L not tying to the trend) print to stderr.
"""
import json
import sys

from compute import compute


def _m(v, dec=1):
    """$000s -> $X.XM display."""
    if v is None:
        return "—"
    neg = v < 0
    s = f"${abs(v)/1000:.{dec}f}M"
    return f"({s})" if neg else s


def _k(v):
    """$000s -> comma thousands (table cells)."""
    if v is None:
        return "—"
    return f"({abs(v):,.0f})" if v < 0 else f"{v:,.0f}"


def _p(v, dec=0, sign=False):
    if v is None:
        return "—"
    return (f"{v:+.{dec}f}%" if sign else f"{v:.{dec}f}%")


def build_spec(model):
    M = compute(model)
    meta = M.get("meta", {})
    cur = meta.get("currency", "$CAD")
    slides = []

    # 1 · COVER
    slides.append({
        "layout": "cover",
        "eyebrow": meta.get("status", "Board Update"),
        "title": "Monthly Board Results",
        "subtitle": f"Consolidated results, P&L by company, portfolio and outlook — {meta.get('period','')}.",
        "period": meta.get("period", ""),
        "entity": meta.get("entity", "Tiny Ltd."),
        "preparedBy": meta.get("preparedBy", "Office of the CFO"),
        "confidential": meta.get("confidential", "Confidential"),
    })

    # 2 & 3 · CONSOLIDATED KPI (pro forma, as reported)
    for key, label in (("proForma", "Pro Forma"), ("asReported", "As Reported")):
        s = M.get("summary", {}).get(key)
        if not s:
            continue
        slides.append({
            "layout": "kpi",
            "eyebrow": f"Consolidated · {label}",
            "title": "Results Update",
            "kpis": [
                {"label": "Revenue", "value": _m(s.get("monthRev")),
                 "delta": s.get("monthRevYoY"), "deltaLabel": "YoY"},
                {"label": "Adj. EBITDA", "value": _m(s.get("monthEbt")),
                 "delta": s.get("monthEbtYoY"), "deltaLabel": "YoY"},
                {"label": "Margin", "value": _p(s.get("monthMargin")),
                 "delta": None, "sub": f"MoM {_p(s.get('monthEbtMoM'),sign=True)}"},
                {"label": f"LTM Revenue", "value": _m(s.get("ltm", {}).get("rev"), 0),
                 "delta": s.get("ltm", {}).get("revYoY"), "deltaLabel": "YoY"},
            ],
            "commentary": s.get("commentary", []),
            "footnote": s.get("basis", ""),
        })

    # 4 · P&L BY COMPANY
    pnl = M.get("pnl", {})
    if pnl.get("companies"):
        rows = []
        for c in pnl["companies"]:
            rows.append([c["name"], _k(c.get("rev")), _k(c.get("gross")),
                         _k(c.get("ebitda")), _p(c.get("margin"))])
        con = pnl.get("consolidated", {})
        rows.append(["Consolidated", _k(con.get("rev")), _k(con.get("gross")),
                     _k(con.get("ebitda")), _p(con.get("margin"))])
        slides.append({
            "layout": "table", "eyebrow": "Detail", "title": "P&L by Company",
            "bandMeta": f"{meta.get('periodShort','')} · {cur} 000s",
            "columns": [{"label": "Company"}, {"label": "Revenue"},
                        {"label": "Gross Profit"}, {"label": "Adj. EBITDA"},
                        {"label": "Margin"}],
            "rows": rows, "totalRows": [len(rows) - 1],
            "note": pnl.get("note", ""),
        })

    # 5 · BY COMPANY — MONTH (revenue)
    bcm = M.get("byCompanyMonth", {})
    if bcm.get("revenue"):
        rows = []
        for r in bcm["revenue"]:
            rows.append([r["name"], _k(r.get("cur")), _k(r.get("priorMo")),
                         _p(r.get("mom"), sign=True), _p(r.get("yoy"), sign=True),
                         _k(r.get("ttm"))])
        tot = bcm.get("revenueTotal", {})
        rows.append(["Consolidated", _k(tot.get("cur")), _k(tot.get("priorMo")),
                     _p(tot.get("mom"), sign=True), _p(tot.get("yoy"), sign=True),
                     _k(tot.get("ttm"))])
        slides.append({
            "layout": "table", "eyebrow": "By Company",
            "title": "Revenue — Month", "bandMeta": f"{cur} 000s",
            "columns": [{"label": "Company"}, {"label": meta.get("periodShort", "Cur")},
                        {"label": meta.get("priorMonth", "Prior Mo")},
                        {"label": "MoM"}, {"label": "YoY"}, {"label": "TTM"}],
            "rows": rows, "totalRows": [len(rows) - 1], "varianceCols": [3, 4],
        })

    # 6 · BY COMPANY — YTD
    ytd = M.get("byCompanyYTD", {})
    if ytd.get("rows"):
        rows = []
        for r in ytd["rows"]:
            rows.append([r["name"], _k(r.get("rev")), _p(r.get("revYoY"), sign=True),
                         _k(r.get("ebitda")), _p(r.get("ebitdaYoY"), sign=True)])
        rows.append(["Consolidated", _k(ytd.get("totalRev")),
                     _p(ytd.get("consolRevYoY"), sign=True),
                     _k(ytd.get("totalEbitda")),
                     _p(ytd.get("consolEbitdaYoY"), sign=True)])
        slides.append({
            "layout": "table", "eyebrow": "By Company",
            "title": "Revenue & Adj. EBITDA — YTD",
            "bandMeta": f"{meta.get('fiscalYTD','YTD')} · {cur} 000s",
            "columns": [{"label": "Company"}, {"label": "Revenue"}, {"label": "YoY"},
                        {"label": "Adj. EBITDA"}, {"label": "YoY"}],
            "rows": rows, "totalRows": [len(rows) - 1], "varianceCols": [2, 4],
            "note": " · ".join(_strip(x) for x in ytd.get("commentary", [])[:1]),
        })

    # 7 · REVENUE TREND
    tr = M.get("trend", {})
    if tr.get("revenue"):
        slides.append({
            "layout": "chart", "eyebrow": "Trend", "title": "Monthly Revenue",
            "chartType": "column",
            "data": {"cats": _months(tr), "values": tr["revenue"], "color": "#2B28F5"},
            "commentary": M.get("revenueTrend", {}).get("commentary", []),
        })

    # 8 · ADJ. EBITDA TREND (combo with margin)
    if tr.get("ebitda"):
        slides.append({
            "layout": "chart", "eyebrow": "Trend", "title": "Adj. EBITDA & Margin",
            "chartType": "combo",
            "data": {"cats": _months(tr), "values": tr["ebitda"],
                     "line": [round(x, 1) for x in tr.get("margin", [])]},
            "commentary": M.get("ebitdaTrend", {}).get("commentary", []),
        })

    # 9 · EBITDA BRIDGE (waterfall)
    br = M.get("bridge", {})
    if br.get("items"):
        slides.append({
            "layout": "chart", "eyebrow": "Attribution",
            "title": "Adj. EBITDA Bridge (YoY)", "chartType": "waterfall",
            "data": {"labels": [i["label"] for i in br["items"]],
                     "deltas": [i["value"] for i in br["items"]],
                     "start": br.get("start", 0), "end": br.get("end", 0)},
            "commentary": br.get("commentary", []),
        })

    # 10 · PORTFOLIO MIX (twin donuts)
    mix = M.get("mix", {})
    if mix.get("revenue"):
        slides.append({
            "layout": "dualchart", "eyebrow": "Composition",
            "title": "Portfolio Mix", "bandMeta": meta.get("period", ""),
            "charts": [
                {"title": "Revenue", "chartType": "doughnut",
                 "data": {"labels": [d["name"] for d in mix["revenue"]],
                          "values": [d["value"] for d in mix["revenue"]],
                          "colors": [d.get("color") for d in mix["revenue"]]}},
                {"title": "Adj. EBITDA", "chartType": "doughnut",
                 "data": {"labels": [d["name"] for d in mix["ebitda"]],
                          "values": [d["value"] for d in mix["ebitda"]],
                          "colors": [d.get("color") for d in mix["ebitda"]]}},
            ],
            "note": mix.get("note", ""),
        })

    # 11 · VALUE-CREATION MATRIX (bubble)
    mx = M.get("matrix", {})
    if mx.get("points"):
        ax = mx.get("axis", {})
        slides.append({
            "layout": "chart", "eyebrow": "Quadrant",
            "title": "Value-Creation Matrix", "chartType": "bubble",
            "data": {"points": mx["points"], "xRange": ax.get("xRange"),
                     "yRange": ax.get("yRange")},
            "commentary": ["Growth (x) vs TTM margin (y); bubble size = TTM revenue."],
        })

    # 12 · FCF
    fcf = M.get("fcf", {})
    if fcf.get("lines"):
        rows, totals = [], []
        for i, ln in enumerate(fcf["lines"]):
            rows.append([ln["label"], _k(ln.get("value"))])
            if ln.get("kind") in ("subtotal", "total"):
                totals.append(i)
        slides.append({
            "layout": "table", "eyebrow": "Cash",
            "title": "Estimated FCF to Shareholders",
            "bandMeta": f"{meta.get('periodShort','')} · {cur} 000s",
            "columns": [{"label": "Line"}, {"label": "Amount"}],
            "rows": rows, "totalRows": totals, "note": fcf.get("note", ""),
        })

    # 13 · TINY FUND
    fund = M.get("fund", {})
    if fund.get("holdings"):
        rows = []
        for hld in fund["holdings"]:
            rows.append([hld["name"], _k(hld.get("rev")), _k(hld.get("ebitda")),
                         _p(hld.get("margin")), _p(hld.get("ownership"))])
        rows.append(["Total (LP basis)", _k(fund.get("totalRev")),
                     _k(fund.get("totalEbitda")), "", ""])
        slides.append({
            "layout": "table", "eyebrow": "Fund",
            "title": "Tiny Fund I",
            "bandMeta": f"{meta.get('fundCurrency','$USD')} 000s",
            "columns": [{"label": "Holding"}, {"label": "Revenue"},
                        {"label": "Adj. EBITDA"}, {"label": "Margin"},
                        {"label": "Ownership"}],
            "rows": rows, "totalRows": [len(rows) - 1],
            "note": " · ".join(_strip(x) for x in fund.get("commentary", [])[:1]),
        })

    # 14 · SUM-OF-THE-PARTS
    sotp = M.get("sotp", {})
    if sotp.get("segments"):
        segs = sotp["segments"]
        slides.append({
            "layout": "chart", "eyebrow": "Valuation",
            "title": "Sum-of-the-Parts (Illustrative)", "chartType": "bar",
            "data": {"cats": [s["name"] for s in segs],
                     "values": [s["ev"] for s in segs],
                     "colors": [s.get("color") for s in segs], "fmt": "#,##0"},
            "commentary": [
                f"<b>Implied EV {_m(sotp.get('evTotal'),0)}</b> across segments (EBITDA × multiple).",
                f"<b>Equity value {_m(sotp.get('equityValue'),0)}</b> after {_m(sotp.get('netDebt'),0)} net debt.",
                f"<b>Attributable to Tiny {_m(sotp.get('tinyEquity'),0)}</b> ({_p(sotp.get('tinyEquityPct'))}); NCI the balance.",
            ],
            "note": sotp.get("note", ""),
        })

    return {"title": f"Tiny — Monthly Board Results — {meta.get('period','')}",
            "slides": slides, "_warnings": M.get("_warnings", [])}


def _months(tr):
    return [_fmt_month(m) for m in tr.get("months", [])]


def _fmt_month(m):
    # "04-25" -> "Apr"
    names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
             "Oct", "Nov", "Dec"]
    try:
        mm = int(str(m).split("-")[0])
        return names[mm - 1]
    except Exception:
        return str(m)


def _strip(s):
    import re
    return re.sub(r"<[^>]+>", "", s or "").replace("&amp;", "&")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    model = json.load(open(sys.argv[1]))
    spec = build_spec(model)
    for w in spec.get("_warnings", []):
        print(f"  [reconcile] {w}", file=sys.stderr)
    if sys.argv[-1] == "--pptx":
        from build import build
        n = build(spec, sys.argv[2])
        print(f"✓ {n} slides -> {sys.argv[2]}")
    else:
        json.dump(spec, open(sys.argv[2], "w"), indent=2)
        print(f"✓ spec ({len(spec['slides'])} slides) -> {sys.argv[2]}")


if __name__ == "__main__":
    main()
