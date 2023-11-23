function downsampleData(trace, desiredDataPoints) {
    var new_trace = trace;
    var chunkSize = Math.ceil(trace.x.length / desiredDataPoints);
    var downsampledData = {x:[],y:[]};
    for (var i = 0; i < trace.x.length; i += chunkSize) {
        var chunk_x = trace.x.slice(i, i + chunkSize);
        var chunk_y = trace.y.slice(i, i + chunkSize);
        if (chunk_x.length) {
            var sumX = 0, sumY = 0;
            for (var j = 0; j < chunk_x.length; j++) {
                sumX += chunk_x[j];
                sumY += chunk_y[j];
            }      
            
            downsampledData.x.push(sumX / chunk_x.length);
            downsampledData.y.push(sumY / chunk_y.length );
        }
    }
    new_trace.x = [...downsampledData.x];
    new_trace.y = [...downsampledData.y];
    return new_trace;
}
function downsample(data, targetLength) {
    const x = data.x;
    const y = data.y;

    const xyData = x.map((val, i) => ({ x: val, y: y[i] }));

    const bins = [];
    const binSize = Math.ceil(x.length / targetLength);

    // Fill bins with values
    for (let i = 0; i < xyData.length; i++) {
        const binIndex = Math.floor(i / binSize);
        if (!bins[binIndex]) {
            bins[binIndex] = [];
        }
        bins[binIndex].push(xyData[i]);
    }

    // Reduce each bin to a single value based on the original distribution
    const downsampledData = bins.map(bin => {
        if (!bin || bin.length === 0) return undefined; // If empty bin

        // Sort the bin based on x values
        bin.sort((a, b) => a.x - b.x);

        // Calculate median y value for each x bin
        const midIndex = Math.floor(bin.length / 2);
        if (bin.length % 2 !== 0) {
            return { x: bin[midIndex].x, y: bin[midIndex].y }; // For odd number of values
        } else {
            const medianY = (bin[midIndex - 1].y + bin[midIndex].y) / 2; // For even number of values
            return { x: bin[midIndex].x, y: medianY };
        }
    });

    // Extract x and y values from downsampled data
    const downsampledX = downsampledData.map(d => d.x);
    const downsampledY = downsampledData.map(d => d.y);

    var new_trace = data;
    new_trace.x = downsampledX;
    new_trace.y = downsampledY;

    return new_trace;
}

function zoom_resample(div,original_traces,desiredDataPoints){
    var downsampledData = [];
    
    original_traces.forEach(function (trace) {
        if (trace.type === 'scatter') {
            var downsampled_trace = downsample(trace, desiredDataPoints);
            downsampledData.push(downsampled_trace);
        } else {
            downsampledData.push(trace);
        }
    });
    Plotly.react(div,downsampledData,div.layout);

}

function load_graph_optimized(div_id,idx,desiredDataPoints) {        
    var figure = JSON.parse(plot[idx]);

    figure.layout.width = containers[idx].offsetWidth;

    var downsampledData = [];

    figure.data.forEach(function (trace) {
        if (trace.type === 'scatter') {
            var downsampled_trace = downsample(trace, desiredDataPoints);
            downsampledData.push(downsampled_trace);
        } else {
            downsampledData.push(trace);
        }
    });

    Plotly.newPlot(div_id,downsampledData,figure.layout);

    var GraphDiv = document.getElementById(div_id);
    GraphDiv.on('plotly_relayout',
        function(eventdata){

            var start_x = eventdata['xaxis.range[0]'];
            var end_x = eventdata['xaxis.range[1]'];
            var start_y = eventdata['yaxis.range[0]'];
            var end_y = eventdata['yaxis.range[1]'];

            var new_traces = JSON.parse(plot[idx]).data;
            
            for (let i=0;i<new_traces.length;i++){

                if (new_traces[i].type == "scatter" && start_x != undefined && start_y != undefined){
                    x=[]
                    y=[]
                    for (let s=0;s<new_traces[i].x.length;s++){
                        if (new_traces[i].x[s]>start_x && new_traces[i].x[s]<end_x && new_traces[i].y[s]>start_y && new_traces[i].y[s]<end_y){
                            x.push(new_traces[i].x[s]);
                            y.push(new_traces[i].y[s]);
                        }
                    }
                    new_traces[i].x = [...x];
                    new_traces[i].y = [...y];
                }else if(new_traces[i].type == "scatter" && start_x != undefined){
                    x=[]
                    y=[]
                    for (let s=0;s<new_traces[i].x.length;s++){
                        if (new_traces[i].x[s]>start_x && new_traces[i].x[s]<end_x){
                            x.push(new_traces[i].x[s]);
                            y.push(new_traces[i].y[s]);
                        }
                    }
                    new_traces[i].x = [...x];
                    new_traces[i].y = [...y];
                } else if(new_traces[i].type == "scatter" && start_y != undefined){
                    x=[]
                    y=[]
                    for (let s=0;s<new_traces[i].x.length;s++){
                        if (new_traces[i].y[s]>start_y && new_traces[i].y[s]<end_y){
                            x.push(new_traces[i].x[s]);
                            y.push(new_traces[i].y[s]);
                        }
                    }
                    new_traces[i].x = [...x];
                    new_traces[i].y = [...y];
                }
                
            }
            zoom_resample(GraphDiv,new_traces,desiredDataPoints);
            
            
        }
    );
}

