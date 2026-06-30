# Board-pack data model

This is the schema for the monthly board pack — the JSON you fill in and feed to
`board_model.py`, which runs `compute.py` and renders the 14-slide pack. See
`assets/demo-model.json` for a worked example and `assets/blank-model.json` for
an empty one to fill.

**Two rules that make the pack reconcile:**

1. **Enter every figure once, in `$000s`** (thousands). `5,545` means $5.545M.
   Negatives take a minus sign (`-822`). Percentages you enter (YoY/budget) are
   whole numbers (`17.0` = 17%).
2. **Never enter an AUTO field.** Margins, %-of-revenue, totals, MoM/YoY deltas,
   the consolidated row, mix donuts, bridge endpoints, fund prorations, FCF
   subtotals, and EV/equity are all derived by `compute.py`. Hand-editing them
   only creates drift. Fix the input and rebuild.

**Reconciliation check:** the P&L (`pnl.companies`) revenue must tie to the
current (last) month of `trend.revenue`. If it doesn't, `compute.py` prints a
`[reconcile]` warning to stderr. Relay it and fix the input — don't paper over it.

Build:
```
python scripts/board_model.py model.json out.pptx --pptx
```

---

## `meta` — deck framing

All strings. No computed fields.

| field | what to enter |
|---|---|
| `period` | "April 2026" — reporting month, long form |
| `periodShort` | "Apr-26" — short label for table bands |
| `priorMonth` | "Mar-26" — prior-month column header |
| `priorYear` | "Apr-25" — prior-year label |
| `fiscalYTD` | "YTD 2026" |
| `currency` | "$" (or "$CAD" / "$USD") — operating currency |
| `fundCurrency` | "$US" — fund table currency |
| `preparedBy` | "Office of the CFO" |
| `entity` | company name on the cover |
| `status` | cover eyebrow, e.g. "Board Update" |
| `confidential` | cover confidentiality stamp |

## `trend` — 13-month revenue & EBITDA

13 months, oldest → newest. The **last entry is the current reporting month** and
seeds the consolidated KPI cards and the bridge end-point.

| field | enter / AUTO |
|---|---|
| `months` | enter — 13 labels as `MM-YY` |
| `revenue` | enter — 13 values, `$000s` |
| `ebitda` | enter — 13 values, `$000s` |
| `margin` | AUTO — per-month EBITDA/revenue % |
| `revAvg`, `ebitdaAvg` | AUTO — 13-month averages |
| `revCurrent`, `ebitdaCurrent`, `marginCurrent` | AUTO — last month |

## `summary` — consolidated KPI cards

Two parallel views: `proForma` (organic) and `asReported` (all entities owned).
Same shape for both. The current-month revenue/EBITDA come from `trend`'s last
entry — you only enter the comparatives.

| field | enter / AUTO |
|---|---|
| `basis` | enter — one-line description (shown as footnote) |
| `monthRevPriorMo`, `monthRevPriorYr` | enter — prior-month / prior-year revenue |
| `monthEbtPriorMo`, `monthEbtPriorYr` | enter — prior-month / prior-year EBITDA |
| `ytd.rev`, `ytd.revPriorYr`, `ytd.ebitda`, `ytd.ebitdaPriorYr` | enter — YTD totals + prior year |
| `ltm.*` | enter — same four fields, last-twelve-months |
| `commentary` | enter — checkmark bullets (`<b>lead.</b> detail`) |
| `monthRev`, `monthEbt`, `monthMargin` | AUTO — from `trend` current month |
| `monthRevMoM/YoY`, `monthEbtMoM/YoY` | AUTO — deltas vs the priors above |
| `ytd.revYoY/ebitdaYoY/margin`, `ltm.*` | AUTO — YoY % and margin |

## `pnl` — P&L by company (current month)

One row per operating company plus a **Head Office** row. All cost lines in
`$000s`. This table must tie to `trend` current-month revenue.

| field | enter / AUTO |
|---|---|
| `name`, `short`, `color` | enter — display name, short label, hex (chart color) |
| `rev`, `cos`, `staff`, `prof`, `sm`, `subs`, `ebitda` | enter — revenue, cost of sales, staff, professional, sales & marketing, subscriptions, Adj. EBITDA |
| `note` | enter — caption under the table |
| `gross` | AUTO — `rev − cos` per company |
| `margin` | AUTO — EBITDA/revenue % per company |
| `consolidated` | AUTO — column summing every line + its gross/margin |

## `byCompanyMonth` — current vs prior, by company

Two series: `revenue` and `ebitda`. Each row is one company.

