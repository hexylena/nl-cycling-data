import json

with open('holland.geojson', 'r') as handle:
    data = json.load(handle)

out = []

for e in data['elements']:
    # print('===')
    # print(len(e['members']))
    # print(json.dumps(e['members'], indent=2))
    # print('===')
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