function load_graph(div_id,idx) {        
    var figure = JSON.parse(plot[idx]);

    figure.layout.width = containers[idx].offsetWidth;
    figure.layout.height = containers[idx].offsetHeight;

    Plotly.newPlot(div_id,figure.data,figure.layout);
}

function resize_graph(div_id,idx){
    var figure = document.getElementById(div_id);

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
    }  
}

function load_all(){

    // Iterate through each container
    for (let i = 0; i < graph_divs.length; i++) {    
        load_graph(graph_divs[i].id,i)
    }  
}

function load_all_optimized(){
    console.log(desiredDataPoints);

    // Iterate through each container
    for (let i = 0; i < graph_divs.length; i++) {    
        load_graph_optimized(graph_divs[i].id,i,desiredDataPoints)
    }  
}


// ANALYTICS

function load_graph_analytics(div_id,idx,idx_page) {        
    var figure = JSON.parse(plotFiltrado[idx_page]);
    figure.layout.width = containers[idx].offsetWidth;
    figure.layout.height = containers[idx].offsetHeight;

    Plotly.newPlot(div_id,figure.data,figure.layout);
}

function create_newgraphic(){
            
    const container = containers[0];

    // Create an inner div for the graph
    const graphDiv = document.createElement("div");
    graphDiv.id = "plotly_graph" ;
    container.appendChild(graphDiv);
    graph_divs.push(graphDiv)
    if (plot.length > 0){
        load_graph(graphDiv,0)
    }
        
}

function load_4(){
    const desiredDataPoints = 1000;

    // Iterate through each container
    for (let i = 0; i < 4; i++) {    
        if (pageIndex*4+i<plotFiltrado.length){
            load_graph_optimized_analytics(graph_divs[i].id,i,pageIndex*4+i,desiredDataPoints);
        }
        else{
            Plotly.purge(graph_divs[i]);
        }
        
    }  
    resize_all();
}

function resize_all(){
    // Iterate through each container
    for (let i = 0; i < graph_divs.length; i++) {    
        resize_graph(graph_divs[i].id,i)
    }  
}

