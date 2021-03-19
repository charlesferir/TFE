from pyArango.connection import *
import sys
import json

def fetch_topology(host):
	# connect to Arango database in jalapeno
	arangoURL = 'http://' + host + ':30852'
	conn = Connection(arangoURL=arangoURL, username="root", password="jalapeno")
	db = conn["jalapeno"]

	# gets general info about routers
	nodes = db["LSNode"].fetchAll(rawResults=True)
	topology = {}

	# request to get routers neighbors
	link_request = "FOR l IN LSv4_Topology FILTER\
		l.LocalRouterID == @RouterID RETURN l"

	for node in nodes:
		topology[node['RouterID']] = {}
		topology[node['RouterID']]['name'] = node['Name']
		bind_link_request = {'RouterID' : node['RouterID']}
		links = db.AQLQuery(link_request, rawResults=True, bindVars=bind_link_request)
		if len(links) == 0:
			continue

		# retreives router prefix-SID
		topology[node['RouterID']]['prefix-sid'] = links[0]['LocalPrefixSID']
		topology[node['RouterID']]['interfaces'] = {}
		interfaces = topology[node['RouterID']]['interfaces']
		for link in links:
			# retreives router neighbors adn their liked interface
			interfaces[link['FromInterfaceName']] = {}
			interfaces[link['FromInterfaceName']]['connected-to'] = link['RemoteRouterID']

			if link['FromInterfaceIP'] < link['ToInterfaceIP']:
				interfaces[link['FromInterfaceName']]['link-ID'] = \
					link['FromInterfaceIP'] + ':' + link['ToInterfaceIP']
			else:
				interfaces[link['FromInterfaceName']]['link-ID'] = \
					link['ToInterfaceIP'] + ':' + link['FromInterfaceIP']

	return topology
	