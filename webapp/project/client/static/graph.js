/*
 Penserbjorne - Sebastian Aguilar
 06/2017
 FI-IIMAS-IIJ-UNAM
 Based on https://bl.ocks.org/mbostock/4062045
 Custom javascript for graph
*/


var handlesSlider = document.getElementById('slider');
var year = (new Date()).getFullYear();
var range_year = [1988,year];

noUiSlider.create(handlesSlider, {
	start: [ 1988, year ],
	range: {
		'min': [ 1988 ],
		'max': [ year ]
	},
	tooltips: [ wNumb({ decimals: 0 }), wNumb({ decimals: 0}) ],
	step: 1,
	connect: true,
});

handlesSlider.noUiSlider.on('update', function( values, handle ) {
	range_year[handle] = parseInt(values[handle]);
});


function update_data(data){
	var nodes=[];
	var edges=[];
	for(inode in data.nodes){
		node=data.nodes[inode];
		nodes.push({'group':node.type,'id':inode, 'label':node.name,'clicked':false});
	}

	for(ilink in data.links){
		link=data.links[ilink];
		edges.push({"from":link.source, "to":link.target,'value':link.value});
	}

	var data_vis={
		nodes:nodes,
		edges:edges
	}

  	var container = document.getElementById('graph-ctn');

	var options = {
    	nodes: {
          shape: 'dot',
          size: 16
        },
		physics: {
			forceAtlas2Based: {
				gravitationalConstant: -26,
				centralGravity: 0.005,
				springLength: 230,
				springConstant: 0.18
			},
			maxVelocity: 146,
			solver: 'forceAtlas2Based',
			timestep: 0.35,
			stabilization: {iterations: 150},
		}
	};
	var network = new vis.Network(container, data_vis, options);

}


$.getJSON('/conectividad/static/graph.json', function(data_) {update_data(data_)});


