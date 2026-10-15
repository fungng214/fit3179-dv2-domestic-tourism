"""Allocate fixed-value symbols to state polygons, not observed travel locations.

One dot represents approximately AUD 100 million. Whole-dot counts are rounded
per state; exact published expenditure remains in the source workbook.
Sampling longitude and sin(latitude) makes candidate placement uniform in
spherical surface area. A fixed seed keeps the display reproducible.
"""
from pathlib import Path
from collections import Counter
import json, math, random

ROOT=Path(__file__).resolve().parent
states=json.loads((ROOT/'data/latest-states.json').read_text())
features=json.loads((ROOT/'data/australia-states.geojson').read_text())['features']
DOT_VALUE_M=100

def inside_ring(x,y,ring):
    inside=False
    for a,b in zip(ring,ring[1:]):
        if (a[1]>y)!=(b[1]>y):
            crossing=(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]
            if x<crossing:inside=not inside
    return inside

def inside_geometry(x,y,geometry):
    polygons=geometry['coordinates'] if geometry['type']=='MultiPolygon' else [geometry['coordinates']]
    return any(inside_ring(x,y,p[0]) and not any(inside_ring(x,y,hole) for hole in p[1:]) for p in polygons)

dots=[];summary=[]
for i,state in enumerate(sorted(states,key=lambda r:r['abbr'])):
    feature=next(f for f in features if f['properties']['state']==state['state'])
    g=feature['geometry']
    points=[xy for poly in g['coordinates'] for ring in poly for xy in ring]
    xmin=min(x for x,y in points);xmax=max(x for x,y in points)
    ymin=min(y for x,y in points);ymax=max(y for x,y in points)
    count=math.floor(state['spend']/DOT_VALUE_M+.5)
    rng=random.Random(20261015+i)
    accepted=0;attempts=0
    while accepted<count:
        attempts+=1
        if attempts>100000:raise RuntimeError('Could not place dots in '+state['state'])
        lon=rng.uniform(xmin,xmax)
        lat=math.degrees(math.asin(rng.uniform(math.sin(math.radians(ymin)),math.sin(math.radians(ymax)))))
        if not inside_geometry(lon,lat,g):continue
        dots.append({'state':state['state'],'abbr':state['abbr'],'lon':lon,'lat':lat,
                     'spend_b':state['spend_b'],'dot_value_m':DOT_VALUE_M,'dot_count':count,
                     'placement':'Allocated within state; not an observed tourist or spending location'})
        accepted+=1
    assert abs(count*DOT_VALUE_M-state['spend'])<=DOT_VALUE_M/2
    summary.append({'state':state['state'],'abbr':state['abbr'],'spend_m':state['spend'],
                    'dots':count,'represented_spend_m':count*DOT_VALUE_M,
                    'rounding_difference_m':count*DOT_VALUE_M-state['spend']})

counts=Counter(d['state'] for d in dots)
assert all(counts[r['state']]==r['dots'] for r in summary)
for d in dots:
    f=next(f for f in features if f['properties']['state']==d['state'])
    assert inside_geometry(d['lon'],d['lat'],f['geometry'])
(ROOT/'data/spending-dots.json').write_text(json.dumps(dots,indent=2)+'\n')
(ROOT/'data/spending-dot-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(f'Validated {len(dots)} fixed-value dots across eight states and territories.')
