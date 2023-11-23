from flask import Blueprint, render_template,request

from app.routes.auth import login_required
from app.database.seeder import *
from app.utils.account.token import *

from app.utils.graph_functions.functions import * 
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
    available_vin = list(df['Id'].keys().unique())  

    columns_list=df_get_columns_tag(df)

    
    
    if request.method == 'POST':
        graph_type = request.form['graph_type']
        graph_title =request.form['graph_title']
        graph_data_x =request.form['graph_data_x']
        graph_data_y=request.form.getlist('graph_data_y[]')
        VIN_select = request.form['VIN_select']

        
        if VIN_select != "":
            df = df[df.index == VIN_select]


        
        if request.form.get('trendline'):
            trendline_check = True
        else:
            trendline_check=False

        config=[graph_type, graph_title, graph_data_x,graph_data_y, VIN_select]

        
        fig_vector = []

        if  graph_type == "none" or len(graph_data_y)==0 or graph_data_y[0]=="" or graph_data_x=="":
            pass
        else :
            
            if graph_type == "Pie_Chart" :

                fig_vector.append(
                    generate_pie_chart(
                    df,
                    graph_data_y,
                    graph_title)
                )
            elif graph_type == "Bar_Chart" :
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

            elif graph_type == "Scatter_Plot":
                fig_vector.append(
                    generate_scatter_plot_user(
                    df,"",
                    graph_data_x,graph_data_y,
                    graph_title, False,trendline_check)
                )

            elif graph_type == "Line_Chart":
                fig_vector.append(
                    generate_line_chart(
                    df,
                    graph_data_x,graph_data_y,
                    graph_title)
                )

            fig_vector[0].update_layout({'paper_bgcolor':'rgba(0,0,0,0)'} , margin=dict(l=20, r=20, t=55, b=20))
            fig_vector[0]=fig_vector[0].to_json()
        
    

    
    

    return render_template('newgraphic.html',columns_list=columns_list,plots=fig_vector, config=config, available_vin=available_vin)

