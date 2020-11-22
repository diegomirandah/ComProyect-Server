function d3RadialBarChartBase() {

    var margin = {top: 30, right: 5, bottom: 30, left: 50},
    width = 500 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom,
    colorBar = d3.scaleOrdinal(d3.schemeCategory10),
    Padding = 10,
    misc = {ylabel: 7, xlabelH : 5, title:11};
    
    return {
        margin : margin, 
        width : width, 
        height : height, 
        colorBar : colorBar, 
        Padding : Padding,
        misc: misc
    };
}


function d3RadialBar(dataset) {
    console.log(dataset.dataposture)
    console.log(dataset.postures)

    var data = {}
    max = 0
    for(var i in dataset.dataposture){
        data[i] = { 
            "total": dataset.dataposture[i],
        }
        if (max < dataset.dataposture[i]){
            max = dataset.dataposture[i];
        }
        for(var j in dataset.postures){
            //console.log(dataset.postures[j].data[i])
            data[i][dataset.postures[j].user] = dataset.postures[j].data[i];
        }
    }
    
    console.log(data)

    //parametros
    var basics = d3RadialBarChartBase();
    var margin = basics.margin,
		width = basics.width,
	    height = basics.height,
		colorBar = basics.colorBar,
        Padding = basics.Padding,
        misc = basics.misc,
        innerRadius = 5,
        outerRadius = Math.min(width, height) / 2.3;
        
    var svg = d3.select("#RadialBarChart")
        .append("svg")
        .attr("viewBox", `0 0 ${width} ${height}`)
        .attr("id","RadialBarChartPlot");
    var g = svg.append("g").attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
    
    postureList = Object.keys(dataset["dataposture"]);
    var x = d3.scaleBand()
    .domain(postureList)
    .range([0, 2 * Math.PI])
    .align(0)
    
    var y = d3.scaleLinear()
    .domain([0, max])
    .range([innerRadius, outerRadius*0.99]);
    
    var z = d3.scaleOrdinal()
    .range(["#a1d76a", "#91bfdb"]);
    
    var zClasses = ['внутренняя сторона', 'внешняя сторона'];

    for(var i in postureList){
        g.call(g => g.append("g")	
            .attr("text-anchor", "middle")
            .attr("transform", "rotate(" + ((x(postureList[i]) + x.bandwidth() / 2) * 180 / Math.PI - 90) + ") translate(" + outerRadius + ",0)")
            .append("text")
            .attr("transform", "rotate(90)")
            .text(postureList[i]));
    }
    for(var i in data){
        console.log(i)
        sum = 0
        for(var j in data[i]){
            if( j != "total" && data[i][j] != undefined){
                g.call(g => g.append("path")
                    .attr("d", d3.arc()
                        .innerRadius(y(sum))
                        .outerRadius(y(sum + data[i][j]))
                        .startAngle(x(i)) 
                        .endAngle(x(i) + x.bandwidth())
                        .padAngle(0.01))
                    .attr("transform", "translate(0,0)")
                    .attr("fill",dataset["nodes"].find(n => n.name == j).color))
                sum += data[i][j];
            }
        }
        console.log(sum)
        
    }
};



