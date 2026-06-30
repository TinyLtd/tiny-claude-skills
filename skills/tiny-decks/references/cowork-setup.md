# Cowork / claude.ai setup & org rollout

How tiny-decks is published org-wide, what environment it runs in, and how
end users use it. (Verified against Anthropic docs, 2026-05.)

## For the Organization Owner (one-time rollout)

Publishing the skill once makes it appear for **every member** with zero per-user
setup. Steps:

1. **Enable the capabilities** (Org settings → Capabilities): turn ON **Code
   execution**, **File creation**, and **Skills**. Skills require code execution
   or they won't appear — and Excel intake is impossible without it.
2. **Upload the skill** (Org settings → **Skills** → **+ Add**): upload the
   `skill/tiny-decks/` folder (zipped). `SKILL.md` is the entry point.
3. It auto-appears for all members under **Customize → Skills**, enabled by
   default. Members can toggle it off individually but never have to install it.
4. **Connect Google Drive org-wide** (Org settings → Connectors) if teams will
   pull models from Drive or save decks back. Native connector is read-only;
   allow connector writes if you want deck save-back.

Notes:
- **Only an Organization Owner** (not Admin/Member) can add org-wide skills.
- **Network mode** (Org settings) governs whether the sandbox can `pip install`.
  tiny-decks needs **no installs** — `python-pptx`, `openpyxl`, `pandas`,
  `pdfplumber`, `matplotlib` are pre-installed — so even the locked-down
  "Disabled" network mode works.
- **Skills don't sync across surfaces.** This folder is the single source of
  truth (in `Folly-Partners/tiny-decks-claude-skill`). To also use it in Claude Code or via
  the API, upload it there separately.

## Execution environment (what the skill can rely on)
- Python 3.11, Linux. Pre-installed: `python-pptx`, `python-docx`, `openpyxl`,
  `xlsxwriter`, `xlrd`, `pandas`, `numpy`, `matplotlib`, `pillow`, `pypdf`,
  `pdfplumber`, `reportlab`.
- Sandbox: ~5 GiB RAM / 5 GiB disk / 1 CPU. Uploaded files land on the sandbox
  filesystem; the skill reads them by path and runs its bundled scripts there.
- Bundled `.py`/`.sh` scripts execute via bash; only their stdout enters context
  (script source doesn't), which keeps the skill cheap to run.

## File limits (end users)
- Up to **20 files per chat**, **30 MB per file**. For larger Excel models, ask
  the user to trim to the relevant tabs or export key tabs as CSV.
- Accepted: `.xlsx .csv .pdf .docx .pptx`, images. **Excel requires Code
  execution ON** (it's read by Python, not text-extracted).

## For end users (layman)
In Cowork, just say: **"Make me a board deck for April"** (or lender / investor /
fundraise / shareholder / M&A / all-hands). Drop in your Excel model, last
period's deck, or a board PDF — or point at a Google Drive file. The skill infers
the deck, asks a couple of quick questions, and returns an editable PowerPoint
and/or a Google Slides link. No setup.

## Updating the skill over time
Everything is editable by asking Claude in plain English — no manual coding:
- "Add a cash-flow slide to the lender deck" → edits `assets/templates/deck-lender.json`.
- "Change the brand blue" → `references/brand.md` + `BLUE`/`CHART_PALETTE` in
  `scripts/theme.py`.
- "Add a QBR deck type" → new `assets/templates/deck-qbr.json` + a menu line here.
- "The P&L table has too many columns" → `scripts/board_model.py` / `slides.py`.
After any change, re-render an example to verify, commit to
`Folly-Partners/tiny-decks-claude-skill`, and re-upload the folder in Org settings → Skills.
