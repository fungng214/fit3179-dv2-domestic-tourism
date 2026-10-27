"""Generate the story and hover-enabled chart containers from verified data."""
from pathlib import Path
import json
from html import escape as esc
from readability import limit_prose_lines

ROOT=Path(__file__).resolve().parent
def load(name): return json.loads((ROOT/'data'/name).read_text())
C=load('chart-catalogue.json'); N=load('national.json'); S=load('state-history.json')
L=load('latest-states.json'); P=load('purpose.json'); E=load('expense-groups.json')
W=load('waterfall.json'); M=load('travel-mix.json')
D=load('spending-dot-summary.json')
takeaways={
1:'By June quarter 2026, nominal overnight spending was <strong>66.1% above 2019</strong>, while trips were only <strong>4.2% higher</strong>. The spending line includes price changes; it is not a measure of real growth.',
2:'Tasmania and Western Australia recorded about <strong>15% more visits</strong> than in June quarter 2019. The ACT remained <strong>7.6% below</strong> its 2019 level. These estimates describe change, not statistical significance.',
3:'Every state and territory fell below its 2019 June-quarter level in 2020. Later recoveries differed. Green means above that destination’s own baseline; brown means below it.',
4:'New South Wales recorded <strong>9.36 million</strong> overnight destination visits in June quarter 2026, followed by Victoria and Queensland. Circle <strong>area</strong> represents visit volume.',
5:'The Northern Territory hosted <strong>4.31 visitor nights per resident</strong>, compared with 3.20 in New South Wales. A large visitor total and a high rate relative to population answer different questions.',
6:'Overnight trips reporting holidays rose from <strong>12.11 million to 12.95 million</strong>. Those reporting business fell from <strong>3.25 million to 2.02 million</strong>. Use the dropdown to compare day trips too.',
7:'<strong>75.1%</strong> of overnight trips were intrastate: travel within the traveller’s home state or territory. Interstate trips crossed a state or territory border. Each square is about one percentage point.',
8:'Northern Territory visits averaged <strong>4.20 nights and A$1,637</strong> in allocated spending. Victoria averaged <strong>2.76 nights and A$767</strong>. These are destination averages, not a quoted holiday budget.',
9:'Accommodation accounted for <strong>A$7.25 billion</strong>, or <strong>28.2%</strong> of overnight expenditure. The area of each rectangle represents its share of the A$25.73 billion total.',
10:'Total overnight spending rose by <strong>A$540.1 million</strong> (2.1%). Accommodation and the combined “Other spending” group added the most, while shopping and drinks recorded the largest decreases.',
11:'New South Wales received <strong>A$7.52 billion</strong> in allocated overnight spending, Queensland A$6.36 billion and Victoria A$5.60 billion. <strong>More equal-sized dots mean more spending.</strong> Dots represent state totals; their positions do not show where spending occurred.',
12:'New South Wales and Queensland held the top two spending ranks throughout these June quarters. Queensland moved into first place in <strong>2024</strong>. A rank shows order, not the size of the spending gap.'}
footnotes={
1:'TRA revised overnight backcast Tables 1–3 (2019–2024); DoTS June 2026 Table 1a (2025–2026). Each point is April–June only. Dotted vertical line: change of statistical series.',
2:'TRA revised backcast Table 1 and DoTS Table 1a. June quarters 2019 and 2026. A trip visiting several states may be counted in each state.',
3:'TRA revised backcast Table 1 and DoTS Table 1a. Formula: (visits ÷ June 2019 visits − 1) × 100. Colour is capped at −60% and +30%; the source data retain exact values.',
4:'TRA DoTS Table 1a; ABS ASGS Edition 3 boundaries. June quarter 2026. State symbols are aggregate anchors, not exact visitor locations; multi-state visits overlap.',
5:'TRA DoTS Table 1a joined to ABS population Table 4 at 31 March 2026, using matching state names. Nights ÷ all-age residents. This is destination activity per resident, not residents’ travel frequency.',
6:'TRA DoTS Tables 3a and 7a. April–June 2025 and 2026. Visit reasons can overlap, so these counts must not be treated as shares of a whole.',
7:'TRA DoTS Table 2a. April–June 2026. Squares round 75.1% and 24.9% to 75 and 25; the precise percentages are 75.1% and 24.9%.',
8:'TRA DoTS Table 1a. April–June 2026. Nights and allocated expenditure are divided by matching destination visit totals. No claim about causation or individual travellers is implied.',
9:'TRA DoTS Table 4a. April–June 2026. Other spending combines smaller categories plus A$29.917m unallocated expenditure and rounding residual. Exact components are listed in the source workbook (Table 4a).',
10:'TRA DoTS Table 4a. April–June 2026 minus April–June 2025, nominal AUD million. Bars accumulate category changes; the last bar is the net change. Other spending includes unallocated expenditure and rounding.',
11:'TRA DoTS Table 1a; ABS boundaries. April–June 2026. One dot ≈ A$100m; each state’s count is rounded to whole dots. Dots are allocated within state boundaries, not observed locations. ACT is enlarged, so its dot density is not comparable with the main map. The source workbook retains exact totals.',
12:'TRA revised backcast Table 3 and DoTS Table 1a. April–June each year. Spending ÷ the destination’s 2019 spending × 100. Nominal AUD; not inflation-adjusted. The dotted divider marks the 2025 series transition.'}

