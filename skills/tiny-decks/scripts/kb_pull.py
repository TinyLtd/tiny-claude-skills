#!/usr/bin/env python3
"""
kb_pull.py — playbook for populating a board model from the tiny-kb MCP.

A plain Python script can't call an MCP. So this script's job is to PRINT a
clear, copy-pasteable playbook telling the agent (Claude) exactly which
`tiny-kb` namespaces to search, what to query, and which model.json fields each
result fills. The agent runs the `mcp__tiny-kb__search` calls itself, then
writes the figures into the model (raw inputs only — `compute.py` derives the
rest).

USAGE
-----
    python kb_pull.py [--period "April 2026"]

  --period   Reporting period to weave into the example queries (default
             "the latest reporting month"). Use the month/quarter you're
             building the deck for.

If the tiny-kb MCP is NOT connected in this environment, fall back to the
paste/CSV intake (`scripts/csv_intake.py`) or read the monthly reporting PDF and
fill the model by hand.
"""
import argparse
import sys

NAMESPACES = [
    "finance/reporting", "finance/consolidation", "finance/forecasts",
    "finance/board", "finance/debt", "finance/tax",
]

# section -> (description, [(namespace, example query, model fields filled)])
SECTIONS = [
    ("trend", "Monthly revenue & Adj. EBITDA time series (12-13 months).", [
        ("finance/reporting",
         'monthly consolidated revenue and adjusted EBITDA by month {period_ltm}',
         "trend.months[], trend.revenue[], trend.ebitda[]"),
        ("finance/consolidation",
         'consolidated EBITDA trend trailing twelve months ending {period}',
         "trend.ebitda[] (cross-check vs reporting)"),
    ]),
    ("summary", "Consolidated KPI cards — pro forma and as reported.", [
        ("finance/reporting",
         'consolidated revenue and adjusted EBITDA {period} vs prior month and prior year',
         "summary.proForma.monthRevPriorMo / monthRevPriorYr / "
         "monthEbtPriorMo / monthEbtPriorYr"),
        ("finance/consolidation",
         'YTD and LTM revenue and EBITDA {period} pro forma vs as reported, prior year',
         "summary.{proForma,asReported}.ytd.* and .ltm.*"),
    ]),
    ("pnl", "P&L by company for the month (rev, COS, staff, prof, S&M, subs, EBITDA).", [
        ("finance/reporting",
         'P&L by operating company {period} revenue cost of sales staff '
         'professional fees sales marketing subscriptions adjusted EBITDA',
         "pnl.companies[].{rev,cos,staff,prof,sm,subs,ebitda}"),
    ]),
    ("byCompanyMonth", "Per-company month revenue & EBITDA with prior-mo / prior-yr / TTM.", [
        ("finance/reporting",
         'revenue by company {period} current month prior month prior year trailing twelve months',
         "byCompanyMonth.revenue[].{cur,priorMo,priorYr,ttm}"),
        ("finance/reporting",
         'adjusted EBITDA by company {period} current vs prior month vs prior year TTM',
         "byCompanyMonth.ebitda[].{cur,priorMo,priorYr,ttm}"),
    ]),
    ("byCompanyYTD", "Per-company YTD revenue & EBITDA with YoY, plus budget.", [
        ("finance/reporting",
         'year to date revenue and adjusted EBITDA by company {period} vs prior year',
         "byCompanyYTD.rows[].{rev,revYoY,ebitda,ebitdaYoY}"),
        ("finance/forecasts",
         'YTD budget revenue and EBITDA {period} consolidated',
         "byCompanyYTD.budgetRev, byCompanyYTD.budgetEbitda"),
    ]),
    ("fcf", "Free cash flow to shareholders walk.", [
        ("finance/reporting",
         'free cash flow to shareholders {period} EBITDA less NCI cash taxes '
         'interest severance other adjustments',
         "fcf.lines[].{label,value,kind}"),
        ("finance/debt",
         'interest payments on debt {period} semi-annual schedule',
         "fcf.lines[] interest line value"),
    ]),
    ("fund", "Tiny Fund I holdings — revenue, EBITDA, ownership %.", [
        ("finance/reporting",
         'Tiny Fund holdings {period} revenue EBITDA ownership percentage',
         "fund.holdings[].{rev,ebitda,ownership}"),
        ("finance/consolidation",
         'Tiny LP interest in the fund {period}',
         "fund.tinyLPInterest"),
    ]),
    ("sotp", "Sum-of-the-parts valuation inputs (TTM EBITDA, multiples, net debt).", [
        ("finance/board",
         'sum of the parts valuation by segment TTM EBITDA exit multiples {period}',
         "sotp.segments[].{ttmEbitda,multiple}"),
        ("finance/debt",
         'net debt total outstanding {period}',
         "sotp.netDebt, sotp.tinyEquityPct"),
    ]),
]

NOTES = [
    "Enter RAW figures only — do NOT compute margins, totals, deltas, mix, "
    "bridge endpoints, EV or the equity split. compute.py derives all of those.",
    "All currency figures are in $000s (thousands), matching demo-model.json.",
    "Commentary bullets are the human's voice — write them fresh per period in "
    "the <b>lead-in.</b> detail checkmark style; don't lift them verbatim from KB.",
    "Cross-check: P&L-by-company revenue should tie to the current-month trend "
    "value (board_model.py prints a reconciliation warning if it doesn't).",
    "Cite source doc (filename + period) for each figure you pull, so the deck "
    "is auditable.",
]


def build_playbook(period_label, ltm_label):
    out = []
    out.append("=" * 72)
    out.append(f"  TINY-KB → board model.json PLAYBOOK   (period: {period_label})")
    out.append("=" * 72)
    out.append("")
    out.append("Run each search below with the tiny-kb MCP tool:")
    out.append('    mcp__tiny-kb__search(query=..., namespace=..., top_k=8)')
    out.append("then write the returned figures into model.json (raw inputs only).")
    out.append("")
    out.append(f"Available namespaces: {', '.join(NAMESPACES)}")
    out.append("")

    for i, (key, desc, queries) in enumerate(SECTIONS, 1):
        out.append("-" * 72)
        out.append(f"{i}. {key}")
        out.append(f"   {desc}")
        for ns, q, fields in queries:
            qf = q.format(period=period_label, period_ltm=ltm_label)
            out.append("")
            out.append(f"   namespace : {ns}")
            out.append(f"   query     : \"{qf}\"")
            out.append(f"   fills     : {fields}")
        out.append("")

    out.append("=" * 72)
    out.append("  NOTES")
    out.append("=" * 72)
    for n in NOTES:
        out.append(f"  • {n}")
    out.append("")
    out.append("  Fallback: if the tiny-kb MCP is NOT connected, use")
    out.append("  scripts/csv_intake.py (paste/CSV) or read the monthly reporting")
    out.append("  PDF and fill the model by hand.")
    out.append("")
    return "\n".join(out)


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Print the tiny-kb → board model playbook.")
    p.add_argument("--period", default="the latest reporting month",
                   help='Reporting period, e.g. "April 2026".')
    args = p.parse_args(argv)

    period = args.period
    ltm = (f"ending {period}" if period != "the latest reporting month"
           else "(trailing 12 months)")
    print(build_playbook(period, ltm))
    return 0


if __name__ == "__main__":
    sys.exit(main())
