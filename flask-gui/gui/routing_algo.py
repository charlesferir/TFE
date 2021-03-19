def dijkstra(topology):
	paths = {}
	for IP_address, router in topology.routers.items():
		queue = [(router, [])]
		discovered_routers = {
			IP_address : [
				{
					'path' : []
				}
			]
		}
		
		while len(queue) > 0:
			current_router, current_path = queue.pop(0)
			for interface, neighbor in current_router.neighbors.items():
				if neighbor.IP_address not in discovered_routers or\
					len(current_path) <= len(discovered_routers[neighbor.IP_address][0]['path']):

					neighbor_path = current_path + [{
						'outgoing-interface' : interface,
						'next-hop' : neighbor.IP_address,
						'link-ID' : current_router.connected_links[interface].ID
					}]
					queue.append((neighbor, neighbor_path))

					if neighbor.IP_address not in discovered_routers:
						discovered_routers[neighbor.IP_address] = []
					
					discovered_routers[neighbor.IP_address].append(
						{
							'path' : neighbor_path
						}
					)

		for destination_IP, paths_info in discovered_routers.items():
			for path_info in paths_info:
				path_info['traffic_portion'] = 1 / len(paths_info) 


		paths[IP_address] = discovered_routers
	return paths
		

