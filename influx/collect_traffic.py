from influxdb import InfluxDBClient
import sys
import json
import time

# recovers forwarding traffic matrix (raw byte count)
def get_routers_traffic(topology, influx_client):
	prefix_ids = []
	# gets all prefix-SID in the topology
	for routerID, routerInfo in topology.items():
		prefix_ids.append(routerInfo['prefix-sid'])

	routers_traffic = {}
	for routerID, routerInfo in topology.items():
		routers_traffic[routerInfo['name']] = {}
		router_traffic = routers_traffic[routerInfo['name']]
		for interface, neighbor in routerInfo['interfaces'].items():
			router_traffic[topology[neighbor]['name']] = {}
			forwardInfo = router_traffic[topology[neighbor]['name']]
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
and \"label_information/outgoing_physical_interface\" = $interface \
and time > now() - 1m"

				result = client.query(traffic_request, bind_params=bind_params)

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






if len(sys.argv) != 7 or sys.argv[1] != '-host' or\
	sys.argv[3] != '-port' or sys.argv[5] != '-topology':
	print("usage: python collect_traffic.py -host '<host ip>' -port '<host port>' \
-topology <topology file>")
	exit(1)

# connect to influx DB in jalapeno
client = InfluxDBClient(sys.argv[2], int(sys.argv[4]), 'root', 'root', 'mdt_db')

with open(sys.argv[6]) as json_file:
	topology = json.load(json_file)


routers_traffics = []
routers_traffics.append(get_routers_traffic(topology, client))

# retreives counters in two minutes interval
time.sleep(120)

routers_traffics.append(get_routers_traffic(topology, client))
print(json.dumps(routers_traffics, indent=4, sort_keys=True))



















