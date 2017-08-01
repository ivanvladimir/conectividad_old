/*
 Penserbjorne - Sebastian Aguilar
 06/2017
 FI-IIMAS-IIJ-UNAM
 Based on https://bl.ocks.org/mbostock/4062045
 Custom javascript for graph
*/


$.getJSON('/conectividad/static/graph.json', function(data) {


	var graphGenerator = Viva.Graph.generator();
	var graph = graphGenerator.grid(3, 3);

	for(inode in data.nodes){
		node=data.nodes[inode];
		graph.addNode(node.id,{'type':node.type,'name':node.name});
	}

	for(ilink in data.links){
		link=data.links[ilink];
		graph.addLink(link.source, link.target,{'value':link.value});
	}

	var layout = Viva.Graph.Layout.forceDirected(graph, {
		springLength : 300,
		springCoeff : 0.0008,
		dragCoeff : 0.04,
		theta: 1,
		gravity : -1.2,
		timeStep: 10,
	});


  	var graphics = Viva.Graph.View.svgGraphics();

	var source_node = {'size':12,'col':'green'};
	var target_node = {'size':8,'col':'blue'};


	function node2rad(node){
	   if(node.data){
		if(node.data.type==1){
			return source_node;
		}
		if(node.data.type==2){
			return target_node;
		}
		return target_node;
	  }else{
		return target_node;
	  }
	}

	highlightRelatedNodes = function(nodeId, isOn) {
    	// just enumerate all realted nodes and update link color:
        graph.forEachLinkedNode(nodeId, function(node, link){
        var linkUI = graphics.getLinkUI(link.id);
        if (linkUI) {
               linkUI.attr('stroke', isOn ? 'red' : 'gray');
			   }
		   });
		};


	highlightLabel = function(node, isOn) {
        var nodeUI = graphics.getNodeUI(node.id);
        if (nodeUI && isOn) {
    		   var text = Viva.Graph.svg('text');
			   text.textContent = node.data.name;
    		   nodeUI.append(text);
		}
  	    if (nodeUI && !isOn) {
			nodeUI.removeChild(nodeUI.lastChild);
		}

	};




	graphics.node(function(node) {
		// now create actual node and reference created fill pattern:
    	var ui = Viva.Graph.svg('g');
		var att = node2rad(node);
    	var circle = Viva.Graph.svg('circle')
      		.attr('cx', att.size)
      		.attr('cy', att.size)
      		.attr('fill', att.col)
      		.attr('r', att.size);
    	ui.append(circle);
		$(ui).hover(function() { // mouse over
                    highlightRelatedNodes(node.id, true);
                    highlightLabel(node, true);
                }, function() { // mouse out
                    highlightRelatedNodes(node.id, false);
                    highlightLabel(node, false);
                });
    	return ui;
	});

	 graphics.placeNode(function(node, pos) {
		var att = node2rad(node);
		node.attr('transform', 'translate(' + (pos.x - att.size) + ',' + (pos.y - att.size) + ')');
     });


	graphics.link(function(link){
		var value = 1;
		if(link.data){value=link.data.value;}else{value=1;}
		
   		return Viva.Graph.svg('path')
                              .attr('stroke', 'gray')
                              .attr('stroke-width', value);
            }).placeLink(function(linkUI, fromPos, toPos) {
                var data = 'M' + fromPos.x + ',' + fromPos.y +
                           'L' + toPos.x + ',' + toPos.y;
                linkUI.attr("d", data);
            })



  	let renderer = Viva.Graph.View.renderer(graph, {
    	layout : layout,
    	graphics: graphics,
		container: document.getElementById('graph-ctn'),
  	});

  renderer.run();

})
