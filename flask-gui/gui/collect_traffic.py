from influxdb import InfluxDBClient
import sys
import json
import time

# recovers forwarding traffic matrix (raw byte count)
def get_routers_traffic(topology, influx_client, time_span):
	prefix_ids = []
	# gets all prefix-SID in the topology
	for routerID, routerInfo in topology.items():
		prefix_ids.append(routerInfo['prefix-sid'])

	routers_traffic = {}
	for routerID, routerInfo in topology.items():
		routers_traffic[routerInfo['name']] = {}
		router_traffic = routers_traffic[routerInfo['name']]
		for interface, neighbor in routerInfo['interfaces'].items():
			router_traffic[topology[neighbor['connected-to']]['name']] = {}
			forwardInfo = router_traffic[topology[neighbor['connected-to']]['name']]
			for prefix_id in prefix_ids:

				
				bind_params = {
					'source': routerInfo['name'],
					'label_value' : str(prefix_id),
					'interface' : 'Gi' + interface[-7:]
				}

				# gets a forwarding traffic matrix entry (neighbor, label)
				traffic_request = "select last(\"label_information/tx_bytes\") from \
\"Cisco-IOS-XR-fib-common-oper:mpls-forwarding/nodes/node/label-fib/forwarding-details/forwarding-detail\" \
where source = $source \
and label_value = $label_value \
and \"label_information/outgoing_physical_interface\" = $interface"

				if time_span > 0:
					traffic_request += ' and time < now() - ' + str(time_span) + 'm'\
						+ ' and time > now() - ' + str(time_span + 2) + 'm'
				else:
					traffic_request += ' and time > now() - 2m'
				result = influx_client.query(traffic_request, bind_params=bind_params)

				# counter is null (no traffic)
				if len(result.raw['series']) == 0:
					forwardInfo[prefix_id] = [0, None]

				# recovers counter value and time at which it was retreived
				else:
					forwardInfo[prefix_id] = [
						result.raw['series'][0]['values'][0][1],
						result.raw['series'][0]['values'][0][0]
					]
	return routers_traffic


def collect_traffic(topology, host):
	# connect to influx DB in jalapeno
	client = InfluxDBClient(host, 30308, 'root', 'root', 'mdt_db')

	routers_traffics = []
	routers_traffics.append(get_routers_traffic(topology, client,15))
	routers_traffics.append(get_routers_traffic(topology, client, 10))
	return routers_traffics



















