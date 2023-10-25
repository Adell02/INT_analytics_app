function load_graph(div_id,idx) {        
    var figure = JSON.parse(plot[idx]);
    figure.layout.width = containers[idx].offsetWidth;
    figure.layout.height = containers[idx].offsetHeight;

    Plotly.newPlot(div_id,figure.data,figure.layout);
}

function create_all(){
                
    // Iterate through each container
    for (let i = 0; i < containers.length; i++) {
        const container = containers[i];
    
        // Create an inner div for the graph
        const graphDiv = document.createElement("div");
        graphDiv.id = "plotly_graph_" + (i + 1);
        container.appendChild(graphDiv);
        graph_divs.push(graphDiv)
        load_graph(graphDiv,i)
    }  
}
function load_all(){

    // Iterate through each container
    for (let i = 0; i < graph_divs.length; i++) {    
        load_graph(graph_divs[i].id,i)
    }  
}