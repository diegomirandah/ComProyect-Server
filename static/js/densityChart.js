function d3DensityChartBase() {

    var margin = {top: 30, right: 5, bottom: 30, left: 40},
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

function d3density(dataset) {
    Keypoints = dataset["Keypoints"]
    //console.log(Keypoints)

    

    //parametros
    var basics = d3DensityChartBase();
    var margin = basics.margin,
		width = basics.width,
	    height = basics.height,
		colorBar = basics.colorBar,
        Padding = basics.Padding,
        misc = basics.misc;

    var svg = d3.select("#DensityChart")
        .append("svg")
        .attr("viewBox", `0 0 ${width} ${height}`)
        .attr("id","DensityChartPlot");
    
    var box = [
        (width - margin.left - margin.right - (Padding*2))/2,
        ((height - margin.top - margin.bottom - Padding)/2)
    ]

    var x = d3.scaleLinear()
        .domain([0, 320])
        .range([0, box[0]]);
    var y = d3.scaleLinear()
        .domain([0, 240])
        .range([0, box[1]]);
    
    var xAxis1 = d3.axisBottom(x);
    var xAxis2 = d3.axisBottom(x);
    
    var yAxis1 = d3.axisLeft(y);
    var yAxis2 = d3.axisLeft(y);
    
    svg.append("text")
        .attr("x", width/2)
        .attr("y", misc.title)
        .attr("class","title")				
        .attr("text-anchor", "middle")
        .text("Densidad del movimiento de manos");
    
    //y axis
    svg.append("g")
      .attr("class", "y axis")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
      .call(yAxis1);
    svg.append("g")
      .attr("class", "y axis")
      .attr("transform", "translate(" + margin.left + "," + (box[1] + margin.top + Padding) + ")")
      .call(yAxis2);

    //x axis
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(" + (margin.left + Padding) + "," + ((height - margin.bottom) + Padding) + ")")
        .call(xAxis1)
    
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(" + (margin.left + Padding + box[0] + Padding) + "," + ((height - margin.bottom) + Padding) + ")")
        .call(xAxis2)
    
    var locate = [[0,0],[box[0] + Padding,0],[0,box[1]+Padding],[box[0]+Padding,box[1]+Padding]]
    for(var i in Keypoints){
        Keypoints[i].keypoints.forEach(element => {
            /* svg.append("circle")
                .attr("cx", margin.left + Padding + locate[i][0] + x(element.posture.Nariz[0]))
                .attr("cy", margin.top + locate[i][1] + y(element.posture.Nariz[1]))
                .attr("r", 3)
                .attr("fill-opacity",0.02)
                .attr("fill", "red"); */
            svg.append("text")
                .attr("x", margin.left + Padding + locate[i][0] + box[0]/2)
                .attr("y", margin.top + locate[i][1] + 5)
                .attr("text-anchor","middle")
                .text(dataset.nodes[i].name);
            svg.append("circle")
                .attr("cx", margin.left + Padding + locate[i][0] + x(element.posture.L_muneca[0]))
                .attr("cy", margin.top + locate[i][1] + y(element.posture.L_muneca[1]))
                .attr("r", 2)
                .attr("fill-opacity",0.03)
                .attr("fill", "green");
            svg.append("circle")
                .attr("cx", margin.left + Padding + locate[i][0] + x(element.posture.R_muneca[0]))
                .attr("cy", margin.top + locate[i][1] + y(element.posture.R_muneca[1]))
                .attr("r", 2)
                .attr("fill-opacity",0.03)
                .attr("fill", "blue");
            /* svg.append("circle")
                .attr("cx", margin.left + Padding + locate[i][0] + x(element.posture.L_Codo[0]))
                .attr("cy", margin.top + locate[i][1] + y(element.posture.L_Codo[1]))
                .attr("r", 3)
                .attr("fill-opacity",0.02)
                .attr("fill", "orange");
            svg.append("circle")
                .attr("cx", margin.left + Padding + locate[i][0] + x(element.posture.R_Codo[0]))
                .attr("cy", margin.top + locate[i][1] + y(element.posture.R_Codo[1]))
                .attr("r", 3)
                .attr("fill-opacity",0.02)
                .attr("fill", "pink"); */
        });
    }
};