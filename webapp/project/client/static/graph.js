/*
 Penserbjorne - Sebastian Aguilar
 06/2017
 FI-IIMAS-IIJ-UNAM
 Based on https://bl.ocks.org/mbostock/4062045
 Custom javascript for graph
*/

var network;
var nodes;
var edges;
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



handlesSlider.noUiSlider.on('slide', function(){
	var ini_year;
	var fin_year;
	years=handlesSlider.noUiSlider.get();
	update_graph(years[0],years[1]);
});

function load_data(data){
	var nodes_ = [];
	var edges_ = [];

	
	for(inode in data.nodes){
		node=data.nodes[inode];
		nodes_.push({'group':node.type,'id':node.id, 'label':node.name,'clicked':false, 'year':node.year});
	}

	nodes = new vis.DataSet(nodes_);

	for(ilink in data.links){
		link=data.links[ilink];
		edges_.push({"from":link.source, "to":link.target,'value':link.value});
	}

	edges = new vis.DataSet(edges_);

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
	network = new vis.Network(container, data_vis, options);

	network.on("click", function (params) {
		params.event = "[original event]";
		var nodo = params.nodes[0];
		var info={};
		$.getJSON('contensioso/'+nodo,function(data){
			console.log(data);
			document.getElementById('infoNode').innerHTML = infoNode(params,data);
		})
		});

	document.getElementById('len_nodes').innerHTML = nodes.length;
	document.getElementById('len_sntcs').innerHTML = nodes_.filter((node) =>node.group==1).length;
	document.getElementById('len_citations').innerHTML = nodes_.filter((node) => node.group==2).length;
	document.getElementById('len_arcs').innerHTML = edges.length;

}


function infoNode(params,info){

	var tipo = "Arco";
	if(params.nodes.length==1){
		tipo = "Nodo";
	}

	var template=`<table class="table">
		<tbody>
		<tr><td><strong>Tipo</strong></td><td>${tipo}</td></tr>
		<tr><td><strong>Total arcos</strong></td><td>${params.edges.length}</td></tr>
		<tr><td><strong>Nombre</strong></td><td>${info.meta_name.name}</td></tr>
		</tbody>
	</table>`;

	return template;
}


function update_graph(ini,fin){
	var updates = [];
	var updates_ = [];
	nodes.forEach(function(node) {
		if(node.group==1){
			if((node.hidden==false || !node.hidden) && (node.year<ini || node.year>fin)){
				updates.push({id:node.id,hidden:true});
				var edges_ = network.getConnectedEdges(node.id);
				for (iedge in edges_){
					var edge= edges_[iedge];
					updates_.push({id:edge,hidden:true});	
				}
			}
			if(node.hidden==true && (node.year>=ini && node.year<=fin)){
				updates.push({id:node.id,hidden:false});
				var edges_ = network.getConnectedEdges(node.id);
				for (iedge in edges_){
					var edge= edges_[iedge];
					updates_.push({id:edge,hidden:false});	
				}

			}
		}
	});
	nodes.update(updates);
	edges.update(updates_);
	updates = [];
	nodes.forEach(function(node) {
		if(node.group==2){
			var nodes_ = network.getConnectedEdges(node.id);
			var res_ = true;
			for(inode in nodes_){
				if (edges.get(nodes_[inode]).hidden == undefined || edges.get(nodes_[inode]).hidden==false){
					res_ = false;
					break;
				}
			}
			if((node.hidden==false || !node.hidden) && res_==true)
			{
				updates.push({id:node.id,hidden:true});
			}
			if(node.hidden==true && res_==false)
			{
				updates.push({id:node.id,hidden:false});
			}

		}
	});
	nodes.update(updates);

	var n_nodes=0;
	var n_nodes_1=0;
	var n_nodes_2=0;
	var n_edges =0;
	nodes.forEach(function(node){
		if (node.hidden == undefined || node.hidden == false){
			n_nodes+=1;
			if (node.group==1){
				n_nodes_1+=1;	
			}
			if (node.group==2){
				n_nodes_2+=1;	
			}
			
		}
	});

	edges.forEach(function(edge){
		if (edge.hidden == undefined || edge.hidden == false){
			n_edges+=1;
		}
	});

	document.getElementById('len_nodes').innerHTML = n_nodes;
	document.getElementById('len_sntcs').innerHTML = n_nodes_1;
	document.getElementById('len_citations').innerHTML = n_nodes_2;
	document.getElementById('len_arcs').innerHTML = n_edges;
}



