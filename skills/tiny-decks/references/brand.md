# Tiny house style

The look that keeps every deck on-brand. The canonical implementation is
`scripts/theme.py` — these are the design tokens, and everything downstream
(`slides.py`, `charts.py`) composes from them so the style is identical across
the whole library. Change the brand here and in `theme.py`, not slide by slide.

## Palette

Core tokens (`theme.py`):

| token | hex | use |
|---|---|---|
| `BLUE` | `#2B28F5` | signature electric royal-blue — hero fills, rails, headers, primary chart series |
| `INK` | `#0E0E14` | near-black — headlines, body, bold lead-ins |
| `MUTED` | `#5C5C6A` | gray — labels, secondary text, commentary detail |
| `LINE` | `#E5E5EE` | hairline dividers and borders |
| `TINT` | `#F4F4FB` | faint lavender — section/total-row tint |

**Chart palette** (blue → indigo → violet → azure) — used automatically when a
chart omits its own colors:

```
#2B28F5  #1A1980  #7A5CF5  #2E8FE0  #C44DDB  #5BB0E8  #8E7BFF  #BFC0E6
```

The pale lavender `#BFC0E6` is the conventional color for drags, NCI, and head
office.

**Variance colors — TABLES ONLY, never in charts:**

| token | hex | use |
|---|---|---|
| `POS` | `#1A9E5C` | green — favorable delta in table text |
| `NEG` | `#D64545` | red — unfavorable delta in table text |

Charts stay in the blue→violet family; green/red is reserved for variance numbers
in tables. `goodUp:false` flips which direction is favorable (costs, leverage).

## Typography

- **Hanken Grotesk** throughout (`FONT` in `theme.py`) — a Google Font, so it
  renders natively in Google Slides. PowerPoint falls back to Arial (`FONT_FALL`)
  if it isn't installed; the brand font is always named first so Slides is correct.
- **Lowercase `tiny` wordmark** — always lowercase.
- **Headlines:** heavy weight, tight tracking.
- **Eyebrows:** uppercase, letter-spaced (tracked) labels above titles.
- **Projection floor:** nothing below ~14pt (`MIN_PT`) at the 16:9 slide scale.

Canvas is full 16:9 widescreen — `13.333 × 7.5 in` (`SLIDE_W` / `SLIDE_H`).

## Layout systems

Two systems carry the whole library:

- **Direction B — electric hero.** Full-bleed electric-blue covers and section
  dividers. Used by the `cover`, `section`, and `close` layouts.
- **Direction C — split-rail + header-band.** Content slides use either a slim
  blue title rail down the side (`kpi`, `chart`, `gauges`, `content`) or a blue
  header band across the top (`table`, `dualchart`, `statgrid`, `timeline`).

Don't invent new layouts — compose from the vocabulary in `deck-spec.md`.

## Component conventions

- **Giant metric callouts.** KPIs render as oversized numbers with a small label
  and an optional delta chip (auto +/- and green/red, or a preformatted string).
- **Blue-checkmark commentary.** The signature bullet: a blue check, a **bold ink
  lead-in**, then gray (`MUTED`) detail. Authored in content as
  `"<b>Lead-in.</b> the detail"`; `rich_para` in `theme.py` renders the two-tone run.
- **Tinted total rows.** Table totals are bold and `TINT`-filled.
- **Hairline dividers** in `LINE`, never heavy rules.
- **No drop shadows.** All shapes set `shadow.inherit = False`.
- **Editable, native objects** — tables, KPIs and charts are real PPTX/Slides
  objects, never flattened to images.

## Where it lives in code

`scripts/theme.py` holds the tokens and helpers:
`BLUE/INK/MUTED/LINE/TINT`, `CHART_PALETTE`, `POS/NEG`, `FONT`/`FONT_FALL`,
`MIN_PT`, `SLIDE_W/SLIDE_H`, the shape helpers (`fill_rect`, `round_rect`, `oval`,
`hline`), the text helpers (`set_text`, `add_para`, `rich_para`), and the
formatters (`fmt_money`, `fmt_pct`, `delta_color`). Adjust the brand there and
every deck updates at once.
