"""Build original, readable Vega-Lite/Vega specifications from verified data."""
from pathlib import Path
import json, copy
from chart_tooltips import add_tooltips
ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'chart-specs'
OUT.mkdir(exist_ok=True)

def read(name):
    return json.loads((ROOT / 'data' / name).read_text())
N = read('national.json')
S = read('state-history.json')
L = read('latest-states.json')
G = read('australia-states.geojson')['features']
P = read('purpose.json')
EXP = read('expense-groups.json')
WF = read('waterfall.json')
TEAL = '#17665b'
INK = '#243b3a'
GOLD = '#bc8246'
BLUE = '#486b99'
GREY = '#afb9b5'
STATE_ORDER = ['New South Wales', 'Victoria', 'Queensland', 'Western Australia', 'South Australia', 'Tasmania', 'Australian Capital Territory', 'Northern Territory']
ABBR_ORDER = ['NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'ACT', 'NT']
COLOURS = ['#17665b', '#b77636', '#526ca2', '#746080', '#8a793b', '#a85b63', '#5c878c', '#707570']
CONFIG = {'background': 'transparent', 'font': 'Arial', 'view': {'stroke': None}, 'axis': {'labelFontSize': 12, 'titleFontSize': 12, 'titleFontWeight': 'normal', 'labelColor': '#425753', 'titleColor': '#425753', 'gridColor': '#e3e8e1', 'domain': False, 'tickColor': '#c5cec7', 'labelPadding': 7, 'titlePadding': 13}, 'legend': {'labelFontSize': 12, 'titleFontSize': 12, 'labelColor': '#425753', 'titleColor': '#425753', 'orient': 'bottom', 'titleFontWeight': 'normal', 'titleLimit': 400, 'labelLimit': 210, 'padding': 8}, 'text': {'font': 'Arial', 'color': INK}}
SPECS = {}
META = []

def save(i, slug, spec, title, idiom, advanced, question, rationale, wide=False):
    if 'vega/v5' in spec.get('$schema', ''):
        def set_text_fonts(marks):
            for mark in marks:
                if mark.get('type') == 'text':
                    mark.setdefault('encode', {}).setdefault('update', {})['font'] = {'value': 'Arial, Helvetica, sans-serif'}
                set_text_fonts(mark.get('marks', []))
        set_text_fonts(spec.get('marks', []))
    add_tooltips(i, spec, L)
    key = f'{i:02d}-{slug}'
    spec.setdefault('$schema', 'https://vega.github.io/schema/vega-lite/v5.json')
    spec.setdefault('description', question + ' ' + rationale)
    if 'facet' not in spec:
        spec.setdefault('width', 960 if wide else 480)
        spec.setdefault('height', 290)
    spec.setdefault('config', copy.deepcopy(CONFIG))
    spec.setdefault('padding', 10)
    spec.setdefault('autosize', {'type': 'fit-x', 'contains': 'padding', 'resize': True})
    (OUT / (key + '.json')).write_text(json.dumps(spec, ensure_ascii=False, indent=2) + '\n')
    SPECS[key] = spec
    META.append({'id': key, 'number': i, 'title': title, 'idiom': idiom, 'advanced': advanced, 'map_number': {4: 1, 5: 2, 11: 3}.get(i), 'question': question, 'rationale': rationale, 'wide': wide})

def dataset(values):
    return {'values': copy.deepcopy(values)}
national = []
for r in N:
    for m, label, raw in [('trips_index', 'Trips', 'trips_m'), ('nights_index', 'Nights', 'nights_m'), ('spend_index', 'Spending', 'spend_b')]:
        national.append({'year': r['year'], 'metric': label, 'index': r[m], 'raw': r[raw], 'units': 'AUD billion' if label == 'Spending' else 'million', 'method': r['method']})
spec = {'data': dataset(national), 'height': 310, 'layer': [{'data': dataset([{'level': 100}]), 'mark': {'type': 'rule', 'color': '#8f9e96', 'strokeDash': [5, 5]}, 'encoding': {'y': {'field': 'level', 'type': 'quantitative'}}}, {'data': dataset([{'year': 2024.5}]), 'mark': {'type': 'rule', 'color': '#aab6b0', 'strokeDash': [2, 4]}, 'encoding': {'x': {'field': 'year', 'type': 'quantitative'}}}, {'mark': {'type': 'line', 'strokeWidth': 3, 'point': {'filled': True, 'size': 55}}, 'encoding': {'x': {'field': 'year', 'type': 'quantitative', 'scale': {'domain': [2019, 2026.7], 'zero': False}, 'axis': {'title': None, 'format': 'd', 'tickMinStep': 1, 'grid': False, 'values': list(range(2019, 2027))}}, 'y': {'field': 'index', 'type': 'quantitative', 'scale': {'domain': [0, 185]}, 'axis': {'title': 'Index · June quarter 2019 = 100', 'values': [0, 50, 100, 150]}}, 'color': {'field': 'metric', 'type': 'nominal', 'scale': {'domain': ['Trips', 'Nights', 'Spending'], 'range': [TEAL, GOLD, BLUE]}, 'legend': None}}}, {'transform': [{'filter': 'datum.year === 2026'}], 'mark': {'type': 'text', 'align': 'left', 'dx': 10, 'dy': {'expr': "datum.metric === 'Trips' ? 7 : datum.metric === 'Nights' ? -6 : 0"}, 'fontSize': 12, 'fontWeight': 'bold'}, 'encoding': {'x': {'field': 'year', 'type': 'quantitative'}, 'y': {'field': 'index', 'type': 'quantitative'}, 'text': {'field': 'metric'}, 'color': {'field': 'metric', 'scale': {'domain': ['Trips', 'Nights', 'Spending'], 'range': [TEAL, GOLD, BLUE]}, 'legend': None}}}]}
save(1, 'national-trend', spec, 'Spending has grown much faster than trip numbers', 'Indexed line chart', False, 'How do trips, nights and nominal spending compare with the same quarter in 2019?', 'Line marks show ordered years. A shared index baseline enables comparison without mixing raw units. The dotted division marks the transition from revised backcast estimates to DoTS.', True)
pairs = []
for r in L:
    old = next((x for x in S if x['state'] == r['state'] and x['year'] == 2019))
    pairs.append({'state': r['state'], 'label': 'ACT' if r['abbr'] == 'ACT' else r['state'], 'old': old['trips_m'], 'new': r['trips_m'], 'change': r['trip_change_2019']})
spec = {'data': dataset(pairs), 'height': 290, 'encoding': {'y': {'field': 'label', 'type': 'nominal', 'sort': [s if s != 'Australian Capital Territory' else 'ACT' for s in STATE_ORDER], 'axis': {'title': None, 'labelLimit': 220, 'labelFontSize': 11}}}, 'layer': [{'mark': {'type': 'rule', 'strokeWidth': 3, 'color': '#bbc7bf'}, 'encoding': {'x': {'field': 'old', 'type': 'quantitative', 'axis': {'title': 'Overnight visits · million'}, 'scale': {'domain': [0, 10]}}, 'x2': {'field': 'new'}}}, {'mark': {'type': 'point', 'filled': False, 'color': '#8d9b94', 'size': 100, 'strokeWidth': 2}, 'encoding': {'x': {'field': 'old', 'type': 'quantitative'}}}, {'mark': {'type': 'point', 'filled': True, 'color': TEAL, 'size': 85}, 'encoding': {'x': {'field': 'new', 'type': 'quantitative'}}}]}
save(2, 'destination-change', spec, 'Destinations have recovered at different speeds', 'Connected dot plot', False, 'Which destinations gained overnight visits between June quarters 2019 and 2026?', 'Two points on a common horizontal scale encode the two periods. The connecting rule reveals direction and magnitude of change more directly than separate bars.')
spec = {'data': dataset(S), 'height': 290, 'mark': {'type': 'rect', 'cornerRadius': 2}, 'encoding': {'x': {'field': 'year', 'type': 'ordinal', 'axis': {'title': None, 'labelAngle': 0}}, 'y': {'field': 'abbr', 'type': 'nominal', 'sort': ABBR_ORDER, 'axis': {'title': None}}, 'color': {'field': 'trip_change_2019', 'type': 'quantitative', 'scale': {'domain': [-60, 0, 30], 'range': ['#b36a3d', '#f1f1e9', '#1b7565'], 'clamp': True}, 'legend': {'type': 'gradient', 'title': 'Change from June 2019 (%)',
                'direction': 'horizontal', 'values': [-60, 0, 30],
                'gradientLength': {'expr': 'min(300, max(180, width - 24))'},
                'gradientThickness': 20,
                'gradientStrokeColor': '#8b9b91', 'gradientStrokeWidth': 0.7,
                'labelOffset': 6, 'labelFontSize': 12,
                'labelExpr': "datum.value === 0 ? '0%' : format(datum.value, '+.0f') + '%'",
                'titlePadding': 10, 'offset': 16}}}}
save(3, 'recovery-heatmap', spec, 'The 2020 interruption was uneven', 'Heatmap', True, 'When did each destination fall below or rise above its own June 2019 level?', 'Rows and columns position states and years. A diverging colour scale centred at zero distinguishes losses from gains. Normalising each state prevents populous states from dominating every cell.')
projection = {'type': 'conicEqualArea', 'rotate': [-134, 0, 0], 'parallels': [-18, -36], 'center': [0, -28]}
labels = copy.deepcopy(L)
for r in labels:
    r['label_lon'], r['label_lat'] = (r['lon'], r['lat'])
    if r['abbr'] == 'ACT':
        r['label_lon'], r['label_lat'] = (154, -36.5)
    if r['abbr'] == 'VIC':
        r['label_lat'] = -38.1
spec = {'height': 340, 'projection': projection, 'layer': [{'data': dataset(G), 'mark': {'type': 'geoshape', 'fill': '#e3e8df', 'stroke': '#ffffff', 'strokeWidth': 1.2}}, {'data': dataset(L), 'mark': {'type': 'circle', 'fill': TEAL, 'fillOpacity': 0.76, 'stroke': 'white', 'strokeWidth': 1.1}, 'encoding': {'longitude': {'field': 'lon', 'type': 'quantitative'}, 'latitude': {'field': 'lat', 'type': 'quantitative'}, 'size': {'field': 'trips_m', 'type': 'quantitative', 'scale': {'domain': [0, 10], 'range': [0, 2200]}, 'legend': {'title': 'Visits · million', 'values': [2, 5, 9]}}}}, {'data': dataset([{'lon': 149.12, 'lat': -35.31, 'lon2': 154, 'lat2': -36.5}]), 'mark': {'type': 'rule', 'color': '#73867e'}, 'encoding': {'longitude': {'field': 'lon'}, 'latitude': {'field': 'lat'}, 'longitude2': {'field': 'lon2'}, 'latitude2': {'field': 'lat2'}}}, {'data': dataset(labels), 'mark': {'type': 'text', 'fontSize': 11, 'fontWeight': 'bold', 'color': INK, 'dy': -3}, 'encoding': {'longitude': {'field': 'label_lon', 'type': 'quantitative'}, 'latitude': {'field': 'label_lat', 'type': 'quantitative'}, 'text': {'field': 'abbr'}}}]}
save(4, 'visits-map', spec, 'Most overnight visits go to the eastern states', 'Proportional symbol map', True, 'Where are overnight visits concentrated in June quarter 2026?', 'Circle area, not radius, is proportional to visits. Symbols at interior state anchors locate aggregate counts without implying that visits occurred at those exact points. An Australian conic equal-area projection preserves relative geographic areas.')
map_values = []
for f in G:
    v = copy.deepcopy(f)
    r = next((r for r in L if r['state'] == v['properties']['state']))
    v['properties'].update({k: r[k] for k in ['nights_per_resident', 'nights_m', 'population']})
    map_values.append(v)
spec = {'height': 340, 'projection': projection, 'layer': [{'data': dataset(map_values), 'mark': {'type': 'geoshape', 'stroke': 'white', 'strokeWidth': 1.2}, 'encoding': {'color': {'field': 'properties.nights_per_resident', 'type': 'quantitative', 'scale': {'domain': [0, 5], 'range': ['#edf2e5', '#17665b']}, 'legend': {'type': 'gradient', 'title': 'Visitor nights per resident',
                'direction': 'horizontal', 'values': [0, 1, 2, 3, 4, 5],
                'gradientLength': {'expr': 'min(300, max(180, width - 24))'},
                'gradientThickness': 20,
                'gradientStrokeColor': '#8b9b91', 'gradientStrokeWidth': 0.7,
                'labelOffset': 6, 'labelFontSize': 12,
                'format': '.0f',
                'titlePadding': 10, 'offset': 16}}}}, {'data': dataset([{'lon': 149.12, 'lat': -35.31, 'lon2': 154, 'lat2': -36.5}]), 'mark': {'type': 'rule', 'color': '#526a60'}, 'encoding': {'longitude': {'field': 'lon'}, 'latitude': {'field': 'lat'}, 'longitude2': {'field': 'lon2'}, 'latitude2': {'field': 'lat2'}}}, {'data': dataset(labels), 'mark': {'type': 'text', 'fontSize': 11, 'fontWeight': 'bold', 'stroke': '#ffffff', 'strokeWidth': 2.5}, 'encoding': {'longitude': {'field': 'label_lon'}, 'latitude': {'field': 'label_lat'}, 'text': {'field': 'abbr'}}}, {'data': dataset(labels), 'mark': {'type': 'text', 'fontSize': 11, 'fontWeight': 'bold', 'color': INK}, 'encoding': {'longitude': {'field': 'label_lon'}, 'latitude': {'field': 'label_lat'}, 'text': {'field': 'abbr'}}}]}
save(5, 'tourism-intensity-map', spec, 'Small populations change the picture', 'Choropleth map', True, 'Which destinations host the most overnight visitor nights relative to their population?', 'Sequential colour luminance encodes a standardised rate. TRA visitor nights are divided by ABS resident population. This measures destination activity relative to population, not the likelihood that a local resident travels.')
spec = {'data': dataset(P), 'height': 265, 'params': [{'name': 'tripKind', 'value': 'Overnight', 'bind': {'input': 'select', 'options': ['Overnight', 'Day trip'], 'name': 'Trip type: '}}], 'transform': [{'filter': 'datum.trip_type === tripKind'}], 'mark': {'type': 'bar', 'cornerRadiusEnd': 3}, 'encoding': {'y': {'field': 'label', 'type': 'nominal', 'sort': ['Holiday', 'Friends / relatives', 'Business', 'Other'], 'axis': {'title': None, 'labelLimit': 150}}, 'yOffset': {'field': 'year', 'sort': [2025, 2026]}, 'x': {'field': 'trips_m', 'type': 'quantitative', 'axis': {'title': 'Trips reporting this visit reason · million'}}, 'color': {'field': 'year', 'type': 'ordinal', 'scale': {'domain': [2025, 2026], 'range': [GREY, TEAL]}, 'legend': {'title': 'June quarter'}}}}
spec['encoding']['y']['axis']['labelLimit'] = 240
save(6, 'travel-purpose', spec, 'Holiday and business travel moved in opposite directions', 'Grouped bar chart', False, 'How did holiday and business trips change between June quarters 2025 and 2026?', 'Aligned bar lengths compare the two years directly. The local dropdown compares day trips and overnight trips without replacing a major story section. Counts are not forced into misleading percentage shares.', True)
spec = {'data': dataset(read('waffle.json')), 'width': 285, 'height': 285, 'mark': {'type': 'rect', 'cornerRadius': 3, 'stroke': '#ffffff', 'strokeWidth': 2.2}, 'encoding': {'x': {'field': 'column', 'type': 'ordinal', 'axis': None}, 'y': {'field': 'row', 'type': 'ordinal', 'axis': None}, 'color': {'field': 'type', 'type': 'nominal', 'scale': {'domain': ['Intrastate', 'Interstate'], 'range': [TEAL, GOLD]}, 'legend': {'title': None}}}}
waffle_cells = {'mark': spec.pop('mark'), 'encoding': spec.pop('encoding')}
intrastate = next(r for r in read('travel-mix.json') if r['type'] == 'Intrastate')
trip_total = sum(r['trips'] for r in read('travel-mix.json'))
callout = {'type': 'Intrastate', 'share': intrastate['share'],
           'trips_m': intrastate['trips'] / 1000,
           'headline': f"{intrastate['share']:.1f}% of trips",
           'detail': 'stay within their home state',
           'counts': f"{intrastate['trips']/1000:.2f}m of {trip_total/1000:.2f}m overnight trips"}
spec['layer'] = [waffle_cells,
    {'data': dataset([callout]), 'mark': {'type': 'rule', 'stroke': '#fffefa', 'strokeWidth': 1.4},
     'encoding': {'x': {'value': 77}, 'y': {'value': 54},
                  'x2': {'value': 137}, 'y2': {'value': 108}}},
    {'data': dataset([callout]), 'mark': {'type': 'rect', 'fill': '#fffefa', 'fillOpacity': 0.94,
        'x': {'expr': 'width * 0.04'}, 'x2': {'expr': 'width * 0.96'},
        'y': {'expr': 'height * 0.37'}, 'y2': {'expr': 'height * 0.71'}}}
]
for field_name, y, size, weight in [('headline', 0.45, 23, 'bold'), ('detail', 0.55, 15, 'normal'), ('counts', 0.64, 12, 'normal')]:
    spec['layer'].append({'data': dataset([callout]),
        'mark': {'type': 'text', 'align': 'left', 'baseline': 'middle', 'fontSize': size,
                 'fontWeight': weight, 'color': INK, 'x': {'expr': 'width * 0.08'}, 'y': {'expr': f'height * {y}'}},
        'encoding': {'text': {'field': field_name}}})
save(7, 'within-state-waffle', spec, 'Three in four overnight trips stay within one state', 'Waffle chart', True, 'How common is crossing a state border on an overnight trip in June quarter 2026?', 'One hundred equal area squares make a simple proportion tangible. Squares round the current share to whole percentage points; the caption states the precise percentages.')
spec = {'data': dataset(L), 'height': 300, 'layer': [{'mark': {'type': 'point', 'filled': True, 'color': TEAL, 'size': 110, 'opacity': 0.85}, 'encoding': {'x': {'field': 'average_nights', 'type': 'quantitative', 'scale': {'domain': [0, 4.8]}, 'axis': {'title': 'Average nights per destination visit'}}, 'y': {'field': 'spend_per_visit', 'type': 'quantitative', 'scale': {'domain': [0, 1900]}, 'axis': {'title': 'Allocated spending per visit · AUD', 'format': ',.0f'}}}}, {'mark': {'type': 'text', 'dy': {'expr': "datum.abbr === 'QLD' || datum.abbr === 'NSW' ? 15 : -13"}, 'dx': {'expr': "datum.abbr === 'TAS' ? 9 : 0"}, 'fontSize': 11, 'fontWeight': 'bold'}, 'encoding': {'x': {'field': 'average_nights', 'type': 'quantitative'}, 'y': {'field': 'spend_per_visit', 'type': 'quantitative'}, 'text': {'field': 'abbr'}}}]}
save(8, 'length-and-spending', spec, 'Longer stays come with different spending levels', 'Scatterplot', False, 'How do average stay length and allocated spending per destination visit differ?', 'Position on two quantitative axes reveals the relationship without requiring statistical knowledge. Each point is one state or territory. The ratios use matching state-level totals, not mismatched purpose definitions.')
spending_items = copy.deepcopy(EXP)
for row in spending_items:
    row['label'] = f"A${row['value_b']:.2f}bn"
spec = {
    'data': dataset(spending_items), 'height': 300,
    'encoding': {
        'y': {'field': 'group', 'type': 'nominal',
              'sort': [r['group'] for r in sorted(EXP, key=lambda r: r['value_b'], reverse=True)],
              'axis': {'title': None, 'labelLimit': 120}},
        'x': {'field': 'value_b', 'type': 'quantitative',
              'scale': {'domain': [0, 9.8]},
              'axis': {'title': 'Overnight spending · AUD billion', 'values': [0, 2, 4, 6, 8]}}
    },
    'layer': [
        {'mark': {'type': 'bar', 'size': 23, 'cornerRadiusEnd': 3},
         'encoding': {'color': {'condition': {'test': "datum.group === 'Accommodation'", 'value': TEAL}, 'value': '#93afa3'}}},
        {'mark': {'type': 'text', 'align': 'left', 'dx': 7, 'fontSize': 11, 'color': INK},
         'encoding': {'text': {'field': 'label'}}}
    ]
}
save(9, 'spending-categories', spec, 'Accommodation takes the largest single spending share',
     'Sorted bar chart', False,
     'How do overnight spending categories compare in June quarter 2026?',
     'Sorted bar lengths compare flat spending categories on a common zero baseline. Direct labels give spending and share; no artificial hierarchy is implied.', True)
spec = {'data': dataset(WF), 'height': 290, 'encoding': {'x': {'field': 'group', 'type': 'nominal', 'sort': {'field': 'order'}, 'axis': {'title': None, 'labelAngle': -25, 'labelLimit': 120}}}, 'layer': [{'mark': {'type': 'bar', 'size': 50, 'cornerRadius': 2}, 'encoding': {'y': {'field': 'start', 'type': 'quantitative', 'axis': {'title': 'Cumulative change · AUD million'}}, 'y2': {'field': 'end'}, 'color': {'field': 'kind', 'scale': {'domain': ['Increase', 'Decrease', 'Net change'], 'range': [TEAL, GOLD, BLUE]}, 'legend': {'title': None}}}}, {'mark': {'type': 'text', 'dy': -10, 'fontSize': 12}, 'encoding': {'y': {'field': 'end', 'type': 'quantitative'}, 'text': {'field': 'change', 'format': '+.0f'}}}]}
spec['encoding']['x']['axis']['labelLimit'] = 220
save(10, 'spending-waterfall', spec, 'Gains and cuts add up to A$540 million more', 'Waterfall chart', True, 'Which expenditure categories explain the change between June quarters 2025 and 2026?', 'Floating bars accumulate signed contributions to the net spending change. The common money unit makes contributions additive, and a separate final bar verifies their net effect.', True)
dots = read('spending-dots.json')
state_features = copy.deepcopy(G)
for f in state_features:
    r = next((r for r in L if r['state'] == f['properties']['state']))
    f['properties']['spend_b'] = r['spend_b']
map_labels = copy.deepcopy(L)
for r in map_labels:
    if r['abbr'] == 'VIC':
        r['lat'] = -38.5
    if r['abbr'] == 'TAS':
        r['lat'] = -43.6
spec = {'$schema': 'https://vega.github.io/schema/vega/v5.json', 'width': 480, 'height': 390, 'padding': 8, 'data': [{'name': 'states', 'values': state_features}, {'name': 'actState', 'source': 'states', 'transform': [{'type': 'filter', 'expr': "datum.properties.abbr === 'ACT'"}]}, {'name': 'dots', 'values': dots}, {'name': 'mainDots', 'source': 'dots', 'transform': [{'type': 'filter', 'expr': "datum.abbr !== 'ACT'"}, {'type': 'geopoint', 'projection': 'mainProjection', 'fields': ['lon', 'lat'], 'as': ['x', 'y']}]}, {'name': 'actDots', 'source': 'dots', 'transform': [{'type': 'filter', 'expr': "datum.abbr === 'ACT'"}, {'type': 'geopoint', 'projection': 'actProjection', 'fields': ['lon', 'lat'], 'as': ['x', 'y']}]}, {'name': 'labels', 'values': map_labels, 'transform': [{'type': 'filter', 'expr': "datum.abbr !== 'ACT'"}, {'type': 'geopoint', 'projection': 'mainProjection', 'fields': ['lon', 'lat'], 'as': ['x', 'y']}]}, {'name': 'actAnchor', 'values': [{'lon': 149.12, 'lat': -35.31}], 'transform': [{'type': 'geopoint', 'projection': 'mainProjection', 'fields': ['lon', 'lat'], 'as': ['x', 'y']}]}], 'projections': [{'name': 'mainProjection', **projection, 'fit': {'signal': "data('states')"}, 'extent': {'signal': '[[4, 12], [width-112, height-60]]'}}, {'name': 'actProjection', **projection, 'fit': {'signal': "data('actState')"}, 'extent': [[10, 12], [82, 105]]}], 'marks': [{'type': 'shape', 'from': {'data': 'states'}, 'encode': {'update': {'fill': {'value': '#e8ece3'}, 'stroke': {'value': '#b5c0b4'}, 'strokeWidth': {'value': 0.7}}}, 'transform': [{'type': 'geoshape', 'projection': 'mainProjection'}]}, {'type': 'symbol', 'from': {'data': 'mainDots'}, 'encode': {'update': {'x': {'field': 'x'}, 'y': {'field': 'y'}, 'size': {'value': 9}, 'fill': {'value': TEAL}, 'fillOpacity': {'value': 0.85}}}}, {'type': 'text', 'from': {'data': 'labels'}, 'encode': {'update': {'x': {'field': 'x'}, 'y': {'field': 'y'}, 'text': {'field': 'abbr'}, 'fontSize': {'value': 11}, 'fontWeight': {'value': 'bold'}, 'align': {'value': 'center'}, 'baseline': {'value': 'middle'}, 'stroke': {'value': '#f7f6ee'}, 'strokeWidth': {'value': 3}}}}, {'type': 'text', 'from': {'data': 'labels'}, 'encode': {'update': {'x': {'field': 'x'}, 'y': {'field': 'y'}, 'text': {'field': 'abbr'}, 'fontSize': {'value': 11}, 'fontWeight': {'value': 'bold'}, 'align': {'value': 'center'}, 'baseline': {'value': 'middle'}, 'fill': {'value': INK}}}}, {'type': 'rule', 'from': {'data': 'actAnchor'}, 'encode': {'update': {'x': {'field': 'x'}, 'y': {'field': 'y'}, 'x2': {'signal': 'width-100'}, 'y2': {'signal': 'height/2'}, 'stroke': {'value': '#8c9e92'}, 'strokeDash': {'value': [3, 3]}}}}, {'type': 'group', 'encode': {'update': {'x': {'signal': 'width-100'}, 'y': {'signal': 'height/2-60'}, 'width': {'value': 92}, 'height': {'value': 126}, 'fill': {'value': '#fffefa'}, 'stroke': {'value': '#c5cfc3'}}}, 'marks': [{'type': 'shape', 'from': {'data': 'actState'}, 'encode': {'update': {'fill': {'value': '#e8ece3'}, 'stroke': {'value': '#8c9e92'}, 'strokeWidth': {'value': 0.7}}}, 'transform': [{'type': 'geoshape', 'projection': 'actProjection'}]}, {'type': 'symbol', 'from': {'data': 'actDots'}, 'encode': {'update': {'x': {'field': 'x'}, 'y': {'field': 'y'}, 'size': {'value': 9}, 'fill': {'value': TEAL}}}}, {'type': 'text', 'encode': {'update': {'x': {'value': 46}, 'y': {'value': -8}, 'align': {'value': 'center'}, 'text': {'value': 'ACT · enlarged'}, 'fontSize': {'value': 11}, 'fontWeight': {'value': 'bold'}, 'fill': {'value': INK}}}}, {'type': 'text', 'encode': {'update': {'x': {'value': 46}, 'y': {'value': 117}, 'align': {'value': 'center'}, 'text': {'value': '5 dots · A$0.50bn'}, 'fontSize': {'value': 10}, 'fill': {'value': INK}}}}]}, {'type': 'symbol', 'encode': {'update': {'x': {'value': 12}, 'y': {'signal': 'height-23'}, 'size': {'value': 9}, 'fill': {'value': TEAL}}}}, {'type': 'text', 'encode': {'update': {'x': {'value': 24}, 'y': {'signal': 'height-23'}, 'baseline': {'value': 'middle'}, 'text': {'value': '1 dot ≈ A$100 million'}, 'fontSize': {'value': 12}, 'fill': {'value': INK}}}}]}
save(11, 'spending-dot-density-map', spec, 'A dot for every A$100 million', 'Dot-density map', True, 'How is allocated overnight spending distributed between Australian states and territories?', 'The number of equal-sized dots encodes state expenditure on a geographic basemap. Each dot represents approximately AUD 100 million, with whole-dot counts rounded per state. Positions are allocated within state boundaries, not observed spending locations. An equal-area projection preserves geographic area, and the enlarged ACT inset is explicitly identified.', True)
state_trends = copy.deepcopy(S)
for row in state_trends:
    row['growth'] = row['spend_index'] - 100
    row['growth_label'] = f"{row['growth']:+.0f}%"
spec = {
    'data': dataset(state_trends), 'columns': 4, 'spacing': 18,
    'facet': {'field': 'state', 'type': 'nominal', 'sort': STATE_ORDER,
              'header': {'title': None, 'labelFont': 'Arial', 'labelFontSize': 12,
                         'labelFontWeight': 'bold', 'labelLimit': 190}},
    'spec': {
        'width': 165, 'height': 115,
        'encoding': {
            'x': {'field': 'year', 'type': 'quantitative',
                  'scale': {'domain': [2019, 2027], 'zero': False},
                  'axis': {'title': None, 'values': [2019, 2026], 'format': 'd', 'grid': False}},
            'y': {'field': 'spend_index', 'type': 'quantitative',
                  'scale': {'domain': [0, 230]},
                  'axis': {'title': None, 'values': [0, 100, 200]}}
        },
        'layer': [
            {'mark': {'type': 'area', 'color': TEAL, 'opacity': 0.09}},
            {'data': dataset([{'baseline': 100}]),
             'mark': {'type': 'rule', 'color': '#8f9e96', 'strokeDash': [4, 4]},
             'encoding': {'x': {'datum': 2019, 'type': 'quantitative'}, 'x2': {'datum': 2027},
                          'y': {'datum': 100, 'type': 'quantitative'}}},
            {'data': dataset([{'boundary': 2024.5}]),
             'mark': {'type': 'rule', 'color': '#aab6b0', 'strokeDash': [2, 4]},
             'encoding': {'x': {'datum': 2024.5, 'type': 'quantitative'},
                          'y': {'datum': 0, 'type': 'quantitative'}, 'y2': {'datum': 230}}},
            {'mark': {'type': 'line', 'color': TEAL, 'strokeWidth': 2, 'point': {'filled': True, 'size': 22}}},
            {'transform': [{'filter': 'datum.year === 2026'}],
             'mark': {'type': 'text', 'align': 'right', 'dx': 0, 'dy': -12, 'fontSize': 11,
                      'fontWeight': 'bold', 'color': TEAL},
             'encoding': {'text': {'field': 'growth_label'}}}
        ]
    },
    'resolve': {'scale': {'x': 'shared', 'y': 'shared'}},
    'autosize': {'type': 'pad', 'contains': 'padding'}
}
# Keep reference-rule encodings independent of the time-series fields.
trend_encoding = spec['spec'].pop('encoding')
trend_encoding['y']['stack'] = None
for i in (0, 3, 4):
    spec['spec']['layer'][i]['encoding'] = {**copy.deepcopy(trend_encoding), **spec['spec']['layer'][i].get('encoding', {})}
save(12, 'state-spending-trends', spec, 'Spending recovered at different speeds across the states',
     'Small-multiple indexed line charts', False,
     'How has nominal overnight spending changed within each destination since June quarter 2019?',
     'Eight panels show actual spending trajectories, indexed to each destination’s 2019 value. Shared scales support comparison of proportional changes even when rankings remain unchanged. Dashed reference lines mark index 100 and the survey transition.', True)
(ROOT / 'assets' / 'charts.bundle.js').write_text('window.TOURISM_SPECS = ' + json.dumps(SPECS, ensure_ascii=False, separators=(',', ':')) + ';\n')
(ROOT / 'data' / 'chart-catalogue.json').write_text(json.dumps(META, ensure_ascii=False, indent=2) + '\n')
print(f"Built {len(META)} charts; {sum((x['advanced'] for x in META))} advanced idioms; 3 map idioms.")