# Concise chart summaries keep the reading area balanced with the figures.
takeaways.update({
1:'Nominal overnight spending was <strong>66.1% above 2019</strong>. Trips were only <strong>4.2% higher</strong>. Spending includes price changes, so this is not real growth.',
2:'Tasmania and Western Australia recorded about <strong>15% more visits</strong>. The ACT remained <strong>7.6% below</strong> its 2019 level.',
3:'Every destination fell below its 2019 level in 2020. Green shows gains against each destination’s baseline; brown shows losses.',
4:'New South Wales recorded <strong>9.36 million</strong> overnight destination visits. Victoria and Queensland followed. Larger circle areas indicate more visits.',
5:'The Northern Territory hosted <strong>4.31 visitor nights per resident</strong>. New South Wales recorded 3.20. Population-adjusted rates reveal a different pattern.',
6:'Overnight holiday trips rose from <strong>12.11m to 12.95m</strong>. Business trips fell from <strong>3.25m to 2.02m</strong>. Select Day trip to explore the other trip type.',
7:'<strong>75.1%</strong> of overnight trips stayed within the traveller’s home state. The remaining <strong>24.9%</strong> crossed a state or territory border.',
8:'Northern Territory visits averaged <strong>4.20 nights and A$1,637</strong>. Victoria averaged <strong>2.76 nights and A$767</strong>. These are destination averages, not holiday budgets.',
9:'Accommodation received <strong>A$7.25 billion</strong>: <strong>28.2%</strong> of overnight expenditure. The sorted bars compare spending categories directly.',
10:'Overnight spending rose by <strong>A$540.1 million</strong>, or 2.1%. Accommodation and Other spending added the most. Shopping and drinks recorded the largest decreases.',
11:'New South Wales received <strong>A$7.52 billion</strong> in overnight spending. Queensland received A$6.36 billion; Victoria received A$5.60 billion. More dots indicate more spending.',
12:'Western Australia’s nominal spending rose <strong>106.3%</strong> from 2019 to 2026. The Northern Territory rose <strong>96.9%</strong>; ACT rose <strong>15.0%</strong>. These panels reveal changes hidden by stable rankings.'
})
annotations = {
1:'100 = the 2019 baseline. Above 100 means growth.',
2:'Hollow dots: 2019. Filled dots: 2026. Follow each connecting line.',
3:'Read down to compare destinations; across to follow their recovery.',
4:'Compare circle areas, not the size of each state.',
5:'Darker states host more visitor nights per resident.',
6:'Compare the two bars within each purpose; reasons can overlap.',
7:'Around three in four overnight trips stay within the home state.',
8:'Further right = longer stays. Higher up = more spending per visit.',
9:'Accommodation accounts for more than one-quarter of overnight spending.',
10:'Floating bars build the total. The final bar shows net change.',
11:'Dots show state totals, not actual spending locations. ACT is enlarged.',
12:'Every panel uses the same scale: 2019 = 100. End labels show growth since 2019.'
}

def chart(n):
    c=C[n-1]; k=c['id']
    filter_attr=' data-filter-chart="'+k+'"' if n==6 else ''
    map_tag=f' · Map {c["map_number"]} of 3' if c.get('map_number') else ''
    key='<div class="key"><span class="old">June 2019</span><span>June 2026</span></div>' if n==2 else ''
    annotation = '' if n == 7 else f'<p class="chart-annotation">{annotations[n]}</p>'
    return f'''<article class="chart-card {'wide' if c['wide'] else ''}" aria-labelledby="title-{n}">
      <div class="chart-copy"><p class="chart-label">Figure {n:02d} · {esc(c['idiom'])}{map_tag}</p><h3 id="title-{n}">{esc(c['title'])}</h3>
      <p class="takeaway">{takeaways[n]}</p>
      {annotation}</div>
      <div class="chart-visual">{key}<div class="chart-frame" data-chart="{k}"{filter_attr} role="group" aria-label="{esc(c['question'])}"><img src="assets/static/{k}.svg" alt="{esc(c['question'])} Supporting values are available in the cited source workbook." loading="lazy"></div>
      <p class="chart-foot">{footnotes[n]}</p></div>
    </article>'''


