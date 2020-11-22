function d3GraphChartBase() {

    var margin = {top: 20, right: 20, bottom: 20, left: 20},
    width = 350 - margin.left - margin.right,
    height = 350 - margin.top - margin.bottom,
    colorBar = d3.scaleOrdinal(d3.schemeCategory10),
    barPadding = 1,
    misc = {ylabel: 7, xlabelH : 5, title:11};
    
    return {
        margin : margin, 
        width : width, 
        height : height, 
        colorBar : colorBar, 
        barPadding : barPadding,
        misc: misc
    };
}

function d3GraphChart(graph) {

    //parametros
    var basics = d3GraphChartBase();
	
	var margin = basics.margin,
		width = basics.width,
	    height = basics.height,
		colorBar = basics.colorBar,
        barPadding = basics.barPadding,
        misc = basics.misc
        ;

    // var graph = {
    //     nodes: [
    //         {name: "Usuario 1", interventions: 10},
    //         {name: "Usuario 2", interventions: 3},
    //         {name: "Usuario 3", interventions: 4},
    //         {name: "Usuario 4", interventions: 6},
    //     ],
    //     link: [
    //         {source: "Usuario 1", target: "Usuario 4", sizeLink: 12},
    //         {source: "Usuario 2", target: "Usuario 3", sizeLink: 41},
    //         {source: "Usuario 4", target: "Usuario 1", sizeLink: 66},
    //         {source: "Usuario 1", target: "Usuario 3", sizeLink: 3},
    //         {source: "Usuario 1", target: "Usuario 2", sizeLink: 53},
    //     ]
    // }

    // Tamaño de nodos
    var sizeNode = d3.scaleLinear()
    .domain([d3.min(graph.nodes, node => node.interventions),d3.max(graph.nodes, node => node.interventions)])
    .range([5, 15]);

    // Tamaño de enlace
    var sizeLink = d3.scaleLinear()
    .domain([d3.min(graph.link, link => link.sizeLink),d3.max(graph.link, link => link.sizeLink)])
    .range([0.3, 1]);

    var canvas = d3.select("#GraphChartCanvas")
    .attr("width",width)
    .attr("height",height)
    .attr("id","plano"),
    ctx = canvas.node().getContext("2d"),
    r = 0,
    simulation = d3.forceSimulation()
    .force("x",d3.forceX(width/2))
    .force("y",d3.forceY(height/2))
    .force("collide",d3.forceCollide(r+1))
    .force("change",d3.forceManyBody().strength(-3000))
    .on("tick", update)
    .force("link",d3.forceLink().id(function (d) { return d.name;}));

    simulation.nodes(graph.nodes);
    simulation.force("link").links(graph.link)

    canvas
      .call(d3.drag()
          .container(canvas.node())
          .subject(dragsubject)
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended));
    // graph.nodes.forEach(function (d){
    //     d.x = Math.random()*width;
    //     d.y = Math.random()*height;
    // });

    function update(){
        ctx.clearRect(0,0,width,height);

        // ctx.beginPath();
        // ctx.strokeStyle = "#aaa";
        graph.link.forEach(drawLink);
        //ctx.stroke();

        graph.nodes.forEach(drawNode);
    }

    function dragsubject() {
        return simulation.find(d3.event.x, d3.event.y);
    }

    function dragstarted() {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d3.event.subject.fx = d3.event.subject.x;
        d3.event.subject.fy = d3.event.subject.y;
        //console.log(d3.event.subject);
      }
      
      function dragged() {
        d3.event.subject.fx = d3.event.x;
        d3.event.subject.fy = d3.event.y;
      }
      
      function dragended() {
        if (!d3.event.active) simulation.alphaTarget(0);
        d3.event.subject.fx = null;
        d3.event.subject.fy = null;
      }

    function drawNode(d){
        ctx.beginPath();
        ctx.globalAlpha = 1
        ctx.fillStyle = d.color
        ctx.moveTo(d.x,d.y);
        ctx.arc(d.x,d.y,sizeNode(d.interventions),0,Math.PI*2);
        ctx.fill();

        ctx.globalAlpha = 1
        ctx.fillStyle = "Black"
        ctx.font = "14px Arial";
        ctx.textAlign = "center";
        ctx.fillText(d.name, d.x, d.y - 20);
    }

    function drawLink(l){
        drawBend(l.source.x,l.source.y,l.target.x,l.target.y,-0.15,10,10,false,true,10 + 1,10 + 5,l);
    }

    function getColorNode(nameNode){
        for (var i in graph.nodes){
            if (graph.nodes[i].name == nameNode){
                return graph.nodes[i].color
            }
        }
        return null
    }

    // x1,y1 location of a circle start
    // x2,y2 location of the end circle
    // bend factor. negative bends up for, positive bends down. If zero the world will end 
    // aLen is Arrow head length in pixels
    // aWidth is arrow head width in pixels
    // sArrow boolean if true draw start arrow
    // eArrow  boolean if true draw end  arrow
    // startRadius = radius of a circle if start attached to circle
    // endRadius = radius of a circle if end attached to circle
    function drawBend(x1, y1, x2, y2, bend, aLen, aWidth, sArrow, eArrow, startRadius, endRadius,l){
        var mx, my, dist, nx, ny, x3, y3, cx, cy, radius, vx, vy, a1, a2;
        var arrowAng,aa1,aa2,b1;
        // find mid point
        mx = (x1 + x2) / 2;  
        my = (y1 + y2) / 2;
        
        // get vector from start to end
        nx = x2 - x1;
        ny = y2 - y1;
        
        // find dist
        dist = Math.sqrt(nx * nx + ny * ny);
        
        // normalise vector
        nx /= dist;
        ny /= dist;
        
        // The next section has some optional behaviours
        // that set the dist from the line mid point to the arc mid point
        // You should only use one of the following sets
        
        //-- Uncomment for behaviour of arcs
        // This make the lines flatten at distance
        //b1 =  (bend * 300) / Math.pow(dist,1/4);

        //-- Uncomment for behaviour of arcs
        // Arc bending amount close to constant
        // b1 =  bend * dist * 0.5

        b1 = bend * dist

        // Arc amount bend more at dist
        x3 = mx + ny * b1;
        y3 = my - nx * b1;
    
        // get the radius
        radius = (0.5 * ((x1-x3) * (x1-x3) + (y1-y3) * (y1-y3)) / (b1));

        // use radius to get arc center
        cx = x3 - ny * radius;
        cy = y3 + nx * radius;

        // radius needs to be positive for the rest of the code
        radius = Math.abs(radius);

        


        // find angle from center to start and end
        a1 = Math.atan2(y1 - cy, x1 - cx);
        a2 = Math.atan2(y2 - cy, x2 - cx);
        
        // normalise angles
        a1 = (a1 + Math.PI * 2) % (Math.PI * 2);
        a2 = (a2 + Math.PI * 2) % (Math.PI * 2);
        // ensure angles are in correct directions
        if (bend < 0) {
            if (a1 < a2) { a1 += Math.PI * 2 }
        } else {
            if (a2 < a1) { a2 += Math.PI * 2 }
        }
        
        // convert arrow length to angular len
        arrowAng = aLen / radius  * Math.sign(bend);
        // get angular length of start and end circles and move arc start and ends
        
        a1 += startRadius / radius * Math.sign(bend);
        a2 -= endRadius / radius * Math.sign(bend);
        aa1 = a1;
        aa2 = a2;
    
        // check for too close and no room for arc
        if ((bend < 0 && a1 < a2) || (bend > 0 && a2 < a1)) {
            return;
        }
        // is there a start arrow
        if (sArrow) { aa1 += arrowAng } // move arc start to inside arrow
        // is there an end arrow
        if (eArrow) { aa2 -= arrowAng } // move arc end to inside arrow
        
        // check for too close and remove arrows if so
        if ((bend < 0 && aa1 < aa2) || (bend > 0 && aa2 < aa1)) {
            sArrow = false;
            eArrow = false;
            aa1 = a1;
            aa2 = a2;
        }
        // draw arc
        ctx.beginPath();
        ctx.strokeStyle = getColorNode(l.source.name);
        ctx.lineWidth = 2;
        ctx.globalAlpha = sizeLink(l.sizeLink)
        ctx.arc(cx, cy, radius, aa1, aa2, bend < 0);
        ctx.stroke();

        ctx.beginPath();
        
        // draw start arrow if needed
        if(sArrow){
            ctx.moveTo(
                Math.cos(a1) * radius + cx,
                Math.sin(a1) * radius + cy
            );
            ctx.lineTo(
                Math.cos(aa1) * (radius + aWidth / 2) + cx,
                Math.sin(aa1) * (radius + aWidth / 2) + cy
            );
            ctx.lineTo(
                Math.cos(aa1) * (radius - aWidth / 2) + cx,
                Math.sin(aa1) * (radius - aWidth / 2) + cy
            );
            ctx.closePath();
        }
        
        // draw end arrow if needed
        if(eArrow){
            ctx.moveTo(
                Math.cos(a2) * radius + cx,
                Math.sin(a2) * radius + cy
            );
            ctx.lineTo(
                Math.cos(aa2) * (radius - aWidth / 2) + cx,
                Math.sin(aa2) * (radius - aWidth / 2) + cy
            );
            ctx.lineTo(
                Math.cos(aa2) * (radius + aWidth / 2) + cx,
                Math.sin(aa2) * (radius + aWidth / 2) + cy
            );
            
            ctx.closePath();
        }
        ctx.fillStyle = getColorNode(l.source.name);
        ctx.fill();
    }

    
    update();

    d3.select("#GraphChart")
        .append("br")
    var table = d3.select("#GraphChart")
        .append("table")
        .attr("class","table")
    var thead = table
        .append("thead")
        .attr("class", "thead-dark")
        .append("tr")
    
    thead.append("th").attr("scope","col").text("Emisor / Receptor")

    for(var i in graph.nodes){
        thead.append("th").attr("scope","col").text(graph.nodes[i].name)
    }

    var tbody = table.append("tbody")
    //console.log(graph.link)
    for(var i in graph.nodes){
        var tr = tbody.append("tr")
        tr.append("th").attr("scope","row").text(graph.nodes[i].name)
        for(var y in graph.nodes){
            //console.log(graph.nodes[i].name + "-" +  graph.nodes[y].name)
            
            var dato = graph.link.find(l => (l["source"].name == graph.nodes[i].name && l["target"].name == graph.nodes[y].name))
            //console.log(dato)
            if (dato != undefined){
                tr.append("td").text(dato["sizeLink"])
            }else{
                tr.append("td").text(0)
            }
        }
    }
}