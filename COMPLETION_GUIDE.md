# Complete your domestic tourism assignment

The website and source files are prepared. Your submission still needs your own hand-drawn sketch, public GitHub Pages links, student details and a screenshot of the final published page. The brief gives a deadline of **25 October 2026 at 11:55 PM**; confirm the submission time in Moodle.

## First review the story

Open `index.html`. Read every chart caption and try both options in the overnight/day-trip filter on Figure 6. Also hover over points, bars, cells, map areas and map labels to read their values. Each chart also has a three-dot menu at the top right for SVG/PNG export, source inspection and opening the chart in Vega Editor. Inspect the source workbooks and chart data files. Adjust wording or design where your own judgment differs. This is also preparation for the Week 12 interview.

The main findings are:

- June-quarter overnight trips were 4.2% above 2019 in 2026; nominal spending was 66.1% higher. That is not a claim of 66.1% real growth.
- Overnight holiday visit-reason counts rose 7.0% from June 2025 to June 2026, while business counts fell 37.7%.
- NSW had the most destination visits, while NT had the most visitor nights relative to resident population.
- Accommodation was the largest single expenditure category, at 28.2% of June 2026 overnight spending.

Use the values table or workbook to explain each statement. Do not invent reasons for the fall in business travel or treat descriptive differences as statistically significant.

## Draw the required sketch by hand

The rubric awards zero sketch marks if the sketch is created digitally. Draw it yourself on paper. The following is a layout guide, not a substitute sketch and not evidence of a past tutor discussion. If the Week 7 sketch discussion was missed, ask your tutor how to handle that requirement honestly.

Use one A4 portrait sheet. Draw a tall page outline and divide it into four clearly labelled sections beneath a title and introductory statistics. Keep the order consistent with the finished website. Use a ruler, clear lettering and a small number of coloured pencils. Do not draw every source value; show enough marks to identify each idiom, its axes and its meaning.

| Section | Draw these figures | Annotate on the sketch |
| --- | --- | --- |
| 1 Change over time | One wide indexed line chart; connected dot chart and heatmap beneath it | 2019 baseline 100; series change after 2024; year and destination axes; spending grows faster than trips |
| 2 Destinations | Proportional symbol map beside choropleth map | Circle area = visits; colour = nights per resident; legends; ACT callout; the two maps answer different questions |
| 3 Travel purposes | One wide grouped purpose bar chart; waffle and scatterplot underneath | Year colours; overnight/day-trip dropdown; 75/25 split; scatter axes in nights and AUD |
| 4 Spending | Wide treemap; wide waterfall; dot-density map and bump chart side by side | Rectangle area = spending; signed category changes; one equal dot ≈ A$100m; ACT inset; rank 1 at top |

Add notes for the serif headings, sans-serif body, teal/gold/blue palette, whitespace, source footnotes and author/date. Clearly show where headings and explanatory text sit relative to each figure. Scan or photograph the full sheet straight-on in good light; crop only the surrounding background. Save a legible PDF as `sketch.pdf` in the website root. Insert the same image in Part C of the assignment document. Keep the original paper for discussion if needed.

## Publish the website on GitHub Pages

1. Sign in to your GitHub account and create a **public** repository, for example `fit3179-dv2-domestic-tourism`.
2. Upload the **contents** of this project folder. `index.html` must be at the repository root, beside `assets`, `data`, `chart-specs` and `source-data`. Do not upload only the ZIP or nest the whole project one level deeper. Keep `.nojekyll` if your upload method includes it.
3. Add your scanned `sketch.pdf` at the same root. Keep your student ID and the private assignment document out of the public website repository unless your tutor specifically requires them there.
4. Open repository **Settings → Pages**. Under **Build and deployment**, choose **Deploy from a branch**, then `main` and `/(root)`. Save and wait for deployment to finish.
5. Copy the actual URL shown by GitHub Pages. Its usual form is `https://YOUR-USERNAME.github.io/fit3179-dv2-domestic-tourism/`; replace the example with the real published URL.
6. Open that URL in an incognito/private window. Scroll through all twelve charts, test both options in the Figure 6 trip-type filter, open each chart’s three-dot menu, check its source and export options, open every source workbook link in the final source register and open `sketch.pdf`.