chapters=[('change','01','A recovery with a bigger price tag','Australian residents made 27.1 million overnight trips in April–June 2026. Trip numbers were close to their 2019 level, but the money spent was much higher. A common baseline makes that difference visible.',[1,2,3]),
('destinations','02','The busiest places are only part of the story','Australia has six states and two mainland territories. First locate the biggest destination totals, then account for the size of the resident population. The two maps reveal different patterns.',[4,5]),
('purpose','03','Holidays grow as business travel falls','Why people travel matters as much as how many trips they take. The latest comparable June quarters show holidays and business moving in different directions. Most overnight trips still stay within a state.',[6,7,8]),
('spending','04','Where the travel dollar goes','Expenditure describes another side of domestic tourism: what travellers buy and which destinations receive the spending. All amounts below are in Australian dollars, with no inflation adjustment.',[9,10,11,12])]

body=''
for id,num,title,intro,nums in chapters:
    extra=''
    if id=='change':extra='<div class="method-note"><p><strong>Read the timeline carefully.</strong> The Domestic Tourism Statistics collection (DoTS) replaced the National Visitor Survey in January 2025.</p><p>Historical values use TRA’s <em>revised backcast</em> for closer comparability. The dotted divider marks this transition; some uncertainty remains.</p></div>'
    body+=f'<section class="chapter" id="{id}"><div class="chapter-head"><span class="chapter-number">{num}</span><div><h2>{title}</h2><p class="chapter-intro">{intro}</p></div></div>{extra}<div class="chart-grid">'+''.join(chart(n) for n in nums)+'</div></section>'

