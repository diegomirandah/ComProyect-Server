

var margin = {top: 20, right: 30, bottom: 30, left: 40},
    width = 460 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;


function d3ViolinChart(dataset) {
    var svg = d3.select("#ViolinhChart")
        .append("svg")
            .attr("viewBox", `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
        .append("g")
            .attr("transform",
                "translate(" + margin.left + "," + margin.top + ")");

    svg.append("text")
        .attr("x", (margin.left + width)/2)
        .attr("y", 5)
        .attr("class","title")				
        .attr("text-anchor", "middle")
        .text("Distribución de las intervenciones en función del tiempo");
    
    interventions = dataset['interventions']
    data = []
    for(var i in interventions){
        data.push({
            user: interventions[i].user,
            time: new Date(interventions[i].end).getTime() - new Date(interventions[i].start).getTime()
        })
    }

    data.sort(function(a, b) {
        return a.time - b.time;
    });
    var maxDate = data[data.length - 1].time;
    
    // Build and Show the Y scale
    var y = d3.scaleLinear()
        .domain([0, maxDate ])          // Note that here the Y scale is set manually
        .range([height, margin.top])
    svg.append("g").call( d3.axisLeft(y) )
    
    // Build and Show the X scale. It is a band scale like for a boxplot: each group has an dedicated RANGE on the axis. This range has a length of x.bandwidth
    var x = d3.scaleBand()
        .range([ 0, width ])
        .domain(["Usuario 1","Usuario 2", "Usuario 3", "Usuario 4"])
        .padding(0.05)     // This is important: it is the space between 2 groups. 0 means no padding. 1 is the maximum.
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x))
    
    // Features of the histogram
    var histogram = d3.histogram()
            .domain(y.domain())
            .thresholds(y.ticks(20))    // Important: how many bins approx are going to be made? It is the 'resolution' of the violin plot
            .value(d => d)
    
    // Calcule el agrupamiento para cada grupo del conjunto de datos
    var sumstat = d3.nest()  // La función de nido permite agrupar el cálculo por nivel de un factor.
        .key(function(d) { return d.user;})
        .rollup(function(d) {   // Para cada clave ...
        input = d.map(function(g) { return g.time;})    // Mantenga la variable llamada time
        bins = histogram(input)   // Y calcule el binning en él.
        return(bins)
        })
        .entries(data)
    
    var sumstat2 = d3.nest() // nest function allows to group the calculation per level of a factor
        .key(function(d) { return d.user;})
        .rollup(function(d) {
          q1 = d3.quantile(d.map(function(g) { return g.time;}).sort(d3.ascending),.25)
          median = d3.quantile(d.map(function(g) { return g.time;}).sort(d3.ascending),.5)
          q3 = d3.quantile(d.map(function(g) { return g.time;}).sort(d3.ascending),.75)
          interQuantileRange = q3 - q1
          min = q1 - 1.5 * interQuantileRange
          max = q3 + 1.5 * interQuantileRange
          return({q1: q1, median: median, q3: q3, interQuantileRange: interQuantileRange, min: min, max: max})
        })
        .entries(data)
    
    // ¿Cuál es la mayor cantidad de valor en un contenedor? Lo necesitamos porque este valor tendrá un ancho del 100% del ancho de banda.
    var maxNum = 0
    for ( i in sumstat ){
        sumstat[i].color = dataset.nodes.find(element => element.name == sumstat[i].key).color
        allBins = sumstat[i].value
        lengths = allBins.map(function(a){return a.length;})
        longuest = d3.max(lengths)
        if (longuest > maxNum) { maxNum = longuest }
    }
    
    // El ancho máximo de un violín debe ser x.bandwidth = el ancho dedicado a un grupo
    var xNum = d3.scaleLinear()
        .range([0, x.bandwidth()])
        .domain([-maxNum,maxNum])
    
    //¡Agrega la forma a este svg!
    svg
        .selectAll("myViolin")
        .data(sumstat)
        .enter()        // Entonces ahora somos grupo de trabajo por grupo
        .append("g")
        .attr("transform", function(d){ return("translate(" + x(d.key) +" ,0)") } ) // Traducción a la derecha para estar en la posición del grupo
        .append("path")
            .style("fill",function(d){ return(d.color)})
            .datum(function(d){ return(d.value)})     // Así que ahora estamos trabajando bin por bin
            .style("stroke", "none")
            .attr("d", d3.area()
                .x0(function(d){ return(xNum(-d.length)) } )
                .x1(function(d){ return(xNum(d.length)) } )
                .y(function(d){ return(y(d.x0)) } )
                .curve(d3.curveCatmullRom)    // Esto hace que la línea sea más suave para darle apariencia al violín. Prueba d3.curveStep para ver la diferencia
            )
        
    // Show the main vertical line
    svg
        .selectAll("vertLines")
        .data(sumstat2)
        .enter()
        .append("line")
            .attr("x1", function(d){return(x(d.key) + x.bandwidth()/2)} )
            .attr("x2", function(d){return(x(d.key) + x.bandwidth()/2)} )
            .attr("y1", function(d){return(y(d.value.min))})
            .attr("y2", function(d){return(y(d.value.max))})
            .attr("stroke", "black")
            .style("width", 10)
    // rectangle for the main box
    var boxWidth = 10
    svg
        .selectAll("boxes")
        .data(sumstat2)
        .enter()
        .append("rect")
            .attr("x", function(d){return(x(d.key) - (boxWidth/2) + (x.bandwidth()/2) )})
            .attr("y", function(d){return(y(d.value.q3))})
            .attr("height", function(d){return(y(d.value.q1)-y(d.value.q3))})
            .attr("width", boxWidth )
            .attr("stroke", "black")
            .style("fill", "#69b3a2")
    // Show the median
    svg
        .selectAll("medianLines")
        .data(sumstat2)
        .enter()
        .append("line")
            .attr("x1", function(d){return(x(d.key) - boxWidth/2 + (x.bandwidth()/2)) })
            .attr("x2", function(d){return(x(d.key) + boxWidth/2 + (x.bandwidth()/2)) })
            .attr("y1", function(d){return(y(d.value.median))})
            .attr("y2", function(d){return(y(d.value.median))})
            .attr("stroke", "black")
            .style("width", 80)
}