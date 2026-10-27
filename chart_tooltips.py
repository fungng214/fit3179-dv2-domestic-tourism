"""Add concise, unit-labelled tooltips without changing chart filters or scales."""
from collections import Counter
import copy


def field(name, title, kind='quantitative', fmt=None):
    item = {'field': name, 'title': title, 'type': kind}
    if fmt is not None:
        item['format'] = fmt
    return item


PERIOD = field('period', 'Period', 'nominal')
STATE = field('state', 'Destination', 'nominal')


def add_periods(node, number):
    """Keep the period available in every mark's underlying data record."""
    if isinstance(node, dict):
        values = node.get('values')
        if isinstance(values, list):
            for row in values:
                if not isinstance(row, dict):
                    continue
                year = row.get('year')
                if isinstance(year, int):
                    period = f'April–June {year}'
                elif number == 2:
                    period = 'April–June 2019 and 2026'
                elif number == 10:
                    period = 'April–June 2026 minus April–June 2025'
                else:
                    period = 'April–June 2026'
                row['period'] = period
        for value in node.values():
            if isinstance(value, (dict, list)):
                add_periods(value, number)
    elif isinstance(node, list):
        for value in node:
            add_periods(value, number)


def encode_tooltip(layer, items):
    layer.setdefault('encoding', {})['tooltip'] = copy.deepcopy(items)


def add_tooltips(number, spec, latest_states):
    add_periods(spec, number)
    if number == 1:
        items = [PERIOD, field('metric', 'Measure', 'nominal'),
                 field('index', 'Index · 2019 = 100', fmt='.1f'),
                 field('raw', 'Published value', fmt='.2f'),
                 field('units', 'Unit', 'nominal'), field('method', 'Statistical series', 'nominal')]
        for layer in spec['layer'][2:]:
            encode_tooltip(layer, items)
    elif number == 2:
        encode_tooltip(spec, [STATE,
            field('old', 'June quarter 2019 visits · million', fmt='.2f'),
            field('new', 'June quarter 2026 visits · million', fmt='.2f'),
            field('change', 'Change since 2019 · %', fmt='+.1f')])
    elif number == 3:
        encode_tooltip(spec, [PERIOD, STATE, field('trips_m', 'Overnight visits · million', fmt='.2f'),
            field('trip_change_2019', 'Change from June 2019 · %', fmt='+.1f'),
            field('method', 'Statistical series', 'nominal')])
    elif number == 4:
        items = [PERIOD, STATE, field('trips_m', 'Overnight visits · million', fmt='.2f'),
                 field('nights_m', 'Visitor nights · million', fmt='.2f')]
        for index in (1, 3):
            encode_tooltip(spec['layer'][index], items)
        # State areas and the symbol/label show the same aggregate information.
        for feature in spec['layer'][0]['data']['values']:
            row = next(r for r in latest_states if r['state'] == feature['properties']['state'])
            feature['properties'].update({k: row[k] for k in ['trips_m', 'nights_m']})
        encode_tooltip(spec['layer'][0], [PERIOD, field('properties.state', 'Destination', 'nominal'),
            field('properties.trips_m', 'Overnight visits · million', fmt='.2f'),
            field('properties.nights_m', 'Visitor nights · million', fmt='.2f')])
    elif number == 5:
        def intensity(prefix=''):
            return [PERIOD, field(prefix+'state', 'Destination', 'nominal'),
                field(prefix+'nights_per_resident', 'Visitor nights per resident', fmt='.2f'),
                field(prefix+'nights_m', 'Visitor nights · million', fmt='.2f'),
                field(prefix+'population', 'Residents · 31 March 2026', fmt=',.0f')]
        encode_tooltip(spec['layer'][0], intensity('properties.'))
        for layer in spec['layer'][2:]:
            encode_tooltip(layer, intensity())
    elif number == 6:
        encode_tooltip(spec, [PERIOD, field('purpose', 'Visit reason', 'nominal'),
            field('trip_type', 'Trip type', 'nominal'), field('trips_m', 'Trips · million', fmt='.3f')])
    elif number == 7:
        encode_tooltip(spec, [PERIOD, field('type', 'Trip geography', 'nominal'),
            field('share', 'Share of overnight trips · %', fmt='.1f'),
            field('trips_m', 'Overnight trips · million', fmt='.2f')])
    elif number == 8:
        items = [PERIOD, STATE, field('average_nights', 'Average nights per visit', fmt='.2f'),
                 field('spend_per_visit', 'Allocated spending per visit · AUD', fmt=',.0f')]
        for layer in spec['layer']:
            encode_tooltip(layer, items)
    elif number == 9:
        encode_tooltip(spec, [PERIOD, field('group', 'Spending category', 'nominal'),
            field('value_b', 'Spending · AUD billion', fmt='.3f'),
            field('share', 'Share of spending · %', fmt='.1f'),
            field('items', 'Includes', 'nominal')])
    elif number == 10:
        encode_tooltip(spec, [PERIOD, field('group', 'Spending category', 'nominal'),
            field('change', 'Change · AUD million', fmt='+.1f'),
            field('end', 'Running change · AUD million', fmt='+.1f')])
    elif number == 11:
        counts = Counter(row['state'] for dataset in spec['data'] if dataset['name'] == 'dots'
                         for row in dataset['values'])
        for dataset in spec['data']:
            if dataset['name'] == 'states':
                for row in dataset['values']:
                    row['properties']['dot_count'] = counts[row['properties']['state']]
            elif dataset['name'] == 'labels':
                for row in dataset['values']:
                    row['dot_count'] = counts[row['state']]
        state_tip = {'signal': "{'Period':datum.period,'Destination':datum.properties.state,'Allocated spending (AUD billion)':format(datum.properties.spend_b,'.3f'),'Rounded dots in state':datum.properties.dot_count,'One dot':'Approximately A$100 million','Placement':'Allocated within the state; not observed spending locations'}"}
        dot_tip = {'signal': "{'Period':datum.period,'Destination':datum.state,'Allocated spending (AUD billion)':format(datum.spend_b,'.3f'),'Rounded dots in state':datum.dot_count,'One dot':'Approximately A$100 million','Placement':'Allocated within the state; not observed spending locations'}"}
        def annotate(marks):
            for mark in marks:
                data_name = mark.get('from', {}).get('data')
                if data_name in ('states', 'actState'):
                    mark['encode']['update']['tooltip'] = copy.deepcopy(state_tip)
                elif data_name in ('mainDots', 'actDots', 'labels'):
                    mark['encode']['update']['tooltip'] = copy.deepcopy(dot_tip)
                if 'marks' in mark:
                    annotate(mark['marks'])
        annotate(spec['marks'])
    elif number == 12:
        items = [PERIOD, STATE, field('spend_index', 'Index · 2019 = 100', fmt='.1f'),
                 field('growth', 'Change since 2019 · %', fmt='+.1f'),
                 field('spend_b', 'Allocated spending · AUD billion', fmt='.3f'),
                 field('method', 'Statistical series', 'nominal')]
        for i in (0, 3, 4):
            encode_tooltip(spec['spec']['layer'][i], items)