GitHub instructions were checked against the official guide: <https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site>.

## Finish the assignment document

Use the supplied `DV2_Submission_Draft.docx`, which follows the assignment template's Parts A–D.

- Fill in your student ID and actual FIT3179 studio session. Confirm the name is correct.
- Part A: paste the working public website URL.
- Part B: review the drafted domain, why/who, what and how explanations. Make sure you understand and agree with them. Retain the AI acknowledgement and add any declaration required by Moodle or Learn HQ.
- Part C: paste the public PDF URL, normally the website URL followed by `sketch.pdf`, and insert the complete legible image of your hand-drawn sketch.
- Part D: insert a full-page screenshot of the **final published** website. In Chrome or Edge, open Developer Tools, open the command menu, search for “Capture full size screenshot”, and save the result. Scroll through the page first and check that all twelve figures are visible. Use the default Overnight option for Figure 6 so the screenshot matches the nearby overnight comparison, and close all chart menus before capturing the page. Inspect the screenshot before inserting it. A long page may require a larger page size or an additional readable image; follow the tutor's formatting directions.
- Remove instructional placeholders. Submit in the format requested on Moodle, and verify both URLs again after your last change.

## How the design targets the rubric

The following is a design mapping, not a promised mark. Effective use and your explanation matter as well as chart count.

| Figure | Idiom | Conservative classification | Why it belongs |
| --- | --- | --- | --- |
| 1 | Indexed line chart | Basic | Compare trends with a common baseline |
| 2 | Connected dot chart | Basic | Compare two endpoints on a shared scale; counted conservatively because the rubric excludes dot plots |
| 3 | Heatmap | Advanced | Compare destination recovery across years |
| 4 | Proportional symbol map | Advanced map 1 | Locate raw visit volumes using circle area |
| 5 | Choropleth | Advanced map 2 | Locate tourism intensity using a population-normalised rate |
| 6 | Grouped bar | Basic | Compare purpose counts without forcing overlapping categories into a whole |
| 7 | Waffle | Advanced | Communicate a current mutually exclusive travel split |
| 8 | Scatterplot | Basic | Relate average stay length to allocated spending per visit |
| 9 | Treemap | Advanced | Show mutually exclusive spending composition |
| 10 | Waterfall | Advanced | Reconcile signed spending changes to their net total |
| 11 | Dot-density map | Advanced map 3 | Number of equal dots represents spending within geographic state boundaries |
| 12 | Bump chart | Advanced | Follow ordinal spending ranks rather than money gaps |

This gives 12 charts and 8 advanced idioms under the stated conservative classification. The three geographic maps are Figures 4, 5 and 11, labelled Map 1 of 3, Map 2 of 3 and Map 3 of 3 on the page. The treemap is a spending-composition chart and is not counted as a map. The final classification remains the marker's decision.

The two data providers are TRA and ABS. Figure 5 actually combines them in one measure. Merely listing two sources would not demonstrate a meaningful join.

## Interview preparation

Practise answering in your own words, then point to the relevant chart and code.

