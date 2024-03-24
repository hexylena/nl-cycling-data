import json
# convert overpass turbo into real geojson for us.

with open('holland.geojson', 'r') as handle:
    data = json.load(handle)

with open('holland.nodes.geojson', 'r') as handle:
    nodes = json.load(handle)

out = []

refs = [
    # [lat, lon, from-to]
]

for e in data['elements']:
    if e['tags']['type'] == 'route':
        out.append({
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

for node in nodes['elements']:
    out.append({
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [
                node['lon'],
                node['lat'],
            ]
        },
        "properties": e['tags']
    })

with open('geojson.js', 'w') as handle:
    handle.write("const gj = ")
    json.dump(out, handle)

# import pprint
# pprint.pprint(refs)
