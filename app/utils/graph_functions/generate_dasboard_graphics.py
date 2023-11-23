
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
    
def build_run_function(element:dict,df,vin):
    func_str = element["function"]+"("
    for param in element["parameters"]:
        if param == "Dataframe":
            func_str += "df"
        elif param == "key_user":
            if vin:
                func_str += ",key_user='"+vin+"'"
            else:
                func_str += ",key_user=''"
        elif type(element[param]) == list or type(element[param]) == bool:
            func_str += ","+param+"="+str(element[param])
        elif type(element[param]) == str:
            func_str += ","+param+"='"+str(element[param])+"'"
        
    func_str += ")"           
    fig = eval(func_str)
    return fig

def generate_dashboard_graphics(config_file:str,df,vin=None):

    # Generate functions in order and add them to a figures vector    
    with open(config_file,encoding="utf-8") as f:
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
                            fig = build_run_function(sub_sub_row,df,vin)                                                        
                            fig_vector.append(fig)
                else:
                    fig = build_run_function(sub_row,df,vin)                                                        
                    fig_vector.append(fig)
                    
    serialized_figures = serialize_figures(fig_vector)

    return serialized_figures

def build_html(config_file:str,df,plots:list,vin=None):
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
                            html_string += '</div>'
                        else:
                            html_string += build_run_function(sub_sub_row,df,vin)
                        
                        idx += 1

                    html_string += '</div>'
                elif sub_row['function'] != 'generate_note':
                    html_string += '<div class="graph-container recuadro-w'+str(sub_row['width'])+'">'                    
                    html_string += '</div>'
                    idx += 1
                else:
                    html_string += build_run_function(sub_row,df,vin)
                    idx += 1
                
            html_string += '</div>'   
    return html_string