from . import routing_algo as ra


def link_utilisation(topo, traffic_matrix):
	map_prefix_IP = {}
	for router_IP, router in topo.routers.items():
		map_prefix_IP[str(router.prefix_SID)] = router_IP

	routing_info = ra.dijkstra(topo)

	for source_IP, dest_prefixes in traffic_matrix.items():
		for dest_prefix, traffic in dest_prefixes.items():
			dest_IP = map_prefix_IP[str(dest_prefix)]
			pathes = routing_info[source_IP][dest_IP]
			for path_info in pathes:
				path = path_info["path"]
				for link_info in path:
					link = topo.links[link_info['link-ID']]
					link.add_traffic(path_info["traffic_portion"] * traffic)