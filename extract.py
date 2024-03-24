import json
import networkx
# convert overpass turbo into real geojson for us.

with open('holland.geojson', 'r') as handle:
    data = json.load(handle)

with open('holland.nodes.geojson', 'r') as handle:
    nodes = json.load(handle)

out = []

refs = {
    # [lat, lon, from-to]
}

G = networkx.Graph()

# First time through the data collect our nodes.
for node in nodes['elements']:
        k = f"{node['lon']},{node['lat']}"
        refs[k] = {
            'num': node['tags']['rcn_ref'],
            'id': node['id'],
            'refs': set(),
            'j': [],
        }
        G.add_node(node['id'], **{'num': node['tags']['rcn_ref']})

# Second time through deep search through the ways to find any overlaps.
for e in data['elements']:
    if e['tags']['type'] == 'route':
        # Start of a node
        matching_nodes = []
        for node in e['members']:
            for geo in node.get('geometry', []):
                k = f"{geo['lon']},{geo['lat']}"
                if k in refs:
                    matching_nodes.append(k)

                    q = set(e['tags']['ref'].split('-'))
                    q = q - {refs[k]['id']}
                    if len(q) == 0:
                        continue
                    refs[k]['refs'] |= q

        matching_nodes = list(set(matching_nodes))
        differently_numbered_nodes = set([refs[m]['num'] for m in matching_nodes])
        if len(differently_numbered_nodes) == 0:
            print("Route without nodes")
        elif len(differently_numbered_nodes) == 1:
            print("Route deadends")
        elif len(differently_numbered_nodes) == 2:
            G.add_edge(
                refs[matching_nodes[0]]['id'], 
                refs[matching_nodes[1]]['id'],
                **e['tags']
            )
            print([refs[m] for m in matching_nodes])
        else:
            print("Route with multiple nodes how do i handle this")

# import pprint
# pprint.pprint(refs)

print(G)
import matplotlib.pyplot as plt
networkx.draw(G, with_labels=True)
plt.show()
