import json

from app.utils.graph_functions.parse_json_functions import serialize_figures,build_run_function

def generate_analytics_graphics(config_file,df):
    with open(config_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    fig_vector = []
    for f in data:
        fig = build_run_function(f,df,vin="")                                                        
        fig_vector.append(fig)
    serialized_vector = serialize_figures(fig_vector)

    return serialized_vector