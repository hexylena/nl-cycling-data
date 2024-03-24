import json
import json
# convert overpass turbo into real geojson for us.
import tqdm
import gzip

print('Loading holland.turbojson')
with gzip.open('holland.turbojson.gz', 'r') as handle:
    data = json.load(handle)

print('Loading holland.nodes.turbojson')
with open('holland.nodes.turbojson', 'r') as handle:
    nodes = json.load(handle)

n = []
w = []

refs = [
    # [lat, lon, from-to]
]

for e in tqdm.tqdm(data['elements']):
    if 'tags' in e and 'type' in e['tags']:
        if e['tags']['type'] == 'route':
            w.append({
                "type": "Feature",
                "geometry": {
                    "type": "MultiLineString",
                    "coordinates": [
                        [[z['lon'], z['lat']] for z in q.get('geometry', [])]
                        for q in
                        e['members']
                    ]
                },
                "properties": e['tags']
            })

for node in tqdm.tqdm(nodes['elements']):
    if 'lon' not in node:
        continue
    n.append({
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [
                node['lon'],
                node['lat'],
            ]
        },
        "properties": node['tags']
    })

print("Saving ways")
with open('geojson.way.js', 'w') as handle:
    handle.write("const gw = ")
    json.dump(w, handle)

with open('geojson.way.geojson', 'w') as handle:
    json.dump(w, handle)

print("Saving nodes")
with open('geojson.node.js', 'w') as handle:
    handle.write("const gn = ")
    json.dump(n, handle)

with open('geojson.node.geojson', 'w') as handle:
    json.dump(n, handle)

# import pprint
# pprint.pprint(refs)
