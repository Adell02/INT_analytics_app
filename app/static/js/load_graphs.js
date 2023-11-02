function load_graph(div_id,idx) {        
    var figure = JSON.parse(plot[idx]);
    figure.layout.width = containers[idx].offsetWidth;
    figure.layout.height = containers[idx].offsetHeight;

    Plotly.newPlot(div_id,figure.data,figure.layout);
}

function resize_graph(div_id,idx){
    var figure = document.getElementById(div_id)

    figure.layout.width = containers[idx].offsetWidth;
    figure.layout.height = containers[idx].offsetHeight;

    Plotly.react(figure,figure.data,figure.layout);
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

function resize_all(){
    // Iterate through each container
    for (let i = 0; i < graph_divs.length; i++) {    
        resize_graph(graph_divs[i].id,i)
    }  
}

function resize_cached_graph(figure,idx){
    figure.layout.width = containers[idx].offsetWidth;
    figure.layout.height = containers[idx].offsetHeight;

    Plotly.react(figure,figure.data,figure.layout);
}

function resize_cached_all(){
    // Iterate through each container
    for (let i = 0; i < containers.length; i++) {    
        var children_div = containers[i].children[0]
        resize_cached_graph(children_div,i)
    } 

}