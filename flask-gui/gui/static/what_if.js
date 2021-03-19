// This is adapted from https://bl.ocks.org/mbostock/2675ff61ea5e063ede2b5d63c08020c7

const MAX_OPACITY = 1;
const MIN_OPACITY = 0.2;
const OPACITY_TWEEN = 500;

const INFO_RECT_WIDTH = 200;
const INFO_RECT_HEIGHT = 80;


var getJSON = function(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'json';
    xhr.onload = function() {
      var status = xhr.status;
      if (status === 200) {
        callback(null, xhr.response);
      } else {
        callback(status, xhr.response);
      }
    };
    xhr.send();
};


var selected_node = null;
var previous_selected_node = null;
var selected_node_info = null;
var node_info = null;

var svg = d3.select("svg"),
	width = +svg.attr("width"),
	height = +svg.attr("height");



var simulation = d3.forceSimulation()
	.force("link", d3.forceLink()
		.id(function (d) {
			return d.id;
		})
		.distance(200)
		.strength(1)
	)
	.force("charge", d3.forceManyBody())
	.force("center", d3.forceCenter(width / 2, height / 2));

load_topology();

function load_topology() {
	getJSON('/static/graph.json', got_graph);
	d3.json("static/graph.json", function (error, graph) {

		var routers = {};
		var neighbors = {};
		for(var i in graph.nodes) {
			var n = graph.nodes[i];
			routers[n["id"]] = n;
		}

		for(var i in graph.nodes) {
			var n = graph.nodes[i];
			var neighbor = {};
			for(var j in graph.links) {
				var l = graph.links[j];
				if(l["source"] == n["id"]) 
					neighbor[l["target"]] = routers[l["target"]]["name"];
				if(l["target"] == n["id"]) 
					neighbor[l["source"]] = routers[l["source"]]["name"];
			}
			neighbors[n["id"]] = neighbor;
		}



		if (error) throw error;

		var link = svg.append("g")
			.attr("class", "links")
			.selectAll("line")
			.data(graph.links)
			.enter().append("line")
			.attr("id", function (d, i) {
				return "link-" + i;
			})
			.attr("class", function (d, i) {
				if(d.util < 0.4)
					return "green";
				if(d.util >= 0.4 && d.util < 0.75)
					return "orange";
				return "red";
			});

		var node = svg.selectAll(".node")
			.data(graph.nodes)
				.enter().append("g")
			.attr("class", "node")
			.attr("id", function (d) {
				return d.name;
			})
			.attr("IP", function (d) {
				return d.id;
			})
			.call(d3.drag()
				.on("start", dragstarted)
				.on("drag", dragged)
				.on("end", dragended));

		
		node.on("click", node_clicked);
		svg.on("click", svg_clicked);

		node_info = svg.append('g')
			.attr('class', 'node-info');

		node_info.on("click", node_info_clicked);
		node_info.append('rect')
			.attr('x', 10)
			.attr('y', 10)
			.attr('width', INFO_RECT_WIDTH)
			.attr('height', 0);

		node_info_text = node_info.append('g')
			.attr('class', 'node-info-text');


		


		node.append("circle")
			.attr("r", 25);

		node.append("text")
			.attr("class", "router-name")
			.attr("dx", -14)
			.attr("dy", 5)
			.text(function(d) { return d.name });

		simulation
			.nodes(graph.nodes)
			.on("tick", ticked);

		simulation.force("link")
			.links(graph.links);

		function svg_clicked() {

			if(selected_node_info != null) {

				selected_node_info = null;
				return;
			}

			if(previous_selected_node != null &&
				selected_node != null &&
				previous_selected_node.attr("id") == selected_node.attr("id")) {
				return;
			}

			node_info.select("rect")
					.transition().duration(OPACITY_TWEEN).attr('height', 0);




			for(var i in graph.nodes) {
				var n = graph.nodes[i];
				svg.select("#" + n["name"])
					.select("circle")
					.transition().duration(OPACITY_TWEEN).attr("opacity", MAX_OPACITY);

				svg.select("#" + n["name"])
					.select("text")
					.transition().duration(OPACITY_TWEEN).attr("opacity", MAX_OPACITY);
			}

			for(var j in graph.links) {
				svg.select("#link-" + j)
					.transition().duration(OPACITY_TWEEN).attr("opacity", MAX_OPACITY);
			}

			if(previous_selected_node != null) {
				// svg.select(".node-info").remove();
				node_info_text.selectAll("text").remove();
				previous_selected_node = null;
			}

			if(selected_node != null) {

				node_info.select("rect")
					.transition().duration(OPACITY_TWEEN).attr('height', INFO_RECT_HEIGHT);

				full_node = routers[selected_node.attr("IP")]

				infos = [
					"IP : " + full_node["id"],
					"Prefix-SID : " + full_node["prefix-sid"],
					"Connections : " + Object.keys(neighbors[full_node["id"]]).length
				]

				for(info in infos) {
					node_info_text.append('text')
						.attr("dx", 20)
						.attr("dy", 30 + info * 20)
						.attr("fill-opacity", 0)
						.text(infos[info])
						.transition().duration(OPACITY_TWEEN * 2).attr("fill-opacity", 1);

				}

				node_info_text.append('text')
					.attr("dx", 170)
					.attr("dy", 70)
					.attr("class", "icon")
					.attr("fill-opacity", 0)
					.text('\u2304')
					.transition().duration(OPACITY_TWEEN * 2).attr("fill-opacity", 1);
				

				// console.log(selected_node.attr("id"))
				selected_IP = selected_node.attr("IP");
				for(var i in graph.nodes) {
					var n = graph.nodes[i];
					if(!(selected_IP in neighbors[n["id"]]) && selected_IP != n["id"]) {
						svg.select("#" + n["name"])
							.select("circle")
							.attr("opacity", MAX_OPACITY)
							.transition().duration(OPACITY_TWEEN).attr("opacity", MIN_OPACITY);

						svg.select("#" + n["name"])
							.select("text")
							.attr("opacity", MAX_OPACITY)
							.transition().duration(OPACITY_TWEEN).attr("opacity", MIN_OPACITY);
					}
				}

				for(var j in graph.links) {
					var l = graph.links[j];
					if(l["source"]["id"] != selected_IP && l["target"]["id"] != selected_IP) {
						svg.select("#link-" + j)
							.attr("opacity", MAX_OPACITY)
							.transition().duration(OPACITY_TWEEN).attr("opacity", MIN_OPACITY);
					}
				}

			}
				// selected_node.select("circle").attr('r', 50);
			previous_selected_node = selected_node;
			selected_node = null;

		}

		function node_info_clicked() {
			selected_node_info = d3.select(this);
		}

		function node_clicked() {
			// d3.select(this).select("circle").attr('r', 50);
			
			selected_node = d3.select(this);
		}

		function ticked() {
			link
				.attr("x1", function (d) {
					return d.source.x;
				})
				.attr("y1", function (d) {
					return d.source.y;
				})
				.attr("x2", function (d) {
					return d.target.x;
				})
				.attr("y2", function (d) {
					return d.target.y;
				});

			node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
		}
	});
}
function dragstarted(d) {
	if (!d3.event.active) simulation.alphaTarget(0.3).restart();
	d.fx = d.x;
	d.fy = d.y;
}

function dragged(d) {
	d.fx = d3.event.x;
	d.fy = d3.event.y;
}

function dragended(d) {
	if (!d3.event.active) simulation.alphaTarget(0);
	d.fx = null;
	d.fy = null;
}



function got_graph(err, data) {
}


function get_topology() {
	load_topology();
	document.getElementById("topology_search").submit();
	
}