from topology import Topology
from routing_algo import dijkstra
import json
import sys




def link_utilisation(topo, traffic_matrix):
	map_prefix_IP = {}
	for router_IP, router in topo.routers.items():
		map_prefix_IP[str(router.prefix_SID)] = router_IP

	routing_info = dijkstra(topo)

	for source_IP, dest_prefixes in traffic_matrix.items():
		for dest_prefix, traffic in dest_prefixes.items():
			dest_IP = map_prefix_IP[str(dest_prefix)]
			pathes = routing_info[source_IP][dest_IP]
			for path_info in pathes:
				path = path_info["path"]
				for link_info in path:
					link = topo.links[link_info['link-ID']]
					link.add_traffic(path_info["traffic_portion"] * traffic)

if __name__ == "__main__":
	if len(sys.argv) != 5 or sys.argv[1] != '-topology'\
		or sys.argv[3] != '-matrix':
		print("usage: python graph_topology.py -topology <topology file> -matrix <traffic matrix file>")
		exit(1)

	topo = Topology(sys.argv[2])

	with open(sys.argv[4]) as json_file:
		traffic_matrix = json.load(json_file)

	link_utilisation(topo, traffic_matrix)
	print(topo.links['10.1.1.4:10.1.1.5'].util)
	# print(json.dumps(routing_info, indent=4, sort_keys=True))
# print(topo.routers['10.0.0.1'].neighbors['GigabitEthernet0/0/0/1'].prefix_SID)