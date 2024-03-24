# fietsroutenetwerk data

an attempt to reconstruct the actual network from fietsroutenetwerk data.

the graphs in OSM are overly complicated, the graphs in the apps are all closed/inaccessible.

you can fetch data:

```bash
bash fetch.sh
# fetches dh.geojson, dh.nodes.geojson
# fetches holland.geojson, holland.nodes.geojson
```

the Hague data is a good representative test case of all the weirdness in the data.

it's not actually geojson, that's a lie. it's the overpass turbo json format which can be converted.

```bash
python process.py # converts to geojson.{way,node}.js for rendering
```

and there's

```bash
python extract.py # extracts the actual network
```

that also outputs an `rd_boxes.geojson` which represent like 80m x 80m boxes around the nodes as a way to roughly measure distance between nodes. And also stores a `holland.gexf` graph with weights.
