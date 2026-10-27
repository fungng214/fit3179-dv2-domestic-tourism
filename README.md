# How Australians travel at home

An original FIT3179 DV2 website about Australian domestic tourism, designed for a general Malaysian audience. It compares April–June observations across 2019–2026 using Tourism Research Australia and Australian Bureau of Statistics data.

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
| `readability.py` | Twelve-word maximum for fallback prose lines |
| `assets/readability.js` | Natural wrapping with a twelve-word line cap |
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
- Updated 15 October 2026: replaced the links below each chart with a three-dot Vega action menu. All five options appear on every chart. For Figure 11, authored directly in Vega, View Compiled Vega opens the same native Vega specification.

Updated 27 October 2026: tightened section and card spacing, placed wide charts alongside their explanations, enlarged supporting text, added reading cues, and enforced serif headings with sans-serif body and chart labels. Prose has a twelve-word maximum per rendered line, with natural wrapping on narrower screens and conservative no-JavaScript fallback breaks. Map heights adapt to narrow screens to reduce unused space.

Chromium checks at 1440, 960 and 390 pixels confirmed all twelve charts mount, all twelve menus appear, both filter options can be selected, serif headings and sans-serif body fonts are applied, no horizontal page overflow occurs, and prose stays within twelve words per line. Chart specifications also compile and render with both filter settings. GitHub Pages deployment is not part of this revision; upload the rebuilt project contents to update the public page.

## Attribution

Author: Ng Cheok Fung. Prepared 14 October 2026. Webpage implementation acknowledgement: OpenAI ChatGPT/Codex assisted with the HTML, CSS and JavaScript used to structure, style and embed the visualisations on the webpage.

## Lecturer feedback revision — 27 October 2026

- Highlight boxes now show their content directly, without a Reading cue heading.
- Figure 7 includes a translucent central annotation: 75.1% of trips, with 20.34m of 27.08m overnight trips. The callout is part of the exported chart.
- Figure 9 replaces the treemap with a sorted horizontal bar chart. These flat categories require no artificial hierarchy.
- Figure 12 replaces the bump chart with eight small-multiple indexed spending trends. Each panel uses the same 2019 = 100 baseline and shared scale; final labels show percentage growth. The survey transition remains marked.
- Figure 11 is displayed across the page with its explanation alongside.
- A scoped webpage-development acknowledgement is included in the footer. The broader project assistance is documented below and should be reflected accurately in any assessment declaration.

The project now has eleven Vega-Lite figures and one native Vega figure. Six figures retain the previous conservative advanced classification; Figures 9 and 12 are conservatively counted as basic. Do not assume an advanced mark for small multiples without checking the rubric.

## Continuous colour legends — 27 October 2026

Figures 3 and 5 use continuous horizontal colour bars with visible outlines and numeric labels. The heatmap shows a brown–neutral–teal gradient; zero is marked at its correct position on the asymmetric −60% to +30% scale. The choropleth shows a light-to-dark teal gradient from zero to five visitor nights per resident. Colour domains, chart colours and data are unchanged.

These two charts render to canvas on the webpage to avoid SVG gradient-reference display issues. Tooltips and the three-dot menus remain available, including both PNG and SVG downloads. Static SVG fallbacks retain the same continuous legends. Legend width adapts to the chart width.