function load_graph_optimized_analytics(div_id,idx,idx_page,desiredDataPoints) {        
    var figure = JSON.parse(plotFiltrado[idx_page]);

    figure.layout.width = containers[idx].offsetWidth;

    var downsampledData = [];

    figure.data.forEach(function (trace) {
        if (trace.type === 'scatter') {
            var downsampled_trace = downsample(trace, desiredDataPoints);
            downsampledData.push(downsampled_trace);
        } else {
            downsampledData.push(trace);
        }
    });

    Plotly.newPlot(div_id,downsampledData,figure.layout);

    var GraphDiv = document.getElementById(div_id);
    GraphDiv.on('plotly_relayout',
        function(eventdata){

            var start_x = eventdata['xaxis.range[0]'];
            var end_x = eventdata['xaxis.range[1]'];
            var start_y = eventdata['yaxis.range[0]'];
            var end_y = eventdata['yaxis.range[1]'];

            var new_traces = JSON.parse(plotFiltrado[idx_page]).data;
            
            for (let i=0;i<new_traces.length;i++){

                if (new_traces[i].type == "scatter" && start_x != undefined && start_y != undefined){
                    x=[]
                    y=[]
                    for (let s=0;s<new_traces[i].x.length;s++){
                        if (new_traces[i].x[s]>start_x && new_traces[i].x[s]<end_x && new_traces[i].y[s]>start_y && new_traces[i].y[s]<end_y){
                            x.push(new_traces[i].x[s]);
                            y.push(new_traces[i].y[s]);
                        }
                    }
                    new_traces[i].x = [...x];
                    new_traces[i].y = [...y];
                }else if(new_traces[i].type == "scatter" && start_x != undefined){
                    x=[]
                    y=[]
                    for (let s=0;s<new_traces[i].x.length;s++){
                        if (new_traces[i].x[s]>start_x && new_traces[i].x[s]<end_x){
                            x.push(new_traces[i].x[s]);
                            y.push(new_traces[i].y[s]);
                        }
                    }
                    new_traces[i].x = [...x];
                    new_traces[i].y = [...y];
                } else if(new_traces[i].type == "scatter" && start_y != undefined){
                    x=[]
                    y=[]
                    for (let s=0;s<new_traces[i].x.length;s++){
                        if (new_traces[i].y[s]>start_y && new_traces[i].y[s]<end_y){
                            x.push(new_traces[i].x[s]);
                            y.push(new_traces[i].y[s]);
                        }
                    }
                    new_traces[i].x = [...x];
                    new_traces[i].y = [...y];
                }
                
            }
            zoom_resample(GraphDiv,new_traces,desiredDataPoints);
            
            
        }
    );
}

function filtrarPlot() {
    plotFiltrado=[];
    let typeFilter = document.getElementById('graph_type').value;
    let dataFilter = document.getElementById('graph_data_x').value; 
    let userInput = document.getElementById('userInput').value.trim().toLowerCase();
    console.log(userInput);
    let userWords = userInput ? userInput.split(" ") : [];
    
    
    
    
    for (let i = 0; i < plot.length; i++) {
        let elemento = JSON.parse(plot[i]);
        let cumpleCondicionvariable = false;
        let cumpleCondiciontype = false;
        let cumplePalabrasUsuario = userWords.length === 0 ? true : userWords.every(word => 
        elemento.layout && elemento.layout.title && elemento.layout.title.text && elemento.layout.title.text.toLowerCase().includes(word));
        console.log(cumplePalabrasUsuario)
        
        for (let y = 0; y < elemento.data.length; y++) {
            //pongo el or porqueen algunas graficas no se llamama label, sino name
            if ((elemento.data[y] && elemento.data[y].labels && elemento.data[y].labels.includes(dataFilter)) || (elemento.data[y] && elemento.data[y].name && elemento.data[y].name.includes(dataFilter))) { // Añado elemento.data[y] && elemento.data[y].labels && para verificar que la posicion que busco exista
                cumpleCondicionvariable = true;
            }
            if (elemento.data[y] && elemento.data[y].type === typeFilter) {
                cumpleCondiciontype = true;
            }
            
        }
        
        if (typeFilter==="none" && dataFilter==="none" && userWords.length === 0){
            plotFiltrado=[...plot];
        }
        else if ((typeFilter !== "none" && dataFilter!=="none" && userWords.length !== 0)){

            if (cumpleCondiciontype && cumpleCondicionvariable && cumplePalabrasUsuario) {
                plotFiltrado.push(plot[i]);
            } 
        }
        else {
            if ( typeFilter === "none" && dataFilter ==="none"){
                if (cumplePalabrasUsuario){
                    plotFiltrado.push(plot[i]);
                }
            }
            else if (typeFilter === "none"){
                if (cumpleCondicionvariable && cumplePalabrasUsuario){
                    plotFiltrado.push(plot[i]);
                }

            }
            else if(dataFilter==="none"){
                if (cumpleCondiciontype && cumplePalabrasUsuario){
                    plotFiltrado.push(plot[i]);
                }

            }
            else if(userWords.length === 0){
                if (cumpleCondiciontype && cumpleCondicionvariable){
                    plotFiltrado.push(plot[i]);
                }
                
            }
            

        }
        
    }
    console.log(plotFiltrado);
    pageIndex=0;
    load_4();
    
}
