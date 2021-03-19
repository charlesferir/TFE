from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
import json
import os
import ipaddress
from . import topology as tp
from . import link_utilisation as lu
from . import graph_topology as gt
from . import fetch_topology as ft
from . import collect_traffic as ct
from . import build_traffic_matrix as btm

bp = Blueprint('what_if', __name__)
examples = {'ex1', 'ex2', 'ex3'}


@bp.route('/')
def index():
	global state, examples

	to_load = None
	if 'topology' in request.args:
		to_load = request.args.get('topology')

	if to_load is None:
		return render_template(
			'what_if/index.html',
			topology=None
		)

	if to_load not in examples:
		try:
			ipaddress.ip_address(to_load)
			topology_json = ft.fetch_topology(to_load)
			if not os.path.exists('gui/' + to_load.replace('.', '_')):
				os.makedirs('gui/' + to_load.replace('.', '_'))
			
			dest_file_path = 'gui/' + to_load.replace('.', '_') + '/topology.json'
			json.dump(topology_json, open(dest_file_path, 'w'), indent=4)
			topology = tp.Topology('gui/' + to_load.replace('.', '_') + '/topology.json')

			routers_traffics = ct.collect_traffic(topology_json, to_load)
			json.dump(routers_traffics, open('gui/' + to_load.replace('.', '_') + '/routers_traffics.json', 'w'), indent=4)
			traffic_matrix = btm.build_traffic_matrix(routers_traffics, topology)
			dest_file_path = 'gui/' + to_load.replace('.', '_') + '/traffic_matrix.json'
			json.dump(traffic_matrix, open(dest_file_path, 'w'), indent=4)
			to_load = to_load.replace('.', '_')
		except ValueError:
			return render_template('what_if/index.html',topology=None)


	topology = tp.Topology('gui/' + to_load + '/topology.json')

	with open('gui/' + to_load + '/traffic_matrix.json') as json_file:
		traffic_matrix_prefix = json.load(json_file)

	traffic_matrix = {}
	for router_IP, router_traffic in traffic_matrix_prefix.items():
		traffic_matrix[router_IP] = {}
		for prefix_SID, traffic in router_traffic.items():
			other_IP = topology.prefixes_to_routers[prefix_SID].IP_address
			traffic_matrix[router_IP][other_IP] = (traffic / 1E6) * 8

	lu.link_utilisation(topology, traffic_matrix_prefix)
	graph = gt.graph_topology(topology, 'gui/static/graph.json')

	return render_template(
		'what_if/index.html',
		topology=topology,
		traffic_matrix=traffic_matrix,
		graph=graph
	)
