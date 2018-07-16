/*
 Penserbjorne - Sebastian Aguilar
 06/2017
 FI-IIMAS-IIJ-UNAM
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


var country2color={
	"argentina":"#922B21",
	"barbados":"#CB4335",
	"bolivia":"#884EA0 ",
	"brasil":"#7D3C98",
	"chile":"#2471A3",
	"colombia":"#2E86C1",
	"costa rica":"#2E86C1",
	"dominicana":"#17A589",
	"ecuador":"#138D75",
	"el salvador":"#F1C40F",
	"guatemala":"#D68910",
	"granada":"#D68910",
	"haití":"#800000",
	"honduras":"#008080",
	"jamaica":"#FFFF00",
	"méxico":"#008000",
	"nicaragua":"#0000FF",
	"panama":"#000080",
	"paraguay":"#800080",
	"perú":"#FF0000",
	"república dominicana":"#FF5733",
	"trinidad y tobago":"#808000",
	"surinam":"#FFCE00",
	"uruguay":"#5AC8D8",
	"venezuela":"#CF0A2C",
}

function load_data(data){
	var nodes_ = [];
	var edges_ = [];


	for(inode in data.nodes){
		node=data.nodes[inode];
		if(node.type==1){
			nodes_.push({'group':node.type,'id':node.id, 'lower_label': node.name.toLowerCase(), 'case_id':node.case_id, 'label':node.name,'clicked':false, 'year':node.year, 'color':country2color[node.country],'size':35});
		}else if(node.type==2){
			nodes_.push({'group':node.type,'id':node.id, 'lower_label': node.name.toLowerCase(), 'label':node.name,'clicked':false, 'year':node.year});
		}else if(node.type==3){
			nodes_.push({'group':node.type,'id':node.id, 'lower_label': node.name.toLowerCase(), 'label':node.name,'clicked':false, 'year':node.year});
		}
	}

	nodes = new vis.DataSet(nodes_);

	for(ilink in data.links){
		link=data.links[ilink];
		if("cidh".localeCompare(link.type)==0){
			edges_.push({to:link.source, from:link.target,value:link.value,arrows:'to',ori_value:link.ori_val,color:{color:'blue'}});
		}else{
			edges_.push({to:link.source, from:link.target,value:link.value,arrows:'to',ori_value:link.ori_val,color:{color:'orange'}});
			
		}
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
			stabilization: {
				enabled: true,
				iterations: 1000,
				updateInterval: 25
			}
		},
		layout: {
			improvedLayout: false,
        },
        edges: {
          smooth: true,
          arrows: {to : true }
        }	

	};
	network = new vis.Network(container, data_vis, options);

	network.on("stabilizationIterationsDone", function () {
		    network.setOptions( { physics: false } );
	});

	network.on("click", function (params) {
		params.event = "[original event]";
		if(params.nodes.length>0){
			var node = nodes.get(params.nodes[0]);
			if(node.group==1){
				$.getJSON('contensioso/'+node.case_id,function(data){
					document.getElementById('infoNode').innerHTML = infoNode(params,data,node);
				});
			}else{
				document.getElementById('infoNode').innerHTML = infoNode(params,null,node);
			}
			};
		});

	document.getElementById('len_nodes').innerHTML = nodes.length;
	document.getElementById('len_sntcs').innerHTML = nodes_.filter((node) =>node.group==1).length;
	document.getElementById('len_citations').innerHTML = nodes_.filter((node) => node.group==2).length;
	document.getElementById('len_arcs').innerHTML = edges.length;

}

function dynamicSort(property) {
    var sortOrder = 1;
    if(property[0] === "-") {
        sortOrder = -1;
        property = property.substr(1);
    }
    return function (a,b) {
        var result = (a[property] < b[property]) ? -1 : (a[property] > b[property]) ? 1 : 0;
        return result * sortOrder;
    }
}

function infoNode(params,info,node){
	var tipo = "Arco";
	var name = "";
	node=nodes.get(params.nodes[0])

	//draw column_on
	if(node.group==2){
		tipo = "Documento cita";
		name = node.label;
		var column_one=`<div class="column">
			<table class="table">
			<tbody>
			<tr><td><strong>Tipo</strong></td><td>${tipo}</td></tr>
			<tr><td><strong>Total arcos</strong></td><td>${params.edges.length}</td></tr>
			</tbody>
		</table>
		</div>`;
	} else if(info.doc_type=="source"){
		tipo = "Sentencia";
		name = info.meta_name.name;
		var column_one=`<div class="column">
			<table class="table">
			<tbody>
			<tr><td><strong>Tipo</strong></td><td>${tipo}</td></tr>
			<tr><td><strong>Subtítulo</strong></td><td>${info.meta_name.actions}</td></tr>
			<tr><td><strong>Número</strong></td><td>${info.meta_name.number}</td></tr>
			<tr><td><strong>Fecha</strong></td><td>${info.meta_name.date_sentence}</td></tr>
			<tr><td><strong>Total arcos</strong></td><td>${params.edges.length}</td></tr>
			<tr><td><strong>Fuentes</strong></td><td>
        		<a href="${info.source_pdf}" target="_blank" >
            	<span class="icon">
            		<i class="fa fa-file-pdf-o"></i>
            	</span>
        		</a>
        		<a href="doc/${info.txt.split("/").pop(-1)}">
            		<span class="icon">
            		<i class="fa fa-eye"></i>
            	</span>
        		</a>
        	</td>
        	</tr>

			</tbody>
		</table>
		</div>
	`;
	}

	var connected_edges = network.getConnectedEdges(node.id);
	var connected_edges_ = [];
	connected_edges.forEach(function(connected_edge){
		connected_edge=edges.get(connected_edge);
		connected_edges_.push(connected_edge);
	});

	connected_edges_.sort(dynamicSort("-ori_value"));

	var rows_column_two = "";
	connected_edges_.forEach(function(connected_edge){
		if(node.group==1){
			connected_node=nodes.get(connected_edge.from);
			rows_column_two+=`<tr><td>${connected_node.label}</td><td>${connected_edge.ori_value}</td></tr>`
		}else{
			connected_node=nodes.get(connected_edge.to);
			rows_column_two+=`<tr><td>${connected_node.label}</td><td>${connected_edge.ori_value}</td></tr>`
		}
	})

	var column_two=`<div class="column">
			<table class="table">
			<thead>
				<tr><th>Cita</th><th>Cantidad</th></tr>
			</thead>
			<tbody>
			${rows_column_two}
			</tbody>
			</table>
	</div>`



	return `<div class="card">
	<header class="card-header">
	    <p class="card-header-title has-text-primary">
		      ${name}
		</p>
	</header>
		<div class="card-content">
		    <div class="content">
				<div class='columns'>${column_one} ${column_two}</div>
			</div>
		</div>
		</div>`;
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

	updateCounts();
}



function updateEdges(){
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
}

function updateCounts(){
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


function showInfoPageGrafo(){
	document.getElementById("myModalGrafo").classList.add('is-active');
}

function closeInfoPageGrafo(){
	document.getElementById("myModalGrafo").classList.remove('is-active');
}

function countryChange(me, country){
	var updates = [];
	var updates_ = [];
	nodes.forEach(function(node) {
			if((node.hidden==false || !node.hidden) && node.lower_label.includes(country) && ! me.checked){
				updates.push({id:node.id,hidden:true});
				var edges_ = network.getConnectedEdges(node.id);
				for (iedge in edges_){
					var edge= edges_[iedge];
					updates_.push({id:edge,hidden:true});
				}
			}
			if(node.hidden==true && node.lower_label.includes(country) & me.checked){
				updates.push({id:node.id,hidden:false});
				var edges_ = network.getConnectedEdges(node.id);
				for (iedge in edges_){
					var edge= edges_[iedge];
					updates_.push({id:edge,hidden:false});
				}

			}
	});
	nodes.update(updates);
	edges.update(updates_);
	updateEdges();
	updateCounts();
}


function myFilterNode(){
	var updates = [];
	var updates_ = [];
    var input;
    input = document.getElementById("myFilterNode").value.toLowerCase();
 
	nodes.forEach(function(node) {
			if((node.hidden==false || !node.hidden) && !node.lower_label.includes(input)){
				updates.push({id:node.id,hidden:true});
				var edges_ = network.getConnectedEdges(node.id);
				for (iedge in edges_){
					var edge= edges_[iedge];
					updates_.push({id:edge,hidden:true});
				}
			}
			if(node.hidden==true && node.lower_label.includes(input)){
				updates.push({id:node.id,hidden:false});
				var edges_ = network.getConnectedEdges(node.id);
				for (iedge in edges_){
					var edge= edges_[iedge];
					updates_.push({id:edge,hidden:false});
				}

			}
	});
	nodes.update(updates);
	edges.update(updates_);
	updateEdges();
	updateCounts();
}
