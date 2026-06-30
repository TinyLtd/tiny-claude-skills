# Intake & data-mapping playbook

Read this when ingesting user files. Contents:
1. Source priority
2. Excel intake (xlsx_intake.py → classified blocks)
3. PDF / Word / prior decks
4. Google Drive
5. tiny-kb (supporting only)
6. Mapping classified blocks → the board model
7. Period, units & sign conventions
8. Inferring the deck type
9. Gap handling — infer first, then ask
10. Reconciliation

---

## 1. Source priority
Source of truth, in order: **uploaded files → connected Google Drive → what the
user types → tiny-kb**. tiny-kb is a vector store and not always accurate; use it
for color/context only and flag any KB-sourced figure "verify." Never let the KB
override a number that appears in an uploaded file.

## 2. Excel intake
Run `python scripts/xlsx_intake.py <file.xlsx> [more.xlsx ...] [--out blocks.json]`.
It opens each workbook with cached values, finds every table across all sheets
(named tables first, else blank-gap block scanning), resolves merged cells, and
classifies each block with a confidence score. It does NOT map to the deck model
— that's your job.

Read the printed summary (and `blocks.json` for detail). Each block carries:
`sheet, range, rows, cols, classification, confidence, headers, sample`.
Classifications: `pnl`, `trend`, `by_company`, `fund`, `balance_sheet`, `fcf`,
`captable`/`ownership`, `kpi`, `unknown`.

- **High confidence (≳0.7) + obvious mapping** → map it (section 6) and proceed.
- **Low confidence or `unknown`** → do NOT guess. Confirm with the user (section
  9) which slide that block belongs to, or whether to drop it.
- **"no cached values" warning** → the file was never saved by Excel, so values
  are blank. Ask the user to open it in Excel and re-save, or paste the numbers.

If `python-pptx`/`openpyxl` import-fails, you're not in the standard sandbox —
they're pre-installed in Cowork/claude.ai (Code execution must be ON for Excel).

## 3. PDF / Word / prior decks
Claude reads PDFs and Word natively (PDFs multimodally — it sees charts/tables).
Read the uploaded file directly, extract the figures and the existing commentary,
and map into the model. A prior deck (PDF/PPTX) is the best guide to the user's
preferred structure and tone — match it. For dense scanned tables, `pdfplumber`
is available as a fallback.

## 4. Google Drive
If the user references a Drive file (or has Drive connected), fetch the named
sheet/doc through the Drive connector, then handle its content like an uploaded
spreadsheet (Excel path) or PDF. Drive is read-only by default; to save the
finished deck back to Drive the org must allow connector writes.

## 5. tiny-kb (supporting only)
`scripts/kb_pull.py` prints which namespaces/queries map to which model sections.
Use ONLY to enrich narrative/context (entity names, prior-period story) or to
sanity-check, never as the numeric source. Tag every KB-derived value "verify"
in your summary to the user.

## 6. Mapping classified blocks → the board model
Target schema: `references/data-schema.md`. Typical mappings:

| Extractor block | Board-model section |
|---|---|
| `trend` (periods × revenue/ebitda) | `trend.months/revenue/ebitda` |
| `pnl` (companies × rev/cogs/staff/.../ebitda) | `pnl.companies[]` |
| `by_company` (company × cur/prior/ttm) | `byCompanyMonth.revenue/ebitda` or `byCompanyYTD.rows` |
| `fund` (holdings × rev/ebitda/ownership) | `fund.holdings[]` |
| `fcf`/`cashflow` (line items) | `fcf.lines[]` |
| `balance_sheet` | a `kpi`/`table` slide (audience decks) |
| `captable`/`ownership` | `sotp.tinyEquityPct` / an ownership donut |
| `kpi` (a few big numbers) | `summary` KPIs or a `statgrid` |

Only raw inputs are entered — margins, %, totals, deltas, mix, bridge endpoints,
EV and the equity split are all auto-computed by `compute.py`. Don't enter them.

For an **audience deck** (lender/investor/etc.), you usually don't fill the full
board model — you take the matching `assets/templates/deck-*.json` and overwrite
its display values (already-formatted strings like `"$19.1M"`) with the user's.

## 7. Period, units & sign conventions
- Board model money is in **$000s** (enter `19076` for $19.1M). Audience-deck
  values are display strings.
- Negatives use a minus sign internally; `(1,268)` in a source means `-1268`.
- Detect the reporting period from the file (column headers like `Apr-26`, a
  "Month" label, the filename) before asking.
- Map period labels `MM-YY` for `trend.months`; set `meta.period`, `periodShort`,
  `priorMonth`, `priorYear`, `fiscalYTD`, `currency`.

## 8. Inferring the deck type
Infer from the strongest signal available, in this order:
1. **The user said so** ("make a lender deck") → use it.
2. **A prior deck was uploaded** → match its type and structure.
3. **The Excel block mix:**
   - trend + pnl + by_company + fcf + fund → **monthly board pack**.
   - leverage/coverage/covenant/debt/maturity terms → **lender review**.
   - NAV/returns/ownership/thesis terms → **investor update**.
   - raise/round/use-of-proceeds terms → **fundraising pitch**.
   - add-backs/normalized EBITDA/quality-of-earnings → **M&A data-room**.
   - annual/quarterly + balance sheet + outlook → **shareholder review**.
   - vs-plan/wins/scoreboard, internal tone → **exec/all-hands**.
4. **Still ambiguous** → default to the **board pack** if board-pack blocks are
   present, else ask. Always show your inferred pick in the confirmation.

## 9. Gap handling — infer first, then ask
Fill what you can from the files. Then ask (one AskUserQuestion call) only for:
genuine gaps (period, output format, currency, watermark), low-confidence block
mappings, and a one-tap confirm of the inferred deck type. If a required model
field is missing and unknowable, use a clearly-marked placeholder and flag it on
the slide rather than blocking. Never ask for something the files already answer.

## 10. Reconciliation
`board_model.py` prints reconciliation warnings (e.g. "P&L revenue ≠ current-month
trend"). Always relay them to the user — they catch fat-finger errors. If a
warning fires, show the two figures and ask which is right before finalizing.
