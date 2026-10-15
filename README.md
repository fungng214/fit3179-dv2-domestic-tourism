# How Australians travel at home

An original FIT3179 DV2 website about Australian domestic tourism, designed for a general Malaysian audience. It compares April–June observations across 2019–2026 using Tourism Research Australia and Australian Bureau of Statistics data.

## Open the website

Extract the ZIP, keep the folders together, and open `index.html` in a current desktop browser. Data and JavaScript are included locally; the page does not fetch chart data from a third-party server. All twelve charts show information on hover and have a three-dot menu at the top right. Its options are Save as SVG, Save as PNG, View Source, View Compiled Vega and Open in Vega Editor. Figure 6 also has an overnight/day-trip filter. Tooltips identify the relevant period, values and units. There are no highlighting controls, zoom controls or expandable panels. Static SVG fallbacks keep all figures visible if chart rendering is unavailable; Figure 6 defaults to overnight trips.

The submission must ultimately use your public GitHub Pages URL. A local file or this ZIP alone does not meet that requirement. Follow `COMPLETION_GUIDE.md`.

The three geographic map idioms are explicitly labelled on the page: Figure 4, proportional symbol map; Figure 5, choropleth map; Figure 11, dot-density map. The treemap is a separate spending chart and is not counted as a map.

## Project structure

| File or folder | Purpose |
| --- | --- |
| `index.html` | Complete single-page story |
| `assets/style.css` | Layout, typography, responsive rules |
| `assets/app.js` | Hover tooltips, three-dot chart menus, Figure 6 filter and responsive sizing |
| `chart-specs/` | Twelve readable JSON chart specifications |
| `assets/charts.bundle.js` | Same specifications bundled for local opening |
| `assets/static/` | Static SVG figures generated with Vega |
| `data/` | Prepared values, formulas' results, source references and validation reports |
| `source-data/` | Unmodified official workbooks and original boundary download |
| `prepare_data.py` | Reproducible extraction, unit conversions and ABS join |
| `prepare_dot_map.py` | Reproducible fixed-value dot allocation within state boundaries |
| `build_charts.py` | Original Vega and Vega-Lite specifications |
| `chart_tooltips.py` | Tooltip fields, periods, units and geographic hover information |
| `build_page.py` | Narrative, captions and source references |
| `validate_charts.cjs` | Headless compilation, SVG rendering and signal checks |
| `COMPLETION_GUIDE.md` | Sketch, publication, submission and interview preparation |
| `THIRD_PARTY_NOTICES.md` | Credits and licences |

## Rebuild after editing

The shipped website is already built. Rebuilding requires Python 3 with `openpyxl`, and Node.js 20 or newer. The chart libraries are bundled, so no npm installation is needed.

```bash
python prepare_data.py
python prepare_dot_map.py
python build_charts.py
node validate_charts.cjs
python build_page.py
```

Edit narrative in `build_page.py`, chart design in `build_charts.py`, styles in `assets/style.css`, and browser behavior in `assets/app.js`. If you edit only a JSON chart file, also update the bundle and static fallback; rebuilding is the safer way to keep all representations consistent.

## Validation completed

- Source units, state names, periods and workbook cells checked.
- Eight national and 64 destination/year records checked.
- Current intrastate/interstate totals and expense groups reconciled to published totals.
- All 12 specifications compiled and rendered to SVG using the bundled runtimes.
- Both trip-type filter options ran without invalid SVG geometry.
- Rendered charts visually inspected; the year-axis zero baseline and overlapping text were corrected.
- Local links and document structure checked during packaging.
- Updated 15 October 2026: replaced the spending cartogram with a geographic dot-density map, checked all 258 dots fall within their assigned state, and verified whole-dot rounding against the source expenditure totals.

- Updated 15 October 2026: enabled tooltips on all twelve charts while retaining only the Figure 6 trip-type filter as a data control. Highlighting selectors and expandable tables remain removed.
- Tooltip payloads checked on rendered chart marks, including both trip types and the ACT inset.
- Updated 15 October 2026: replaced the links below each chart with a three-dot Vega action menu. All five options appear on every chart. For the two charts authored directly in Vega, View Compiled Vega opens the same native Vega specification.

Full-page browser rendering, hover behaviour, menu actions, keyboard/mouse operation of the trip-type filter and GitHub Pages deployment still need a final check on your laptop. The available environment did not provide the required browser preview capability. Do not describe the page as browser-tested until you have completed that check.

## Attribution

Author: Ng Cheok Fung. Prepared 14 October 2026. OpenAI ChatGPT/Codex assisted with data preparation, chart specifications, website code and draft text. Review, understand and adapt the project before submission. Keep the AI acknowledgement and comply with the unit's stated acknowledgement requirements.
