# Deck spec reference

A deck is a JSON file: `{ "title": str, "slides": [ {slide}, ... ] }`.
`build.py spec.json out.pptx` renders it to an editable Tiny-branded `.pptx`.

Every slide has a `"layout"` key naming one of the builders below. All other
keys are layout-specific. Missing/blank fields render cleanly (blank templates
work). Money is entered as already-formatted display strings in audience decks
(e.g. `"$19.1M"`); the data-driven board pack computes and formats from raw
`$000s` figures via `board_model.py`.

Commentary strings support a `<b>...</b>` bold lead-in (the signature Tiny
checkmark bullet: bold ink lead-in + gray detail). `&amp;` is decoded.

Colors are `#RRGGBB` hex strings. The house chart palette (used automatically
when you omit `colors`) is blue → indigo → violet → azure:
`#2B28F5 #1A1980 #7A5CF5 #2E8FE0 #C44DDB #5BB0E8 #8E7BFF #BFC0E6`.

---

## Layouts

### `cover` — full-bleed electric-blue hero (Direction B)
```
{ "layout":"cover", "eyebrow":"BOARD UPDATE — DRAFT", "title":"Monthly Board Results",
  "subtitle":"One sentence framing.", "period":"April 2026", "entity":"Tiny Ltd.",
  "preparedBy":"Office of the CFO", "confidential":"Confidential" }
```

### `section` — blue section divider
```
{ "layout":"section", "number":"01", "title":"Consolidated Results", "subtitle":"optional" }
```

### `kpi` — slim blue title rail + up to 4 giant metric callouts + checkmark commentary
```
{ "layout":"kpi", "eyebrow":"CONSOLIDATED · PRO FORMA", "title":"April Results Update",
  "kpis":[ {"label":"Revenue","value":"$19.1M","delta":6.8,"deltaLabel":"YoY","goodUp":true,"sub":"optional"} ],
  "commentary":["<b>Lead-in.</b> detail..."], "footnote":"optional", "railNote":"optional" }
```
- `delta` may be a number (auto +/- and green/red) or a preformatted string.
- `goodUp:false` flips the favorable color (e.g. for costs/leverage).

### `table` — blue header band + native editable table (full width)
```
{ "layout":"table", "eyebrow":"DETAIL", "title":"P&L by Company", "bandMeta":"April 2026 · $000s",
  "columns":[{"label":"Company"},{"label":"Revenue"}, ...],
  "rows":[ ["Beam","5,545", ...], ["Consolidated","19,076", ...] ],
  "totalRows":[6], "varianceCols":[4,5], "highlightLastCol":true, "note":"optional" }
```
- `totalRows`: 0-based row indices rendered as bold totals (tinted).
- `varianceCols`: column indices whose numeric values get green/red coloring.

### `chart` — blue rail (eyebrow/title/commentary/note) + one native chart
```
{ "layout":"chart", "eyebrow":"TREND", "title":"Monthly Revenue",
  "chartType":"column|combo|doughnut|pie|bar|waterfall|bubble",
  "data":{ ... see chart data below ... },
  "commentary":["..."], "note":"optional" }
```

### `dualchart` — blue band + two charts side by side (e.g. twin donuts)
```
{ "layout":"dualchart", "eyebrow":"COMPOSITION", "title":"Portfolio Mix", "bandMeta":"April 2026",
  "charts":[ {"title":"Revenue","chartType":"doughnut","data":{...}},
             {"title":"Adj. EBITDA","chartType":"doughnut","data":{...}} ],
  "note":"optional" }
```

### `statgrid` — blue band + grid of big-number cards
```
{ "layout":"statgrid", "eyebrow":"SCOREBOARD", "title":"At a Glance", "perRow":3,
  "stats":[ {"label":"Revenue","value":"$19.1M","sub":"+6.8% YoY"} ], "commentary":["..."] }
```

### `gauges` — blue rail + horizontal gauges with covenant markers
```
{ "layout":"gauges", "eyebrow":"CREDIT", "title":"Leverage & Coverage",
  "gauges":[ {"label":"Net leverage","value":3.7,"max":6,"marker":4.5,"unit":"x"} ],
  "commentary":["..."], "note":"optional" }
```

### `timeline` — blue band + columnar timeline (debt maturities etc.)
```
{ "layout":"timeline", "eyebrow":"DEBT", "title":"Maturity Profile",
  "items":[ {"year":"2026","label":"Scotia facility","value":12000,"valueLabel":"$12M"} ],
  "note":"optional" }
```

### `content` — blue rail + editorial bullets (generic)
```
{ "layout":"content", "eyebrow":"OUTLOOK", "title":"Priorities",
  "lead":"Optional bold lead sentence.", "bullets":["<b>X</b> detail"], "footnote":"optional" }
```

### `close` — blue rally close
```
{ "layout":"close", "title":"Thank you", "subtitle":"optional", "contact":"optional" }
```

---

## Chart `data` by `chartType`

- **column**: `{ "cats":[...], "values":[...], "color":"#hex"?, "colors":[...]?, "fmt":"#,##0"? }`
- **combo** (columns + margin line on 2nd axis): `{ "cats":[...], "values":[...], "line":[...], "fmt":"#,##0"?, "lineFmt":"0\"%\""? }`
- **doughnut / pie**: `{ "labels":[...], "values":[...], "colors":[...]? }`
- **bar** (horizontal): `{ "cats":[...], "values":[...], "colors":[...]?, "fmt":"#,##0"? }`
- **waterfall**: `{ "labels":[...drivers...], "deltas":[...+/-...], "start":num, "end":num }`
- **bubble**: `{ "points":[ {"label","color","x","y","size"} ], "xRange":[lo,hi]?, "yRange":[lo,hi]?, "xFmt"?, "yFmt"? }`

Per-point colors: omit `colors`/`color` to auto-cycle the house palette.
