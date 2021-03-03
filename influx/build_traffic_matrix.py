import sys
import json
import datetime

if len(sys.argv) != 3 or sys.argv[1] != '-traffic':
	print("usage: python build_traffic_matrix.py -traffic <traffic file>")
	exit(1)

with open(sys.argv[2]) as json_file:
	routers_traffics = json.load(json_file)

intial_traffics = routers_traffics[0]


# computes the  forwarding traffic matrix (throughput)
for routerName, routers_traffic in routers_traffics[1].items():
	for neighborName, prefixs_traffic in routers_traffic.items():
		for prefix_id, traffic in prefixs_traffic.items():
			intial_traffic = intial_traffics[routerName][neighborName][prefix_id]
			traffic[0] -= intial_traffic[0]
			if traffic[1] is not None and intial_traffic[1]:
				init_time = datetime.datetime.strptime(intial_traffic[1], '%Y-%m-%dT%H:%M:%S.%fZ')
				curr_time = datetime.datetime.strptime(traffic[1], '%Y-%m-%dT%H:%M:%S.%fZ')
				# time diff between measurents
				traffic[1] = (curr_time - init_time).seconds
				# throughput
				prefixs_traffic[prefix_id] = traffic[0]/traffic[1]
			else:
				prefixs_traffic[prefix_id] = 0

traffic_diff = routers_traffics[1]
traffic_matrix = {}

for routerName, routers_traffic in traffic_diff.items():
	traffic_matrix[routerName] = {}
	# add up all traffic
	for neighborName, prefixs_traffic in routers_traffic.items():
		for prefix_id, traffic in prefixs_traffic.items():
			if prefix_id in traffic_matrix[routerName]:
				traffic_matrix[routerName][prefix_id] += traffic
			else:
				traffic_matrix[routerName][prefix_id] = traffic

	# remove transit traffic
	for neighborName, prefixs_traffic in routers_traffic.items():
		if routerName in traffic_diff[neighborName]:
			for prefix_id, traffic in traffic_diff[neighborName][routerName].items():
				traffic_matrix[routerName][prefix_id] -= traffic
				if traffic_matrix[routerName][prefix_id] < 0:
					traffic_matrix[routerName][prefix_id] = 0

print(json.dumps(traffic_diff, indent=4, sort_keys=True))
print(json.dumps(traffic_matrix, indent=4, sort_keys=True))

















