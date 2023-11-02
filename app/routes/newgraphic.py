from flask import Blueprint, render_template,request,url_for,session

from app.routes.auth import login_required
from app.database.seeder import *
from app.utils.account.token import *

from app.utils.graph_functions.functions import * 
from app.utils.graph_functions.consumption_vs_temp import *

import pyarrow as pa
import pyarrow.parquet as pq

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import statsmodels.api as sm
import os


newgraphic_bp = Blueprint('newgraphic', __name__)

@newgraphic_bp.route('/newgraphic', methods=["GET", "POST"])
@login_required
def new_graph():

    fig_vector="[]"
    if request.method == 'POST':
        graph_type = request.form['graph_type']
        graph_title =request.form['graph_title']
        graph_data_x =request.form['graph_data_x']
        graph_data_y =request.form['graph_data_y']

        parquet_file = "app/database/Database_Ray.parquet"
        table = pq.read_table(parquet_file)
        df = table.to_pandas()
        fig_vector = []

        if  graph_type == "none" :
            h
        elif graph_type == "Pie_Chart" :
            fig_vector.append(
            generate_pie_chart(
            df,
            [graph_data_x,graph_data_y],
            graph_title)
            )
        
        


        fig_vector[0].update_layout({'paper_bgcolor':'rgba(0,0,0,0)'} , margin=dict(l=20, r=20, t=55, b=20))
        fig_vector[0]=fig_vector[0].to_json()

    columns_list = ['City (km)','Sport (km)','Flow (km)','Sail (km)','Regen (km)',
                    'City energy (Wh)','Sport energy (Wh)','Flow energy (Wh)','City regen (Wh)','Sport regen (Wh)',
                    'Total energy (Wh)','Total regen (Wh)',
                    'End odometer','Min cell V','Max cell V',
                    'Total (km)','Avg temp','SoC delta (%)',
                    'Motor min T (°C)','Motor max T (°C)',
                    'Inv  min T (°C)','Inv max T (°C)']
    

    return render_template('newgraphic.html',columns_list=columns_list,plots=fig_vector)