| Likely question | What a strong answer explains |
| --- | --- |
| Who is the audience? | General Malaysian readers. Domestic tourism, Australian state abbreviations, quarter dates and AUD are explained because local Australian knowledge cannot be assumed. |
| Why compare June quarters? | The same seasonal window reduces seasonal mismatch; it does not describe full-year totals. June means April–June. |
| What is your domain question? | How Australian residents' domestic travel changed over time, and how destination, purpose and expenditure reveal different aspects of that change. |
| What are the data types? | Destination and purpose are nominal; year is ordered temporal; trips, nights, spending and population are quantitative; rank is ordinal; boundaries are spatial. |
| Why use an index? | Trips, nights and money have different units. Dividing by each measure's 2019 value and multiplying by 100 supports relative-change comparison. |
| What changed in 2025? | DoTS replaced NVS, with changes to collection and coverage. The historical series uses TRA's revised backcast rather than splicing original NVS totals into DoTS. |
| Why is the choropleth a rate? | Raw totals are strongly affected by size. Visitor nights divided by ABS resident population provides a relative measure. It does not measure a resident's likelihood of travel. |
| Why are there three map types? | The proportional symbol map encodes visits through circle area; the choropleth encodes visitor nights per resident through colour; the dot-density map encodes spending through the number of equal dots. All three use geographic state boundaries. The treemap does not count. |
| Do the dots show actual tourist locations? | No. They are allocated within each state to represent its published total, with one dot approximately A$100 million. Whole-dot counts are rounded per state; exact totals remain in the source workbook. The map cannot identify local tourism hotspots. ACT is enlarged, so its density is not comparable with the main map. |
| How are circle sizes calculated? | Vega's size channel encodes symbol area. Radius is not scaled directly to the data. Doubling the value doubles area, not radius. |
| Which projection did you choose? | An Australian conic equal-area projection, with standard parallels at 18°S and 36°S and central meridian 134°E. It preserves area; it does not preserve every distance or angle. The dot-density map retains this projection; its ACT inset is explicitly enlarged. |
| Why not a purpose pie chart? | Trip counts are visit reasons and can overlap. A pie would imply a mutually exclusive whole. Purpose expenditure also uses a different main-purpose definition. |
| Why not add up state visits? | A trip can visit multiple destinations, so state counts overlap. The national trip total is taken directly from TRA. |
| What does nominal spending mean? | Money at the prices of that period. More spending can reflect prices, travel mix and quantities; these data do not isolate those causes. |
| What is in Other spending? | Smaller published spending items plus the unallocated and rounding residual needed to reconcile to TRA's total. The components are disclosed. |
| Why is interactivity limited? | The Figure 6 trip-type filter switches between overnight and day trips. Tooltips reveal the period, values and units for an individual mark without adding permanent labels everywhere. Axes, legends and captions keep the main comparisons understandable before hovering. |
| How did you use AI? | Explain the real assistance in research, extraction, code and draft wording; show what you reviewed, changed and understood. Do not claim work or checks you did not perform. |

## Final checks on your laptop

- At 1280 × 800 and 100% zoom, the page has no horizontal scrolling; chart labels remain legible.
- Every chart has a three-dot menu with Save as SVG, Save as PNG, View Source, View Compiled Vega and Open in Vega Editor. Check downloads and source views, including the treemap and dot-density map. For those two native Vega charts, source and compiled Vega refer to the same specification.
- Only Figure 6 has a data-filter dropdown. Both trip types display correctly, keyboard focus is visible and the filter works with the keyboard. There are no selection-highlighting controls or expandable data panels.
- Hover over marks in every chart, including map labels and the ACT inset. Tooltips must show the correct period, value and units, fit within the window and disappear when the pointer leaves. Check the Figure 6 values for both trip types.
- Axes, labels and captions show the correct units and dates. Source workbooks provide the supporting numeric values.
- All twelve chart sections load in a private window with no missing assets, and the browser console has no chart errors.
- The chart JSON and sketch PDF are publicly accessible in the same repository.
- Author, date and sources are visible on the website. Retain the AI acknowledgement in the assignment document.
- Part A and Part C contain real URLs; student ID and studio session are complete; sketch and webpage screenshot are inserted.
- The paper sketch matches the final page order and the tutor's feedback is reflected where applicable.

The source and headless chart checks are complete. Whole-page browser interaction and deployment were not tested in the creation environment, so these final checks are still necessary.
