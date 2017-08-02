/*
 Penserbjorne - Sebastian Aguilar
 06/2017
 FI-IIMAS-IIJ-UNAM
 Based on https://bl.ocks.org/mbostock/4062045
 Custom javascript for graph
*/


$.getJSON('/conectividad/static/graph.json', function(data) {
	var graph = Viva.Graph.graph();
	//var graph = graphGenerator.grid(100, 100);
	var idealLength = 1500;
	var domLabels = {};

	    var colors = [
0xddddddff,
0xccccccff,
0xbbbbbbff,
0xaaaaaaff,
0x999999ff,
0x888888ff,
0x777777ff,
0x666666ff,
0x555555ff,
0x444444ff,
0x333333ff,
                        ];


	for(inode in data.nodes){
		node=data.nodes[inode];
		graph.addNode(node.id,{'type':node.type,'name':node.name,'clicked':false});
	}

	for(ilink in data.links){
		link=data.links[ilink];
		if(link.value){
			graph.addLink(link.source, link.target,{'value':link.value,'article':link.article});
		}
	}

   	var container= document.querySelector('#graph-ctn');
	
	var layout = Viva.Graph.Layout.forceDirected(graph, {
		springLength : idealLength,
		springCoeff : 0.0008,
		dragCoeff : 0.04,
		theta: 1,
		gravity : -1.2,
		//timeStep: 10,

		//springTransform: function (link, spring) {
        //   			spring.length = idealLength * (1 - link.data.value/15);
        //}

	});


	// specify where it should be rendered:
	let graphics = Viva.Graph.View.webglGraphics()


  	var circleNode = buildCircleNodeShader();
 	graphics.setNodeProgram(circleNode);

	graphics.placeNode(function(ui, pos) {
		  // This callback is called by the renderer before it updates
		  // node coordinate. We can use it to update corresponding DOM
		  // label position;
		  // we create a copy of layout position
		  var nodeId = ui.node.id;
		  		  // then move corresponding dom label to its own position:
		  if(nodeId in domLabels && domLabels[nodeId].style.visibility=="visible"){
			var domPos = {
				  x: pos.x,
				  y: pos.y
			};
			// And ask graphics to transform it to DOM coordinates:
			graphics.transformGraphToClientCoordinates(domPos);

				var labelStyle = domLabels[nodeId].style;
		  	labelStyle.left = domPos.x + 'px';
		  	labelStyle.top = domPos.y + 'px';
		  }
   	});

  	graphics.node(function (node) {
    	if (!node.data){
     		return new WebglCircle(4, 0xdddd00);
		}
		if (node.data.type==1){
     		return new WebglCircle(24, 0x0000dd);
		}
		if (node.data.type==2){
     		return new WebglCircle(24, 0x00dd00);
		}
		if (node.data.type==3){
     		return new WebglCircle(24, 0xdddd00);
		}

  	});

	graphics.link(function(link) {
       	return Viva.Graph.View.webglLine(colors[link.data.value]);
    });

  	let renderer = Viva.Graph.View.renderer(graph, {
    	container: container,
    	layout : layout,
    	graphics: graphics,
  	});
	

	highlightRelatedNodes = function(nodeId, isOn) {
        graph.forEachLinkedNode(nodeId, function(node, link){
        	var linkUI = graphics.getLinkUI(link.id);
       			linkUI.color = isOn ? 0xff0000ff : colors[link.data.value];
		   	});
		};

	var events = Viva.Graph.webglInputEvents(graphics, graph);
	events.mouseEnter(function (node) {
					var label = document.createElement('span');
					label.classList.add('node-label');
					label.innerText = node.data.name;
					label.style.visibility="visible";
					domLabels[node.id] = label;
					container.appendChild(label);
                }).mouseLeave(function (node) {
					var label=domLabels[node.id];
					label.style.visibility="hidden";
   				}).click(function (node) {
                    highlightRelatedNodes(node.id, !node.data.clicked);
					node.data.clicked= !node.data.clicked;
                });

	renderer.run();

	
	 function generateDOMLabels(graph) {
		// this will map node id into DOM element
		var labels = Object.create(null);
		graph.forEachNode(function(node) {
			var label = document.createElement('span');
			label.classList.add('node-label');
			label.innerText = node.id;
			label.style.visibility='hidden';
			labels[node.id] = label;
			container.appendChild(label);
		});
		// NOTE: If your graph changes over time you will need to
		// monitor graph changes and update DOM elements accordingly
		return labels;
			}



  	// Lets start from the easiest part - model object for node ui in webgl
  	function WebglCircle(size, color) {
            this.size = size;
            this.color = color;
  	}


	// Next comes the hard part - implementation of API for custom shader
    // program, used by webgl renderer:
	function buildCircleNodeShader() {
    	// For each primitive we need 4 attributes: x, y, color and size.
        var ATTRIBUTES_PER_PRIMITIVE = 4,
                nodesFS = [
                'precision mediump float;',
                'varying vec4 color;',
                'void main(void) {',
                '   if ((gl_PointCoord.x - 0.5) * (gl_PointCoord.x - 0.5) + (gl_PointCoord.y - 0.5) * (gl_PointCoord.y - 0.5) < 0.25) {',
                '     gl_FragColor = color;',
                '   } else {',
                '     gl_FragColor = vec4(0);',
                '   }',
                '}'].join('\n'),
                nodesVS = [
                'attribute vec2 a_vertexPos;',
                // Pack color and size into vector. First elemnt is color, second - size.
                // Since it's floating point we can only use 24 bit to pack colors...
                // thus alpha channel is dropped, and is always assumed to be 1.
                'attribute vec2 a_customAttributes;',
                'uniform vec2 u_screenSize;',
                'uniform mat4 u_transform;',
                'varying vec4 color;',
                'void main(void) {',
                '   gl_Position = u_transform * vec4(a_vertexPos/u_screenSize, 0, 1);',
                '   gl_PointSize = a_customAttributes[1] * u_transform[0][0];',
                '   float c = a_customAttributes[0];',
                '   color.b = mod(c, 256.0); c = floor(c/256.0);',
                '   color.g = mod(c, 256.0); c = floor(c/256.0);',
                '   color.r = mod(c, 256.0); c = floor(c/256.0); color /= 255.0;',
                '   color.a = 1.0;',
                '}'].join('\n');
		var program,
                gl,
                buffer,
                locations,
                utils,
                nodes = new Float32Array(64),
                nodesCount = 0,
                canvasWidth, canvasHeight, transform,
                isCanvasDirty;
            return {
                /**
                 * Called by webgl renderer to load the shader into gl context.
                 */
                load : function (glContext) {
                    gl = glContext;
                    webglUtils = Viva.Graph.webgl(glContext);
                    program = webglUtils.createProgram(nodesVS, nodesFS);
                    gl.useProgram(program);
                    locations = webglUtils.getLocations(program, ['a_vertexPos', 'a_customAttributes', 'u_screenSize', 'u_transform']);
                    gl.enableVertexAttribArray(locations.vertexPos);
                    gl.enableVertexAttribArray(locations.customAttributes);
                    buffer = gl.createBuffer();
                },
                /**
                 * Called by webgl renderer to update node position in the buffer array
                 *
                 * @param nodeUI - data model for the rendered node (WebGLCircle in this case)
                 * @param pos - {x, y} coordinates of the node.
                 */
                position : function (nodeUI, pos) {
                    var idx = nodeUI.id;
                    nodes[idx * ATTRIBUTES_PER_PRIMITIVE] = pos.x;
                    nodes[idx * ATTRIBUTES_PER_PRIMITIVE + 1] = -pos.y;
                    nodes[idx * ATTRIBUTES_PER_PRIMITIVE + 2] = nodeUI.color;
                    nodes[idx * ATTRIBUTES_PER_PRIMITIVE + 3] = nodeUI.size;
                },
                /**
                 * Request from webgl renderer to actually draw our stuff into the
                 * gl context. This is the core of our shader.
                 */
                render : function() {
                    gl.useProgram(program);
                    gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
                    gl.bufferData(gl.ARRAY_BUFFER, nodes, gl.DYNAMIC_DRAW);
                    if (isCanvasDirty) {
                        isCanvasDirty = false;
                        gl.uniformMatrix4fv(locations.transform, false, transform);
                        gl.uniform2f(locations.screenSize, canvasWidth, canvasHeight);
                    }
                    gl.vertexAttribPointer(locations.vertexPos, 2, gl.FLOAT, false, ATTRIBUTES_PER_PRIMITIVE * Float32Array.BYTES_PER_ELEMENT, 0);
                    gl.vertexAttribPointer(locations.customAttributes, 2, gl.FLOAT, false, ATTRIBUTES_PER_PRIMITIVE * Float32Array.BYTES_PER_ELEMENT, 2 * 4);
                    gl.drawArrays(gl.POINTS, 0, nodesCount);
                },
                /**
                 * Called by webgl renderer when user scales/pans the canvas with nodes.
                 */
                updateTransform : function (newTransform) {
                    transform = newTransform;
                    isCanvasDirty = true;
                },
                /**
                 * Called by webgl renderer when user resizes the canvas with nodes.
                 */
                updateSize : function (newCanvasWidth, newCanvasHeight) {
                    canvasWidth = newCanvasWidth;
                    canvasHeight = newCanvasHeight;
                    isCanvasDirty = true;
                },
                /**
                 * Called by webgl renderer to notify us that the new node was created in the graph
                 */
                createNode : function (node) {
                    nodes = webglUtils.extendArray(nodes, nodesCount, ATTRIBUTES_PER_PRIMITIVE);
                    nodesCount += 1;
                },
                /**
                 * Called by webgl renderer to notify us that the node was removed from the graph
                 */
                removeNode : function (node) {
                    if (nodesCount > 0) { nodesCount -=1; }
                    if (node.id < nodesCount && nodesCount > 0) {
                        // we do not really delete anything from the buffer.
                        // Instead we swap deleted node with the "last" node in the
                        // buffer and decrease marker of the "last" node. Gives nice O(1)
                        // performance, but make code slightly harder than it could be:
                        webglUtils.copyArrayPart(nodes, node.id*ATTRIBUTES_PER_PRIMITIVE, nodesCount*ATTRIBUTES_PER_PRIMITIVE, ATTRIBUTES_PER_PRIMITIVE);
                    }
                },
                /**
                 * This method is called by webgl renderer when it changes parts of its
                 * buffers. We don't use it here, but it's needed by API (see the comment
                 * in the removeNode() method)
                 */
                replaceProperties : function(replacedNode, newNode) {},
            };
            };
})


/*

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

}) */
