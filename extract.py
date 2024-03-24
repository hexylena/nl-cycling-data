import json
# convert overpass turbo into real geojson for us.

with open('holland.geojson', 'r') as handle:
    data = json.load(handle)

with open('holland.nodes.geojson', 'r') as handle:
    nodes = json.load(handle)

out = []

refs = {
    # [lat, lon, from-to]
}

# First time through the data collect our nodes.
for node in nodes['elements']:
        k = f"{node['lon']},{node['lat']}"
        refs[k] = {
            'id': node['tags']['rcn_ref'],
            'refs': set()
        }

# Second time through deep search through the ways to find any overlaps.
for e in data['elements']:
    if e['tags']['type'] == 'route':
        for node in e['members']:
            for geo in node.get('geometry', []):
                k = f"{geo['lon']},{geo['lat']}"
                if k in refs:
                    q = set(e['tags']['ref'].split('-'))
                    q = q - {refs[k]['id']}
                    if len(q) == 0:
                        continue

                    refs[k]['refs'] |= q

import pprint
pprint.pprint(refs)

