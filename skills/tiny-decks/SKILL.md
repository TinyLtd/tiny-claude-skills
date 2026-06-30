---
name: tiny-decks
description: >-
  Builds polished, on-brand Tiny presentation decks as editable PowerPoint
  (.pptx) and Google Slides. Use when someone wants to make, build, draft,
  update, or export a finance or corporate deck — a board pack, board slides,
  monthly/quarterly results, a lender or banking review, an investor or LP
  update, a fundraising pitch, a shareholder review, an M&A or data-room
  overview, or an exec/all-hands. Also use when they upload an Excel model,
  a spreadsheet, a prior deck, or a board PDF and want it turned into slides,
  or say "turn these numbers into a presentation." Accepts Excel (.xlsx), CSV,
  PDF, Word and Google Drive files, infers the right deck, and asks a few quick
  questions to confirm.
---

# Tiny Decks

Turn a finance team's numbers into a polished, on-brand Tiny deck — editable
PowerPoint or Google Slides — in minutes. Drop in whatever you have (an Excel
model, last quarter's deck, a board PDF, a few notes), and the skill figures out
what kind of deck you need, maps your numbers onto it, asks a couple of quick
questions to fill gaps, renders it, then **reviews the draft from the target
audience's point of view** — surfacing what a board member / investor / lender
would also want to see and repositioning it to land — before final delivery.

House style: electric royal-blue (`#2B28F5`), the heavy Hanken Grotesk grotesque,
the lowercase `tiny` wordmark, giant metric callouts, blue-checkmark commentary,
and a blue→indigo→violet→azure chart palette.

## When to use
Any request to build / update / draft / export a corporate or finance deck
(board, lender, investor, fundraise, shareholder, M&A, all-hands), OR when the
user uploads a spreadsheet / model / prior deck / board PDF and wants slides.

## Workflow — follow in order

### 1. Gather the inputs first
Ask the user to drop in **everything relevant at once** (Cowork accepts up to 20
files, 30 MB each): the Excel model or spreadsheet, last period's deck, the
monthly board PDF, any commentary/notes, and a logo if they have one. Accepted:
`.xlsx .csv .pdf .docx .pptx` and images, plus anything in their connected
**Google Drive**. If they gave nothing, ask for the one file that matters most
(usually the Excel model) — or offer to start from the synthetic demo.

### 2. Read the inputs (source-of-truth order)
1. **Excel / spreadsheets** → run `python scripts/xlsx_intake.py <file.xlsx ...>`.
   It extracts every table across all sheets, resolves merged cells, and
   classifies each block (pnl / trend / by_company / fund / balance_sheet /
   fcf / captable / kpi / unknown) with a confidence score. Read its summary.
2. **PDF / Word / prior decks** → read them directly (Claude reads PDFs and docs
   natively); pull the figures and commentary.
3. **Google Drive** → fetch the named file/sheet through the Drive connector,
   then treat it like an uploaded spreadsheet.
4. **tiny-kb** → SUPPORTING CONTEXT ONLY. It's a vector store and not always
   accurate, so never use it as the source of truth for hard numbers. Use it to
   fill background/color (entity names, prior-period narrative) and ALWAYS flag
   KB-sourced figures "verify." `scripts/kb_pull.py` documents the queries.

The uploaded files are the source of truth. The data-model schema you're mapping
into is `references/data-schema.md`. The full intake + mapping playbook (how to
turn extracted blocks into the model, period detection, units, gap handling) is
in **`references/intake.md`** — read it when ingesting files.

### 3. Present a PLAN and wait for approval (do not build yet)
From the files + anything the user said, **infer the most likely deck type and
the block→slide mapping yourself** — then show a short **build plan and wait for
the user's go-ahead before building.** The plan is a quick, skimmable outline:

- **Deck type** (your inferred pick, with a note if alternates are plausible).
- **Slide outline** — the slides you'll produce, in order.
- **Data mapping** — which uploaded block/sheet feeds which slide.
- **Gaps & assumptions** — anything missing, any placeholder you'll mark
  "illustrative", any low-confidence block, and any KB-sourced figure ("verify").
- **Options** — currency, Confidential watermark (default ON), Drive folder.

Use **AskUserQuestion** for the few genuine decisions, each answerable in <30s:
confirm deck type, fill a missing period, resolve an ambiguous block. **Ask the
output format as TWO separate questions, in order:**
1. **"PowerPoint, Google Slides, or both?"** (the editable deliverable.)
2. **then "Generate a PDF too?"** — Yes / No. (PDF is an add-on, never bundled by
   default; ask it as its own follow-up.)

Then ask plainly: "Approve this plan, or adjust?" **Build only after approval.**
If the user says "just build it," use sensible defaults (both editable formats,
no PDF unless asked) and skip ahead.

### 4. Build
- **Board pack (data-driven, auto-reconciling):**
  `python scripts/board_model.py model.json out.pptx --pptx` — runs the
  single-source `compute()` (margins, %, totals, deltas, mix, bridge, EV,
  equity) and prints reconciliation warnings (e.g. P&L not tying to the trend)
  to stderr — relay them.
- **Audience decks:** start from `assets/templates/deck-<type>.json`, replace its
  content with the user's, then `python scripts/build.py spec.json out.pptx`.
- **Custom / "something else":** author a spec from `references/deck-spec.md` and
  build it. Use the existing layout vocabulary; don't invent layouts.

Save outputs to a visible folder (e.g. `~/Desktop/`), not a dotfolder.

### 5. Verify it renders
Render and actually look: `soffice --headless --convert-to pdf out.pptx --outdir
/tmp && pdftoppm -png -r 70 /tmp/out.pdf /tmp/chk`, then read a few pages. Check
nothing overflows, KPI numbers don't wrap, charts populated, variance colors
right, on-brand. Fix and re-render. (In Cowork, render to confirm; if LibreOffice
isn't available, sanity-check the spec instead.)

### 6. Audience review & enrich (every time — and show your work)
Put on the hat of whoever the deck is FOR — a board member, a lender's credit
committee, a prospective investor/LP, an acquirer's deal team, employees — and
review the draft critically AS THEM: **"If I were [the audience], what would I
expect to see, what would I push back on, and what's missing?"** Typical gaps by
audience:
- **Board:** cash runway, variance vs budget, risks & mitigations, prior asks /
  follow-ups, KPI trends, decisions needed.
- **Lender:** covenant headroom, liquidity, maturity wall, DSCR, a downside case.
- **Investor / LP:** growth durability, retention/cohorts, unit economics, the
  returns/NAV bridge, capital allocation, comparables.
- **Acquirer (M&A):** quality of earnings & add-backs, customer concentration,
  churn, normalized margins, what's in/out of the deal.
- **Fundraise:** use of proceeds, milestones to the next round, multiples, team.
- **All-hands:** performance vs plan, wins, the honest challenges, the ask.

Then, transparently:
1. **Name the gaps** to the user in plain language — "A board member would also
   expect X, Y, Z; here's what I'd add and why."
2. **Ask with AskUserQuestion** which to add (multi-select), AND request any
   materials or answers you need to add them well (a figure, a file, a one-line
   answer). **Never fabricate numbers** — if you don't have it, ask, or mark a
   clearly-labelled placeholder.
3. **Think through positioning for this audience** — what leads, what's
   emphasized vs de-emphasized, slide order, framing — so the additions land the
   way that audience actually reads a deck. Say how you're repositioning and why.
4. **Revise** (add/reorder/reframe slides), then re-run step 5 to verify.

Tell the user what you reviewed as the audience, what you added, and how you
repositioned. Skip only if the user says "ship it as-is."

### 7. Deliver — exactly the formats they chose
Run `deliver.sh` with flags matching the two format answers:
`bash scripts/deliver.sh out.pptx "Deck Title" [--slides] [--pdf] [--drive-folder <id|name>]`
- PowerPoint chosen → the `.pptx` is the deliverable (always produced).
- Google Slides chosen → add `--slides` (native Slides link; Hanken renders right).
- "Both" → the `.pptx` plus `--slides`.
- PDF = yes → add `--pdf`.
- `--drive-folder` saves copies to Drive.
Give the user the path(s) and the Slides link for whatever was produced. Each
step degrades gracefully if a tool is missing.

## House rules
- **Editable, native objects** — tables, KPIs and charts are real PPTX/Slides
  objects the user can retype. Never flatten to images.
- **One source of truth for the board pack** — enter each figure once in the
  model; never hand-edit a derived number, fix the input and rebuild.
- **Uploaded files > Drive > what the user types > tiny-kb.** KB figures are
  always flagged "verify."
- **Synthetic/illustrative data is clearly flagged.** The shipped demo uses
  fictional companies (Northwind Holdings: Acme, Initech, Umbrella, Globex,
  Hooli, Stark; Fund: Brewster, Pixelle, Verde, Cinephile, Petworks). Replace
  with the user's real numbers; mark placeholders (multiples, net debt,
  covenants) "illustrative."
- **Commentary is the human's voice** — make bullets easy to edit; use the
  `<b>lead-in.</b> detail` checkmark style.

## Files
- `scripts/` — engine: `theme.py`, `compute.py`, `charts.py`, `slides.py`,
  `build.py` (spec→pptx), `board_model.py` (data→board pack); intake:
  `xlsx_intake.py` (Excel→classified blocks), `csv_intake.py` (filled template→
  model), `kb_pull.py` (tiny-kb playbook); delivery: `to_slides.sh`.
- `references/intake.md` — file-intake + data-mapping playbook (read when
  ingesting). `references/deck-spec.md` — slide/chart layout vocabulary (read for
  custom decks). `references/data-schema.md` — the board model. `references/brand.md`
  — house style. `references/cowork-setup.md` — org rollout + environment.
- `assets/` — `demo-model.json` (synthetic board data), `blank-model.json`,
  `templates/deck-*.json` (one per audience deck), `board-template-BLANK.csv`.

(Rendered sample `.pptx` for each deck type live in the repo's `examples/`, not
in the skill bundle — regenerate any time with the build scripts.)

## Requirements
Runs in any environment with Python 3 + `python-pptx`. In the Claude Cowork /
claude.ai sandbox, `python-pptx`, `openpyxl`, `pandas`, `pdfplumber` and
`matplotlib` are **pre-installed — do not pip install**. Excel intake requires
**Code execution** enabled (it's how .xlsx is read at all). `gog` (or the Drive
connector) is needed only for the Google Slides path. See
`references/cowork-setup.md`.
