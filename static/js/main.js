queue()
    .defer(d3.json, dataUrl)
    .await(ready);

function ready(error, dataset) {
    color = d3.scaleOrdinal(d3.schemeCategory10)
    for (var i in dataset["nodes"]){
        dataset["nodes"][i].color = color(i)
    }
    d3TimeLine(dataset)
    d3GraphChart(dataset)
    d3ViolinChart(dataset)
    d3density(dataset)
    d3RadialBar(dataset)
}