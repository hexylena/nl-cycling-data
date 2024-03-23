import json

with open('holland.geojson', 'r') as handle:
    data = json.load(handle)

out = []

refs = [
    # [lat, lon, from-to]
]

for e in data['elements']:
    # print('===')
    # print(len(e['members']))
    # print(json.dumps(e['members'], indent=2))
    # print('===')
    print(e['members'][0])
    print(e['members'][-1])
    refs.append([
        e['members'][0]['geometry'][0]['lat'],
        e['members'][0]['geometry'][0]['lon'],
        e['members'][0]['geometry'][-1]['lat'],
        e['members'][0]['geometry'][-1]['lon'],
        e['tags']['ref'],
    ])
    refs.append([
        e['members'][-1]['geometry'][0]['lat'],
        e['members'][-1]['geometry'][0]['lon'],
        e['members'][-1]['geometry'][-1]['lat'],
        e['members'][-1]['geometry'][-1]['lon'],
        e['tags']['ref'],
    ])
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

with open('geojson.js', 'w') as handle:
    handle.write("const gj = ")
    json.dump(out, handle)

import pprint
pprint.pprint(refs)
