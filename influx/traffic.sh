mkdir -p traffic
python collect_traffic.py -host $2 -port '30308' -topology ../arango/topology/topology.txt > traffic/traffic.json
python build_traffic_matrix.py -traffic traffic/traffic.json > traffic/traffic_matrix.json