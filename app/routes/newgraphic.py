from flask import Blueprint, render_template,request
from plotly.graph_objects import Pie

from app.routes.auth import login_required
from app.database.seeder import *
from app.utils.account.token import *

from app.utils.graph_functions.plots_generation import *
from app.utils.graph_functions.consumption_vs_temp import *
from app.utils.DataframeManager.load_df import generate_df_name, load_current_df_memory

import pyarrow.parquet as pq


newgraphic_bp = Blueprint('newgraphic', __name__)

@newgraphic_bp.route('/newgraphic', methods=["GET", "POST"])
@login_required
def new_graph():

    fig_vector=[]
    config=["none","","","",""]

    df = load_current_df_memory()
    full_df = df
    available_vin = list(df['Id'].keys().unique())  

    columns_list=list(df.columns)

    
    
    if request.method == 'POST':
        graph_type = request.form['graph_type']
        VIN_select = request.form['VIN_selector']
        graph_title =request.form['graph_title']
        graph_data_x =request.form['graph_data_x']
        graph_data_y=request.form['graph_data_y']
        trendline_select = request.form.get('trendline')
        trendline_global_select = request.form.get("trendline_global")
  
        if VIN_select != "":            
            df = df[df.index == VIN_select]

        if trendline_select:
            trendline_check = True
        else:
            trendline_check=False
        
        if trendline_global_select:
            trendline_global_check = True
        else:
            trendline_global_check = False
        
        if trendline_global_select is None:
            trendline_global_select = "false"
        if trendline_select is None:
            trendline_select = "false"

        config=[graph_type, graph_title, graph_data_x,graph_data_y, VIN_select,trendline_select,trendline_global_select]

        fig_vector = []

        if  (graph_type == "none" or graph_data_y=="") or ((graph_type == "Bar_Chart" or graph_type == "Scatter_Plot" or graph_type == "Line_Chart") and graph_data_x == ""):
            pass
        else:
            graph_data_y = graph_data_y.split(",")
            graph_data_y = [var.strip() for var in graph_data_y]

            if set(graph_data_y).issubset(set(columns_list)):

                if graph_type == "Pie_Chart":
                
                    fig_vector.append(
                        generate_pie_chart(
                        df,
                        graph_data_y,
                        graph_title)
                    )
                elif graph_type == "Bar_Chart"  and graph_data_x!="":
                    fig_vector.append(
                        generate_bar_chart(
                        df,
                        graph_data_x,graph_data_y,
                        graph_title)
                    )
    
                elif graph_type == "Histogram_Distribution" :  
                
                    start_index = graph_data_y[0].find("(")
                    end_index = graph_data_y[0].find(")")
                    if start_index != -1 and end_index != -1:
                        units = graph_data_y[0][start_index + 1: end_index]
                    else :
                        units=""
    
                    fig_vector.append(
                        generate_multi_histogram(
                        df,
                        graph_data_y,units,-200,200,10,
                        graph_title)
                    )
    
                elif graph_type == "Scatter_Plot" and graph_data_x!="":
                    fig_vector.append(
                        generate_scatter_plot_user(
                        full_df,VIN_select,
                        graph_data_x,graph_data_y,
                        graph_title, trendline_check,trendline_global_check)
                    )
    
                elif graph_type == "Line_Chart" and graph_data_x!="":
                    fig_vector.append(
                        generate_line_chart(
                        df,
                        graph_data_x,graph_data_y,
                        graph_title)
                    )
                
                elif graph_type =="Box_Plot":
                    fig_vector.append(
                        generate_box_plot(
                            df,
                            graph_data_y,
                            graph_title
                        )
                    )
    
                fig_vector[0].update_layout({'paper_bgcolor': 'rgba(0, 0, 0, 0)'},margin=dict(l=25, r=20, t=55, b=20),legend = dict(bgcolor = 'white'))
                
                if type(fig_vector[0].data[0]) != Pie:
                    fig_vector[0].update_layout(showlegend=True,legend=dict(
                        yanchor="top",
                        y=0.99,
                        xanchor="right",
                        x=0.99
                ))
                fig_vector[0]=fig_vector[0].to_json()

    return render_template('newgraphic.html',columns_list=columns_list,plots=fig_vector, config=config, available_vin=available_vin)

