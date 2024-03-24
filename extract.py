import json
import networkx as nx
import geopy.distance
import pyproj

CHUNK_DIST = 80
wg84 = pyproj.CRS("WGS84")
rd = pyproj.CRS("EPSG:28992")
transformer = pyproj.Transformer.from_crs(wg84, rd)
r_transformer = pyproj.Transformer.from_crs(rd, wg84)

# convert overpass turbo into real geojson for us.

with open('holland.geojson', 'r') as handle:
    data = json.load(handle)

with open('holland.nodes.geojson', 'r') as handle:
    nodes = json.load(handle)

def swap(x, y):
    return y, x
out = []

refs = {
    # [lat, lon, from-to]
}

rd_boxes = []

G = nx.Graph()

# First time through the data collect our nodes.
for node in nodes['elements']:
        k = f"{node['lon']},{node['lat']}"
        refs[k] = {
            'num': node['tags']['rcn_ref'],
            'id': node['id'],
            'refs': set(),
            'j': [],
        }
        G.add_node(node['id'], num=node['tags']['rcn_ref'], lon=node['lon'], lat=node['lat'])

def chunk(x, y, size=CHUNK_DIST):
    # Round both x and y to chunks of 50
    # e.g. (0, 0) -> (0, 0), 25, 25 -> (0, 0), 50, 50 -> (50, 50)
    return (int(x/size)*size, int(y/size)*size)

# Second time through deep search through the ways to find any overlaps.
for e in data['elements']:
    if e['tags']['type'] == 'route':
        # Start of a node
        matching_nodes = []
        all_nodes = []
        # TODO: generate subdivisions of lat/lon pairs with long distances between them.
        for node in e['members']:
            for geo in node.get('geometry', []):
                rd_coords = transformer.transform(geo['lat'], geo['lon'])
                all_nodes.append(chunk(*rd_coords))


                k = f"{geo['lon']},{geo['lat']}"
                if k in refs:
                    matching_nodes.append(k)

                    q = set(e['tags']['ref'].split('-'))
                    q = q - {refs[k]['id']}
                    if len(q) == 0:
                        continue
                    refs[k]['refs'] |= q

        # We have our set of all nodes, chunked into 50m chunks.
        sall = set(all_nodes)
        # We need to measure distance along these chunks in a sensible way, what if e.g.
        # the chunks are arranged like:
        # xxx
        # x..
        # xxx
        # How do we measure distance covered by the Xs? do we just sum them?????
        distance = len(sall) * CHUNK_DIST
        for n in sall:
            x0 = r_transformer.transform(*n)
            x1 = r_transformer.transform(n[0]+CHUNK_DIST, n[1])
            x2 = r_transformer.transform(n[0], n[1]+CHUNK_DIST)
            x3 = r_transformer.transform(n[0]+CHUNK_DIST, n[1]+CHUNK_DIST)

            rd_boxes.append({
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        swap(*x0),
                        swap(*x1),
                        swap(*x3),
                        swap(*x2),
                    ]]
                },
                # "properties": e['tags']
            })

        matching_nodes = list(set(matching_nodes))
        differently_numbered_nodes = set([refs[m]['num'] for m in matching_nodes])
        if len(differently_numbered_nodes) == 0:
            pass
            # print("Route without nodes")
        elif len(differently_numbered_nodes) == 1:
            pass
            # print("Route deadends")
        elif len(differently_numbered_nodes) == 2:
            if e['id'] == "1163378":
                print(distance)
            G.add_edge(
                refs[matching_nodes[0]]['id'], 
                refs[matching_nodes[1]]['id'],
                id=e['id'],
                distance=distance,
                weight=100 / distance,
                **e['tags']
            )
            # print([refs[m] for m in matching_nodes])
        else:
            pass
            # print("Route with multiple nodes how do i handle this")

# import pprint
# pprint.pprint(refs)

# Remove isolates
G.remove_nodes_from(list(nx.isolates(G)))

pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility
import matplotlib.pyplot as plt

# nodes
nx.draw_networkx_nodes(G, pos, node_size=50)

# edges
nx.draw_networkx_edges(G, pos, width=2)

# node labels
nx.draw_networkx_labels(G, pos, font_size=5, font_family="sans-serif", labels={k: v['num'] for k, v in G.nodes(data=True)})
# edge weight labels
edge_labels = nx.get_edge_attributes(G, "distance")
nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=5, font_family="sans-serif")

plt.axis("off")
plt.tight_layout()
plt.savefig("graph.png", dpi=300)

nx.write_gexf(G, 'holland.gexf')

with open('rd_boxes.geojson', 'w') as handle:
    handle.write("const rd_boxes = ")
    json.dump(rd_boxes, handle, indent=2)
