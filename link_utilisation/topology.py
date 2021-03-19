import json
import routing_algo

class Topology:
	def __init__(self, topology_file_path):
		with open(topology_file_path) as json_file:
			topology_dict = json.load(json_file)

		self.routers = {}
		self.links = {}
		for IP_address, routerInfo in topology_dict.items():
			self.routers[IP_address] = Router(routerInfo['name'], IP_address, routerInfo['prefix-sid'])

		for IP_address, routerInfo in topology_dict.items():
			for interface, connection in routerInfo['interfaces'].items():
				if connection['link-ID'] in self.links:
					link = self.links[connection['link-ID']]
				else:
					link = Link(connection['link-ID'], 10E+3)
					self.links[connection['link-ID']] = link

				
				self.routers[IP_address].add_neighbor(
					interface,
					link,
					self.routers[connection['connected-to']]
				)
class Path:
	def __init__(links):
		self.links = links

	def add_traffic(self, traffic):
		for link_ID, link in links.items():
			link.add_traffic(traffic)

class Link:
	def __init__(self, link_ID, capacity):
		self.ID = link_ID
		self.capacity = capacity
		self.util = 0
		self.util_raw = 0

	def add_traffic(self, traffic):
		self.util_raw += traffic
		self.util = self.util_raw / self.capacity

class Router:
	def __init__(self, name, IP_address, prefix_SID):
		self.name = name
		self.IP_address = IP_address
		self.prefix_SID = prefix_SID
		self.neighbors = {}
		self.connected_links = {}

	def add_neighbor(self, interface, link, neighbor):
		self.neighbors[interface] = neighbor
		self.connected_links[interface] = link

























