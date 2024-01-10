from plotly.graph_objects import Figure,Pie
from app.utils.graph_functions.plots_generation import *
from app.utils.graph_functions.consumption_vs_temp import *
from app.utils.graph_functions.analytic_functions import *



def serialize_figures(fig_vector):
    serialized_figures = []
    for idx,fig in enumerate(fig_vector):
        if type(fig) == Figure:
            fig.update_layout({'paper_bgcolor': 'rgba(0, 0, 0, 0)'},margin=dict(l=25, r=20, t=55, b=20),legend = dict(bgcolor = 'white'))
            
            if type(fig.data[0]) != Pie:
                fig.update_layout(showlegend=True,legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="right",
                    x=0.99
            ))
            serialized_figures.append(fig.to_json())
                
    return serialized_figures
    
def build_run_function(element:dict,df,vin):    
    if element["function"] == "generate_scatter_plot_user":
        from app.utils.DataframeManager.load_df import load_current_df_memory
        df = load_current_df_memory()

    func_str = element["function"]+"("
    for param in element["parameters"]:
        if param == "dataframe":
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