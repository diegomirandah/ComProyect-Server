
function d3TimeLineBase() {

    var margin = {top: 30, right: 5, bottom: 100, left: 80},
    width = 900,
    height = 550,
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

function d3TimeLine(dataset) {
    //console.log("print d3TimeLine")
    //console.log(dataset)

    //parametros
    var basics = d3TimeLineBase();
	var margin = basics.margin,
		width = basics.width,
	    height = basics.height,
		colorBar = basics.colorBar,
        barPadding = basics.barPadding,
        misc = basics.misc
        ;
    
    posturesColor = d3.scaleOrdinal(["#7fc97f","#beaed4","#fdc086","#ffff99","#386cb0","#f0027f","#bf5b17","#666666"])

    //vad_doa
    //console.log("vad_doa")
    vad_doa = dataset['vad_doa']
    interventions = dataset['interventions']
    postures = dataset['postures']

    listPostures = []
    maxTime = 0
    for(i in postures){
        for(j in postures[i].postures){
            start = new Date(postures[i].postures[j].start);
            end = new Date(postures[i].postures[j].end);
            c = (end.getTime() + start.getTime())/2;
            time = end.getTime() - c;
            maxTime = (time > maxTime ) ? time : maxTime;
            if (listPostures.find(element => element == postures[i].postures[j].posture) == null){
                listPostures.push(postures[i].postures[j].posture)
            }
        }
    }


    vad_doa.sort(function(a, b) {
        return a.endTime - b.endTime;
    });
    var maxDate = vad_doa[vad_doa.length - 1].endTime;

    vad_doa.sort(function(a, b) {
        return a.startTime - b.startTime;
    });
    var minDate = vad_doa[0].startTime;

    // var xScale = d3.scaleTime()
    // xScale.domain([maxDate, minDate]).nice();
    // xScale.range([margin.left, width - margin.right]);
    delta = new Date(maxDate).getTime() - new Date(minDate).getTime()

    var deltaTime = d3.scaleTime()
    .domain([new Date(minDate), new Date(maxDate)])
    .range([0, delta]);

    var x = d3.scaleTime()
    .domain([0, delta])
    .range([margin.left, width - margin.right]);

    var y = d3.scaleLinear()
    .domain([0, 100])
    .range([margin.top, height - margin.bottom]);
    

    // var xAxis = d3.axisBottom(xScale);
    var xAxis = d3.axisBottom(x)
    .ticks(10);

    var yAxis = d3.axisLeft(y)
    .ticks(0);

    var svg = d3.select("#TimeLineChart")
    .append("svg")
    //.attr("width",width)
    //.attr("height",height)
    .attr("viewBox", `0 0 ${width} ${height}`)
    .attr("id","TimeLineChartPlot");

    svg.append("text")
    .attr("x", (margin.left + width)/2)
    .attr("y", misc.title)
    .attr("class","title")				
    .attr("text-anchor", "middle")
    .text("Intervenciones en Actividad y postura cerrada");

    for(var i in dataset.nodes){
        index = parseInt(i) + 1 ;
        var bordesuperior = (100 / dataset.nodes.length) * parseInt(i) 
        var bordeinferior = (100 / dataset.nodes.length) * index
        var centro = (bordesuperior + bordeinferior) / 2 

        var radioTime = d3.scaleTime()
            .domain([0, maxTime])
            .range([2, centro]);

        svg.append("line")
            .attr("x1",x(0))
            .attr("y1",y(bordesuperior))
            .attr("x2",x(delta))
            .attr("y2",y(bordesuperior))
            .attr("stroke-dasharray","10, 5")
            .attr("style","stroke:#000; stroke-width:1;")

        svg.append("image")
            .attr("xlink:href", "https://github.com/favicon.ico")
            .attr("x", margin.left / 3)
            .attr("y", (y(centro) + y(bordesuperior)) / 2)
            .attr("width", 16)
            .attr("height", 16);

        svg.append("text")
            .attr("x", 0)
            .attr("y", (y(centro) + y(bordeinferior)) / 2)
            .attr("class","title")
            .text(dataset.nodes[i].name);

        var inter = interventions.filter(d => d.user == dataset.nodes[i].name);
        for(var q in inter){
            start = deltaTime(new Date(inter[q].start));
            end = deltaTime(new Date(inter[q].end));

            svg.append("rect")
            .attr("x", x(start))
            .attr("y", y(bordesuperior))
            .attr("height", y(bordeinferior) - y(bordesuperior) )
            .attr("width", x(end) -x(start))
            .attr("fill-opacity",0.5)
            .attr("fill", dataset.nodes[i].color);
        }

        var dataUser = vad_doa.filter(d => d.micPos == i);
         for (var d in dataUser){
            start = deltaTime(new Date(dataUser[d].startTime));
            end = deltaTime(new Date(dataUser[d].endTime));
            //console.log("start " + dataUser[d].startTime + " end " + dataUser[d].endTime)
            svg.append("rect")
            .attr("x", x(start))
            .attr("y", y(bordesuperior))
            .attr("height", y(bordeinferior) - y(bordesuperior) )
            .attr("width", x(end) -x(start))
            //.attr("width", x(new Date(end)) - x(new Date(start)))
            .attr("fill", dataset.nodes[i].color);
        } 

        var posturesByUser = postures.find(p => p.user == dataset.nodes[i].name);
        for(var q in posturesByUser.postures){
            //console.log(posturesByUser.postures[q])
            start = new Date(posturesByUser.postures[q].start);
            end = new Date(posturesByUser.postures[q].end);
            c = (end.getTime() + start.getTime())/2;
            cx = new Date(c);
            //console.log("start \n" + start + " end \n" + end + " media \n" + cx)
            svg.append("circle")
                .attr("cx", x(deltaTime(cx)))
                .attr("cy", (y(bordeinferior) + y(bordesuperior))/2)
                .attr("r", radioTime(end.getTime() - c))
                .attr("fill-opacity",0.7)
                .attr("fill", posturesColor(posturesByUser.postures[q].posture));
                
        }
    }

    //x axis
    svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(" + 0 + "," + (height - margin.bottom) + ")")
    .call(xAxis)

    //y axis
    svg.append("g")
      .attr("class", "y axis")
      .attr("transform", "translate(" + margin.left + "," + 0 + ")")
      .call(yAxis);
    
    if(listPostures != null || listPostures.length != 0){
        var p = 0;
        var xy = [40,height - 70]
        for (var j = 0; j < 4; j++) {
            for (var i = 0; i < 3; i++) {
                if(p >= listPostures.length){
                    j=3
                    i=3
                    break;
                }
                svg.append("circle")
                    .attr("cx", xy[0])
                    .attr("cy", xy[1])
                    .attr("r", 10)
                    .attr("fill-opacity",0.7)
                    .attr("fill", posturesColor(listPostures[p]));
                svg.append("text")
                    .attr("x", xy[0] + 10)
                    .attr("y", xy[1] + 3)
                    .text(listPostures[p]);
                xy[1]+=22
                p += 1
            }
            xy[1] = height - 70
            xy[0]+= 215
        }
    }
    d3.select("#TimeLineChart")
        .append("br")
    var table = d3.select("#TimeLineChart")
        .append("table")
        .attr("class","table")
    var thead = table
        .append("thead")
        .attr("class", "thead-dark")
        .append("tr")
    
    thead.append("th").attr("scope","col").text("#")

    for(var i in dataset.nodes){
        thead.append("th").attr("scope","col").text(dataset.nodes[i].name)
    }

    var row = ["Intevenciones","Duración Intervenciones"]
    var tbody = table.append("tbody")
    for(var i in row){
        var tr = tbody.append("tr")
        tr.append("th").attr("scope","row").text(row[i])
        if (row[i] == "Intevenciones"){
            for(var i in dataset.nodes){
                tr.append("td").text(dataset.nodes[i].interventions)
            }
        }
        if (row[i] == "Duración Intervenciones"){
            for(var i in dataset.nodes){
                tr.append("td").text(dataset.nodes[i].duration.slice(7,dataset.nodes[i].duration.length ))
            }
        }
            
        //<th scope="row">1</th>
    }
}