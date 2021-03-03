#! /usr/bin/env python

# Set log level to benefit from Scapy warnings
import logging
logging.getLogger("scapy").setLevel(2)

from scapy.all import *
import subprocess
import sys
import time
from random import getrandbits, randint
from ipaddress import IPv4Network, IPv4Address


class MPLS(Packet):
         name = "MPLS"
         fields_desc =  [
                 BitField("label", 3, 20),
                 BitField("experimental_bits", 0, 3),
                 BitField("bottom_of_label_stack", 1, 1),
                 ByteField("TTL", 255)
                 ]

if len(sys.argv) != 7 or sys.argv[1] != '-dest' or\
	sys.argv[3] != '-label' or sys.argv[5] != '-b':
	print("usage: python sim_traffic.py -dest '<destination ip>' -label <prefix-SID> -b <bandwidth>")
	exit(1)


bind_layers(Ether, MPLS, type = 0x8847)
bind_layers(MPLS, MPLS, bottom_of_label_stack = 0)
bind_layers(MPLS, IP)

while True:
	p = Ether() / MPLS(label = int(sys.argv[4]), experimental_bits = 0, bottom_of_label_stack=1) / IP(dst = sys.argv[2]) / ICMP()
	# p = Ether() / IP(dst = "10.0.0.3") / ICMP()
	tic = time.perf_counter()
	sendp(p, count=int(int(sys.argv[6])/len(p)))
	toc = time.perf_counter()

	wait_for = toc - tic
	if wait_for < 1:
		time.sleep(1 - wait_for)

