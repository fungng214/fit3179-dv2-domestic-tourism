# Sources and third party notices

## Statistical data and boundaries

Tourism values are based on Tourism Research Australia data, © Commonwealth of Australia, represented by the Australian Trade and Investment Commission. Population values and geographic boundaries are based on Australian Bureau of Statistics data, © Commonwealth of Australia.

The published data are supplied under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/), subject to the publishers' exclusions for logos, third-party material and other specified content. See the [Austrade copyright notice, which covers tra.gov.au](https://www.austrade.gov.au/en/site-information/site-disclaimer) and [ABS copyright notice](https://www.abs.gov.au/website-privacy-copyright-and-disclaimer).

The original workbooks are retained in `source-data`. Selected statistical values have been converted to display units and used to calculate indices, ratios, ranks and changes. Geography was simplified, and small or distant islands were omitted for display. These adaptations are the project author's responsibility and do not imply endorsement by TRA or ABS. Dataset titles, source links and access dates are listed on the webpage and in `data/sources.json`.

The dot-density map allocates fixed-value symbols within state boundaries using a reproducible seed. These positions are a cartographic encoding of published aggregates, not observed travel or spending locations. The method follows the equal-dot, polygon-total approach described in the supplied FIT2179 Dot Maps course notes and [Esri's dot-density documentation](https://pro.arcgis.com/en/pro-app/3.4/help/mapping/layer-properties/dot-density.htm). The map was newly implemented in Vega; no external map artwork is reused.

## Software

| Component | Version | Source | Licence file |
| --- | --- | --- | --- |
| Vega | 5.33.0 | <https://github.com/vega/vega> | `assets/licenses/vega-LICENSE.txt` |
| Vega-Lite | 5.23.0 | <https://github.com/vega/vega-lite> | `assets/licenses/vega-lite-LICENSE.txt` |
| Vega-Embed | 6.26.0 | <https://github.com/vega/vega-embed> | `assets/licenses/vega-embed-LICENSE.txt` |

These projects are distributed under their BSD 3-Clause licences. Copyright notices and full licence texts are included. The distribution files were retrieved from the version-specific jsDelivr npm endpoints. All chart specifications and layouts in this project were newly authored for the assignment; no external finished chart artwork is incorporated.

## Typeface

DM Serif Display, copyright Adobe and Google LLC, is distributed under the SIL Open Font License 1.1. The unmodified font is bundled at `assets/fonts/dm-serif-display.ttf`; the full licence is `assets/licenses/DM-Serif-Display-OFL.txt`. Source: <https://github.com/google/fonts/tree/main/ofl/dmserifdisplay>.

Arial and Helvetica are named as system fonts and are not distributed with this project.

## AI assistance

OpenAI ChatGPT/Codex assisted with the HTML, CSS and JavaScript used to structure, style and embed the visualisations on the webpage.
