# Jalapeno
ip addr add 10.0.253.1/24 dev br7
ifconfig br7 up
ip route add 10.0.0.0/16 via 10.0.253.2 dev br7
 
# H1 setup
ip netns add host1
ip link set r01xr3 netns host1
ip netns exec host1 ip link set lo up
ip netns exec host1 ip link set dev r01xr3 up
ip netns exec host1 ip addr add 10.0.254.1/24 dev r01xr3
ip netns exec host1 ip route add 10.0.0.0/16 via 10.0.254.2 dev r01xr3


# H2 setup
ip netns add host2
ip link set r02xr3 netns host2
ip netns exec host2 ip link set lo up
ip netns exec host2 ip link set dev r02xr3 up
ip netns exec host2 ip addr add 10.0.255.1/24 dev r02xr3
ip netns exec host2 ip route add 10.0.0.0/16 via 10.0.255.2 dev r02xr3