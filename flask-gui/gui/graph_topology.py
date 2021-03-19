import json
import sys
import networkx as nx


def graph_topology(topology, output_path):
	G = nx.DiGraph()
	links = set()

	for router_IP, router in topology.routers.items():
		nodeID = router_IP
		G.add_node(nodeID)
		for interface, neighbor in router.neighbors.items():
			link = router.connected_links[interface]
			if link.ID not in links:
				links.add(link.ID)
				neighborNodeID = neighbor.IP_address
				G.add_edge(nodeID, neighborNodeID, id=link.ID, util=link.util)

	d = nx.json_graph.node_link_data(G)
	for node in d['nodes']:
		node['name'] = topology.routers[node['id']].name
		node['prefix-sid'] = topology.routers[node['id']].prefix_SID

	# json.dump(d, open(output_path, "w"), indent=4)
	return d;
	
















