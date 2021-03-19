mkdir -p topology
python fetch_topology.py -host $2 -port '30852' > topology/topology.json
python graph_topology.py -topology topology/topology.json -dest topology/topology.png
