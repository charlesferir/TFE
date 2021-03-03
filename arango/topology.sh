mkdir -p topology
python fetch_topology.py -host $2 -port '30852' > topology/topology.txt
python graph_topology.py -topology topology/topology.txt -dest topology/topology.png