page='''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="How Australian domestic tourism changed across June quarters 2019–2026: trips, destinations, travel purposes and spending."><title>How Australians travel at home · Domestic tourism</title><link rel="stylesheet" href="assets/style.css"><link rel="icon" href="data:,"></head>
<body><a class="skip" href="#main">Skip to the tourism story</a><header class="topbar"><div class="wrap"><span class="brand">Domestic tourism · Australia</span></div></header>
<main id="main"><div class="wrap"><section class="hero"><p class="eyebrow">April–June comparisons · 2019–2026</p><h1>How Australians<br>travel <span>at home</span></h1><p class="lede">Travel has recovered unevenly. Holidays are growing, business trips are falling, and spending tells a different story from trip numbers.</p><p class="byline">By Ng Cheok Fung · Monash University Malaysia · 14 October 2026</p>
<div class="statrow" aria-label="June quarter 2026 highlights"><div class="stat"><strong>27.1m</strong><span>domestic overnight trips</span><small>2.0% fewer than June quarter 2025</small></div><div class="stat"><strong>+7.0%</strong><span>overnight holiday trips</span><small>Change from June quarter 2025</small></div><div class="stat"><strong>−37.7%</strong><span>overnight business trips</span><small>Change from June quarter 2025</small></div></div>
<div class="reading-note"><p><strong>For readers in Malaysia:</strong> domestic tourism means Australian residents travelling within Australia. These are <strong>trips, not unique people</strong>; one person may travel several times.</p><p>A June quarter covers <strong>April to June</strong>, not a whole year. Money is shown in <strong>AUD (A$)</strong>. Hover over chart marks or map labels to see values, dates and units. Use the trip-type filter on Figure 6 to compare overnight and day trips.</p></div></section>'''+body+'''
<p class="closing">Australia’s domestic tourism story is about more than recovery in trip counts. The purpose of travel, the destination and the money spent reveal different kinds of change.</p></div>
<section class="methods" id="sources"><div class="wrap"><h2>Sources and how to read the data</h2>
<div class="methods-grid"><div class="method-column"><div class="method-block"><h3>The statistical series</h3><p>Tourism Research Australia (TRA) supplies domestic trips, nights and expenditure. The latest two-year comparisons use the June quarter 2026 DoTS workbook. Historical comparisons use only June quarters from the revised 2019–2024 overnight backcast, joined to the 2025–2026 DoTS estimates. The new collection covers Australian residents aged 14 years and over and changed collection methods and routine travel treatment. <a href="https://www.tra.gov.au/en/about-us/changes-to-the-australian-resident-tourism-statistics-collection-in-2025">Read TRA’s explanation of the change</a>.</p>
</div><div class="method-block"><h3>Source register</h3><ol><li>Tourism Research Australia (2026). <a href="https://www.tra.gov.au/en/tourism-statistics/domestic-tourism-statistics-results">Domestic Tourism Statistics June quarter 2026</a>. Tables 1a, 2a, 3a, 4a and 7a. <a href="source-data/dots-june-2026.xlsx">Source workbook</a>.</li><li>Tourism Research Australia (2026). <a href="https://www.tra.gov.au/en/tourism-statistics/domestic-tourism-statistics-results/dots-march-2026">Revised overnight backcast 2019–2024</a>. Tables 1–3, June quarters only. <a href="source-data/dots-backcast-revised.xlsx">Source workbook</a>.</li><li>Australian Bureau of Statistics (2026). <a href="https://www.abs.gov.au/statistics/people/population/national-state-and-territory-population/mar-2026">National, state and territory population, March 2026</a>. Table 4, estimated resident population, persons. <a href="source-data/abs-population.xlsx">Source workbook</a>.</li><li>Australian Bureau of Statistics. <a href="https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs/edition-3-july-2021-june-2026/access-and-downloads/data-services-and-apis">ASGS Edition 3 state and territory boundaries</a>, matching the June 2026 observation period. Coastlines simplified for display; small and distant islands omitted. <a href="data/australia-states.geojson">Display geometry</a>.</li></ol><p>Sources accessed 14 October 2026. Calculations and joins are reproducible in <a href="prepare_data.py">prepare_data.py</a>; <a href="data/source-cells.json">source cell references</a> retain the origin and units of the historical, current state and population values. Purpose and expenditure files include their own cell references.</p>
</div></div><div class="method-column"><div class="method-block"><h3>Four definitions that matter</h3><ul><li><strong>Trips and destination visits:</strong> national trips count journeys. State totals count visits to destinations; a multi-state journey can appear in more than one state. State visit totals are therefore not shares that must add to the national trip total.</li><li><strong>Visit reason:</strong> the purpose chart reports reasons recorded during a trip. Reasons can overlap. It compares counts rather than constructing a 100% breakdown. Expenditure by main trip purpose uses a different definition and is not divided by these counts.</li><li><strong>Visitor nights per resident:</strong> June quarter 2026 visitor nights divided by the ABS estimated resident population at 31 March 2026. The denominator covers all ages and approximates the population at the start of the quarter. It describes tourism activity relative to destination population, not local residents’ propensity to travel.</li><li><strong>Money and uncertainty:</strong> spending is in nominal Australian dollars. Changes include price effects and are not inflation-adjusted. Values are survey and model estimates; displayed precision supports traceability rather than claims of exact counts or statistically significant differences.</li></ul>
</div><div class="method-block"><h3>State and territory abbreviations</h3><div class="state-key"><div><strong>NSW</strong>New South Wales</div><div><strong>VIC</strong>Victoria</div><div><strong>QLD</strong>Queensland</div><div><strong>WA</strong>Western Australia</div><div><strong>SA</strong>South Australia</div><div><strong>TAS</strong>Tasmania</div><div><strong>ACT</strong>Australian Capital Territory</div><div><strong>NT</strong>Northern Territory</div></div>
</div></div></div></div></div></section></main>
<footer class="footer"><div class="wrap"><p>Ng Cheok Fung · Domestic tourism in Australia · October 2026</p><p class="ai-acknowledgement"><strong>Webpage development acknowledgement:</strong> <a href="https://chatgpt.com/">OpenAI ChatGPT</a> (2026) assisted with HTML, CSS and JavaScript for the webpage’s layout, styling and embedding functionality.</p></div></footer>
<script src="assets/readability.js" defer></script><script src="assets/vendor/vega.min.js" defer></script><script src="assets/vendor/vega-lite.min.js" defer></script><script src="assets/vendor/vega-embed.min.js" defer></script><script src="assets/charts.bundle.js" defer></script><script src="assets/app.js" defer></script></body></html>'''
(ROOT/'index.html').write_text(limit_prose_lines(page),encoding='utf-8')
(ROOT/'.nojekyll').touch()
print('Built index.html with 12 charts, one trip-type filter, four chapters and a source register.')
