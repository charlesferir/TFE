import json
import sys
import networkx as nx

if len(sys.argv) != 5 or sys.argv[1] != '-topology'\
	or sys.argv[3] != '-dest':
	print("usage: python graph_topology.py -topology <topology file> -dest <destination file>")
	exit(1)

with open(sys.argv[2]) as json_file:
	topology = json.load(json_file)

G = nx.DiGraph()
links = set()

for routerID, routerInfo in topology.items():
	nodeID = routerID
	G.add_node(nodeID)
	for interface, connection in routerInfo['interfaces'].items():
		if connection['link-ID'] not in links:
			links.add(connection['link-ID'])
			neighborNodeID = connection['connected-to']
			G.add_edge(nodeID, neighborNodeID, id=connection['link-ID'])

d = nx.json_graph.node_link_data(G)
for node in d['nodes']:
	node['name'] = topology[node['id']]['name']
	node['prefix-sid'] = topology[node['id']]['prefix-sid']
json.dump(d, open(sys.argv[4], "w"), indent=4)

# options = {
#     'node_size' : 4000,
#     'width' : 2,
#     'node_color' : '#00b4d9'
# }

# pos = nx.circular_layout(G)
# nx.draw(G, pos, with_labels=True, **options)

# x_values, y_values = zip(*pos.values())

# x_max = max(x_values)
# x_min = min(x_values)
# x_margin = (x_max - x_min) * 0.2
# plt.xlim(x_min - x_margin, x_max + x_margin)

# y_max = max(y_values)
# y_min = min(y_values)
# y_margin = (y_max - y_min) * 0.2
# plt.ylim(y_min - y_margin, y_max + y_margin)

# plt.savefig(sys.argv[4], bbox_inches='tight')
















