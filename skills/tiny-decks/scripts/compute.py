"""
Board-model math — the single-source-of-truth engine.

Takes the raw monthly data model (see references/data-schema.md) and derives
everything: margins, %-of-revenue, consolidated totals, MoM/YoY deltas,
portfolio mix, the EBITDA bridge endpoints, fund prorations, enterprise value
and the equity split. Enter each figure ONCE in the model; compute() makes the
KPIs, tables, charts and donuts reconcile so the deck can never disagree with
itself.
"""
from copy import deepcopy


def _pct_change(cur, prior):
    if prior in (None, 0) or cur is None:
        return None
    return (cur - prior) / abs(prior) * 100.0


def _margin(ebitda, rev):
    if not rev:
        return None
    return ebitda / rev * 100.0


def compute(model):
    """Return a deep-resolved copy of the model with all derived fields added."""
    m = deepcopy(model)
    warnings = []

    # ---- Trend: margins + trailing averages ----
    tr = m.get("trend", {})
    rev = tr.get("revenue", [])
    ebt = tr.get("ebitda", [])
    if rev and ebt and len(rev) == len(ebt):
        tr["margin"] = [(_margin(e, r) or 0) for e, r in zip(ebt, rev)]
        tr["revAvg"] = sum(rev) / len(rev)
        tr["ebitdaAvg"] = sum(ebt) / len(ebt)
        tr["revCurrent"] = rev[-1]
        tr["ebitdaCurrent"] = ebt[-1]
        tr["marginCurrent"] = tr["margin"][-1]

    # ---- Summary KPI cards (proForma / asReported) ----
    for key in ("proForma", "asReported"):
        s = m.get("summary", {}).get(key)
        if not s:
            continue
        cur_rev = tr.get("revCurrent")
        cur_ebt = tr.get("ebitdaCurrent")
        s["monthRev"] = cur_rev
        s["monthEbt"] = cur_ebt
        s["monthMargin"] = _margin(cur_ebt, cur_rev)
        s["monthRevMoM"] = _pct_change(cur_rev, s.get("monthRevPriorMo"))
        s["monthRevYoY"] = _pct_change(cur_rev, s.get("monthRevPriorYr"))
        s["monthEbtMoM"] = _pct_change(cur_ebt, s.get("monthEbtPriorMo"))
        s["monthEbtYoY"] = _pct_change(cur_ebt, s.get("monthEbtPriorYr"))
        for span in ("ytd", "ltm"):
            d = s.get(span)
            if d:
                d["revYoY"] = _pct_change(d.get("rev"), d.get("revPriorYr"))
                d["ebitdaYoY"] = _pct_change(d.get("ebitda"), d.get("ebitdaPriorYr"))
                d["margin"] = _margin(d.get("ebitda"), d.get("rev"))

    # ---- P&L by company: gross profit, consolidated col, %-of-rev, margins ----
    pnl = m.get("pnl", {})
    comps = pnl.get("companies", [])
    if comps:
        keys = ["rev", "cos", "staff", "prof", "sm", "subs", "ebitda"]
        consol = {k: sum(c.get(k, 0) or 0 for c in comps) for k in keys}
        for c in comps:
            c["gross"] = (c.get("rev", 0) or 0) - (c.get("cos", 0) or 0)
            c["margin"] = _margin(c.get("ebitda", 0), c.get("rev", 0))
        consol["gross"] = consol["rev"] - consol["cos"]
        consol["margin"] = _margin(consol["ebitda"], consol["rev"])
        pnl["consolidated"] = consol
        # reconcile vs trend
        if tr.get("revCurrent") and abs(consol["rev"] - tr["revCurrent"]) > 1:
            warnings.append(
                f"P&L revenue ({consol['rev']:,}) != current-month trend "
                f"({tr['revCurrent']:,})."
            )

    # ---- By company (month): MoM/YoY, consolidated totals ----
    bcm = m.get("byCompanyMonth", {})
    for series in ("revenue", "ebitda"):
        rows = bcm.get(series, [])
        for r in rows:
            r["mom"] = _pct_change(r.get("cur"), r.get("priorMo"))
            r["yoy"] = _pct_change(r.get("cur"), r.get("priorYr"))
        if rows:
            tot = {k: sum(r.get(k, 0) or 0 for r in rows)
                   for k in ("cur", "priorMo", "priorYr", "ttm")}
            tot["mom"] = _pct_change(tot["cur"], tot["priorMo"])
            tot["yoy"] = _pct_change(tot["cur"], tot["priorYr"])
            bcm[series + "Total"] = tot

    # ---- By company (YTD): consolidated sums + vs-budget ----
    ytd = m.get("byCompanyYTD", {})
    rows = ytd.get("rows", [])
    if rows:
        ytd["totalRev"] = sum(r.get("rev", 0) or 0 for r in rows)
        ytd["totalEbitda"] = sum(r.get("ebitda", 0) or 0 for r in rows)
        if ytd.get("budgetRev"):
            ytd["revVsBudget"] = _pct_change(ytd["totalRev"], ytd["budgetRev"])
        if ytd.get("budgetEbitda"):
            ytd["ebitdaVsBudget"] = _pct_change(ytd["totalEbitda"], ytd["budgetEbitda"])

    # ---- Portfolio mix (from P&L) ----
    if comps:
        rev_mix = [{"name": c["name"], "color": c.get("color"),
                    "value": c.get("rev", 0) or 0} for c in comps]
        # EBITDA mix: positive contributors only (exclude head office / negatives)
        ebt_mix = [{"name": c["name"], "color": c.get("color"),
                    "value": c.get("ebitda", 0) or 0}
                   for c in comps if (c.get("ebitda", 0) or 0) > 0]
        m.setdefault("mix", {})
        m["mix"]["revenue"] = sorted(rev_mix, key=lambda d: -d["value"])
        m["mix"]["ebitda"] = sorted(ebt_mix, key=lambda d: -d["value"])

    # ---- EBITDA bridge endpoints ----
    br = m.get("bridge", {})
    if br.get("items"):
        s = m.get("summary", {}).get("proForma", {})
        br["start"] = s.get("monthEbtPriorYr")  # prior-year month
        br["end"] = tr.get("ebitdaCurrent")
        br["sumItems"] = sum(i.get("value", 0) or 0 for i in br["items"])

    # ---- Fund: margins, LP totals, prorations ----
    fund = m.get("fund", {})
    holds = fund.get("holdings", [])
    if holds:
        for h in holds:
            h["margin"] = _margin(h.get("ebitda", 0), h.get("rev", 0))
            own = (h.get("ownership", 0) or 0) / 100.0
            h["attribRev"] = (h.get("rev", 0) or 0) * own
            h["attribEbitda"] = (h.get("ebitda", 0) or 0) * own
        fund["totalRev"] = sum(h.get("rev", 0) or 0 for h in holds)
        fund["totalEbitda"] = sum(h.get("ebitda", 0) or 0 for h in holds)
        fund["attribRev"] = sum(h["attribRev"] for h in holds)
        fund["attribEbitda"] = sum(h["attribEbitda"] for h in holds)
        lp = (fund.get("tinyLPInterest", 0) or 0) / 100.0
        fund["tinyLPRev"] = fund["attribRev"] * lp
        fund["tinyLPEbitda"] = fund["attribEbitda"] * lp

    # ---- FCF: subtotal / total roll-ups ----
    fcf = m.get("fcf", {})
    lines = fcf.get("lines", [])
    if lines:
        running = 0
        for ln in lines:
            kind = ln.get("kind", "line")
            if kind in ("subtotal", "total"):
                ln["value"] = running
            else:
                running += ln.get("value", 0) or 0

    # ---- Sum-of-the-parts: implied EV, equity, ownership split ----
    sotp = m.get("sotp", {})
    segs = sotp.get("segments", [])
    if segs:
        for sg in segs:
            sg["ev"] = (sg.get("ttmEbitda", 0) or 0) * (sg.get("multiple", 0) or 0)
        sotp["evTotal"] = sum(sg["ev"] for sg in segs)
        sotp["equityValue"] = sotp["evTotal"] - (sotp.get("netDebt", 0) or 0)
        pct = (sotp.get("tinyEquityPct", 0) or 0) / 100.0
        sotp["tinyEquity"] = sotp["equityValue"] * pct
        sotp["nciEquity"] = sotp["equityValue"] * (1 - pct)

    m["_warnings"] = warnings
    return m


if __name__ == "__main__":
    import json
    import sys
    data = json.load(open(sys.argv[1]))
    out = compute(data)
    print(json.dumps(out.get("_warnings", []), indent=2))
    print("Computed OK. Keys:", list(out.keys()))
