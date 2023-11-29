import json
from app.utils.graph_functions.parse_json_functions import serialize_figures,build_run_function


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
            html_string += '<div class="recuadro-h'+ str(row['height'])+'" style="display:flex;flex-direction:'+str(row['flex-direction'])+'">'
            for sub_row in row['child_config']:
                if sub_row['child']:
                    html_string += '<div class="sub-recuadro-h'+str(sub_row['height'])+' sub-recuadro-w'+str(sub_row['width'])+'" style="display:flex;flex-direction:'+str(sub_row['flex-direction'])+'">'
                    for sub_sub_row in sub_row['child_config']:
                        if sub_sub_row['child']:
                            print("Too complex layout")
                        elif sub_sub_row['function'] != 'generate_note':
                            html_string += '<div class="graph-container sub-recuadro-h'+ str(sub_sub_row['height'])+' sub-recuadro-w'+str(sub_sub_row['width'])+'">'
                            
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