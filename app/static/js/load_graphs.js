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

function load_graph_analytics(div_id,idx,idx_page) {        
    var figure = JSON.parse(plot[idx_page]);
    figure.layout.width = containers[idx].offsetWidth;
    figure.layout.height = containers[idx].offsetHeight;

    Plotly.newPlot(div_id,figure.data,figure.layout);
}

function load_4(){

    // Iterate through each container
    for (let i = 0; i < 4; i++) {    
        if (pageIndex*4+i<plot.length){
            load_graph_analytics(graph_divs[i].id,i,pageIndex*4+i);
        }
        else{
            Plotly.purge(graph_divs[i]);
        }
        
    }  
}

function resize_all(){
    // Iterate through each container
    for (let i = 0; i < graph_divs.length; i++) {    
        resize_graph(graph_divs[i].id,i)
    }  
}