| field | enter / AUTO |
|---|---|
| `name`, `color` | enter |
| `cur`, `priorMo`, `priorYr`, `ttm` | enter — current / prior-month / prior-year / trailing-twelve, `$000s` |
| `spark` | enter — 6-point sparkline series |
| `mom`, `yoy` | AUTO — deltas vs priorMo / priorYr |
| `revenueTotal`, `ebitdaTotal` | AUTO — consolidated row (sums + its own MoM/YoY) |

## `byCompanyYTD` — year-to-date, by company

| field | enter / AUTO |
|---|---|
| `rows[].name`, `color` | enter |
| `rows[].rev`, `ebitda` | enter — YTD totals, `$000s` |
| `rows[].revYoY`, `ebitdaYoY` | enter — YoY % (or `null` if no prior-year base) |
| `rows[].spark` | enter — 6-point sparkline |
| `consolRevYoY`, `consolEbitdaYoY` | enter — consolidated YoY % |
| `budgetRev`, `budgetEbitda` | enter — YTD budget, `$000s` |
| `commentary` | enter — checkmark bullets |
| `totalRev`, `totalEbitda` | AUTO — sums of the rows |
| `revVsBudget`, `ebitdaVsBudget` | AUTO — actual vs budget % |

## `revenueTrend` / `ebitdaTrend` — chart commentary

Each: `commentary` — enter the bullets shown beside the monthly revenue chart and
the Adj. EBITDA & margin combo chart. `<b>..</b>` bold supported. No data here —
the chart series come from `trend`.

## `bridge` — YoY Adj. EBITDA waterfall

| field | enter / AUTO |
|---|---|
| `items[].label`, `value` | enter — one driver per item; `value` is the YoY `$000s` contribution (negative = drag) |
| `commentary` | enter — checkmark bullets |
| `start` | AUTO — prior-year month EBITDA (`summary.proForma.monthEbtPriorYr`) |
| `end` | AUTO — current-month EBITDA (`trend` last) |
| `sumItems` | AUTO — sum of the drivers |

The drivers should sum to roughly `end − start`; if not, you're missing one.

## `mix` — portfolio donuts

| field | enter / AUTO |
|---|---|
| `note` | enter — caption under the twin donuts |
| `revenue`, `ebitda` | AUTO — donut data built from `pnl.companies` (EBITDA donut shows positive contributors only; head office / negatives excluded) |

## `matrix` — value-creation bubble chart

All entered (this view is standalone).

| field | enter |
|---|---|
| `points[].label`, `color` | name + hex |
| `points[].x` | revenue growth %, e.g. `-18.0` |
| `points[].y` | TTM margin %, e.g. `29.6` |
| `points[].size` | TTM revenue, `$000s` (bubble size) |
| `axis.xRange`, `axis.yRange` | `[lo, hi]` plot bounds |

## `fcf` — free-cash-flow roll-up

Ordered lines. `kind:"line"` rows you enter; `kind:"subtotal"` and `kind:"total"`
rows are running roll-ups — leave their `value` off.

| field | enter / AUTO |
|---|---|
| `lines[].label` | enter |
| `lines[].kind` | enter — `line` / `subtotal` / `total` |
| `lines[].value` (on `line` rows) | enter — `$000s`, negatives with a minus |
| `lines[].strong`, `muted` | enter — optional styling flags |
| `lines[].value` (on subtotal/total) | AUTO — running sum to that point |
| `commentary`, `note` | enter |

## `fund` — Tiny Fund holdings

| field | enter / AUTO |
|---|---|
| `holdings[].name`, `color` | enter |
| `holdings[].rev`, `ebitda` | enter — `$000s` |
| `holdings[].ownership` | enter — % the entity owns of the holding |
| `tinyLPInterest` | enter — Tiny's LP % of the fund |
| `commentary` | enter |
| `holdings[].margin` | AUTO — EBITDA/revenue % |
| `holdings[].attribRev`, `attribEbitda` | AUTO — figure × ownership |
| `totalRev`, `totalEbitda`, `attribRev`, `attribEbitda` | AUTO — fund totals |
| `tinyLPRev`, `tinyLPEbitda` | AUTO — attributable × LP interest |

## `sotp` — sum-of-the-parts valuation

| field | enter / AUTO |
|---|---|
| `segments[].name`, `color` | enter |
| `segments[].ttmEbitda` | enter — `$000s` |
| `segments[].multiple` | enter — EV/EBITDA multiple (placeholder; mark "illustrative") |
| `netDebt` | enter — `$000s` |
| `tinyEquityPct` | enter — Tiny's % of equity value |
| `note` | enter |
| `segments[].ev` | AUTO — `ttmEbitda × multiple` |
| `evTotal`, `equityValue` | AUTO — Σ EV, then less net debt |
| `tinyEquity`, `nciEquity` | AUTO — equity split by `tinyEquityPct` |
