import json
import json
# convert overpass turbo into real geojson for us.
import tqdm
import gzip

# centimeters
PRECISION = 6
# half a meter or so
PRECISION = 5
# A couple meters
PRECISION = 4

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
                        [
                            [
                                round(z['lon'], PRECISION), 
                                round(z['lat'], PRECISION)
                            ] 
                            for z in q.get('geometry', [])
                        ]
                        for q in
                        e['members']
                    ]
                },
                "properties": {
                    "ref": e['tags'].get('ref', ''),
                }
            })

for node in tqdm.tqdm(nodes['elements']):
    if 'lon' not in node:
        continue
    n.append({
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [
                round(node['lon'], PRECISION),
                round(node['lat'], PRECISION)
            ]
        },
        "properties": {
            "rcn_ref": node['tags'].get('rcn_ref', '')
        }
    })

print("Saving ways")
with open('geojson.way.js', 'w') as handle:
    handle.write("const gw = ")
    json.dump(w, handle, separators=(',', ':'))

with open('geojson.way.geojson', 'w') as handle:
    json.dump(w, handle, separators=(',', ':'))

print("Saving nodes")
with open('geojson.node.js', 'w') as handle:
    handle.write("const gn = ")
    json.dump(n, handle, separators=(',', ':'))

with open('geojson.node.geojson', 'w') as handle:
    json.dump(n, handle, separators=(',', ':'))

# import pprint
# pprint.pprint(refs)
