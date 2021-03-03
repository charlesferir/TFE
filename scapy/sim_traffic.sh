ip netns exec host0 python3 sim_traffic.py -dest '10.0.0.3' -label 100103 -b 1000 > /dev/null &
ip netns exec host0 python3 sim_traffic.py -dest '10.0.0.2' -label 100102 -b 1000 > /dev/null &

ip netns exec host1 python3 sim_traffic.py -dest '10.0.0.3' -label 100103 -b 1000 > /dev/null &

ip netns exec host2 python3 sim_traffic.py -dest '10.0.0.0' -label 100100 -b 1000 > /dev/null &