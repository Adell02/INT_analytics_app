from app.utils.graph_functions.functions import * 
from app.utils.graph_functions.consumption_vs_temp import *
from plotly.graph_objects import Figure


def serialize_figures(fig_vector):
    serialized_figures = []
    for idx,fig in enumerate(fig_vector):
        if type(fig) == Figure:
            fig.update_layout({'paper_bgcolor': 'rgba(0, 0, 0, 0)'},margin=dict(l=25, r=20, t=55, b=20))
            serialized_figures.append(fig.to_json())
        
    return serialized_figures
    
def generate_dashboard_graphics(df,vin=None):

    # Generate functions in order and add them to a figures vector
    
    with open('app/utils/graph_functions/dashboard_config.json',encoding="utf-8") as f:
        config = json.load(f)
    
    fig_vector = []

    for row in config:
        if row['child'] == True:
            for sub_row in row['child_config']:
                if sub_row['child'] == True:
                    for sub_sub_row in sub_row['child_config']:
                        if sub_sub_row['child'] == True:
                            print("Too complex layout")
                        else:
                            func_str = sub_sub_row["function"]+"("
                            for param in sub_sub_row["parameters"]:
                                if param == "Dataframe":
                                    func_str += "df"
                                elif param == "key_user":
                                    if vin:
                                        func_str += +",key_user='"+vin+"'"
                                    else:
                                        func_str += ",key_user=''"
                                elif type(sub_sub_row[param]) == list or type(sub_sub_row[param]) == bool:
                                    func_str += ","+param+"="+str(sub_sub_row[param])
                                elif type(sub_sub_row[param]) == str:
                                    func_str += ","+param+"='"+str(sub_sub_row[param])+"'"
                                
                            func_str += ")"           
                            fig = eval(func_str)                                                        
                            fig_vector.append(fig)
                else:
                    func_str = sub_row["function"]+"("
                    for param in sub_row["parameters"]:
                        if param == "Dataframe":
                            func_str += "df"
                        elif param == "key_user":
                            if vin:
                                func_str += ",key_user='"+vin+"'"
                            else:
                                func_str += ",key_user=''"
                        elif type(sub_row[param]) == list or type(sub_row[param]) == bool:
                            func_str += ","+param+"="+str(sub_row[param])
                        elif type(sub_row[param]) == str:
                            func_str += ","+param+"='"+str(sub_row[param])+"'"
                    func_str += ")"  
                    fig = eval(func_str)                                                        
                    fig_vector.append(fig)
                    
    serialized_figures = serialize_figures(fig_vector)

    return serialized_figures

def build_html(config_file:str):
    html_string = ""
    with open(config_file) as f:
        config = json.load(f)
    idx = 0
    for row in config:        
        if row['child']:
            html_string += '<div class="recuadro-'+row['height']+'-dashboard" style="display:flex;flex-direction:'+row['flex-direction']+'">'
            for sub_row in row['child_config']:
                if sub_row['child']:
                    html_string += '<div class="sub-container-'+sub_row['height']+' sub-recuadro-w'+str(sub_row['width'])+'" style="display:flex;flex-direction:'+sub_row['flex-direction']+'">'
                    for sub_sub_row in sub_row['child_config']:
                        if sub_sub_row['child']:
                            print("Too complex layout")
                        elif sub_sub_row['function'] != 'generate_note':
                            html_string += '<div class="sub-graph-container graph-container">'
                            #html_string += plots[idx]
                            #idx += 1
                            html_string += '</div>'

                    html_string += '</div>'
                elif sub_row['function'] != 'generate_note':
                    html_string += '<div class="graph-container recuadro-w'+str(sub_row['width'])+'">'
                    #html_string += plots[idx]
                    #idx += 1
                    html_string += '</div>'
            html_string += '</div>'   
    return html_string