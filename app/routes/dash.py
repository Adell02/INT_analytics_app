# dash.py
import os
from flask import Blueprint, render_template,url_for,request,session
import zlib
import requests,json

from app.routes.auth import login_required
from app.utils.graph_functions.generate_scatter import generate_scatter_plot
from app.utils.account.token import generate_token
from app.utils.DataframeManager.load_df import generate_cache_dash_name,load_current_df_memory
from app.utils.graph_functions.generate_dasboard_graphics import build_html


dash_bp = Blueprint('dash', __name__)

@dash_bp.route('/dashboard',methods=['POST','GET'])
@login_required
def dashboard():
    dataframe = load_current_df_memory()
    available_vin = list(dataframe['Id'].keys().unique())    

    default_vin = ''

    if request.method == 'POST':
        VIN_selected = request.form['VIN_selector']
        
        session['Optimization'] = request.form['Optimization']
            
        if VIN_selected != '':
            token_cache = generate_token("dash_from_vin_admin")
            url_cache_dashboard = url_for("rest_api.compute_dash_from_VIN",token=token_cache,vin=VIN_selected,_external=True)
            plots = json.loads(requests.get(url_cache_dashboard).content.decode('utf-8'))
            default_vin = VIN_selected
            return render_template('dashboard.html', plots=plots,available_vin=available_vin,default_vin=default_vin)  

    cached_path = generate_cache_dash_name()
    if os.path.isfile(cached_path):
        with open(cached_path, "rb") as file:
            cached = file.read()
        dashboard = json.loads(zlib.decompress(cached).decode('utf-8'))
    else:        
        token_cache = generate_token("cache_dashboard_admin")
        url_cache_dashboard = url_for("rest_api.cache_dashboard",token=token_cache,_external=True)
        plots = json.loads(requests.get(url_cache_dashboard).content.decode('utf-8'))

    html_string = build_html('app/utils/graph_functions/dashboard_config.json')

    return render_template('dashboard.html', html_string = html_string, plots=plots,available_vin=available_vin,default_vin=default_vin)
    


@dash_bp.route('/mapview')
@login_required
def mapview():
    return render_template('mapview.html')


@dash_bp.route('/analytics')
@login_required
def analytics():

    plots = []
    x_prueba=[1,2,3,4,5]
    y_prueba=[1,2,3,4,5]
    title_prueba='Prueba 1'
    plotly_plot = generate_scatter_plot(x_prueba, y_prueba, title_prueba)
    plots.append(plotly_plot)
    x_prueba2=[1,2,3,4,5]
    y_prueba2=[5,4,3,2,1]
    title_prueba2='Prueba 2'
    plotly_plot2 = generate_scatter_plot(x_prueba2, y_prueba2, title_prueba2)
    plots.append(plotly_plot2)
    x_prueba3=[1,2,3,4,5]
    y_prueba3=[1,2,3,2,1]
    title_prueba3='Prueba 3'
    plotly_plot3 = generate_scatter_plot(x_prueba3, y_prueba3, title_prueba3)
    plots.append(plotly_plot3)
    x_prueba4=[1,2,3,4,5]
    y_prueba4=[5,4,3,4,5]
    title_prueba4='Prueba 4'
    plotly_plot4 = generate_scatter_plot(x_prueba4, y_prueba4, title_prueba4)
    plots.append(plotly_plot4)
    x_prueba4=[1,2,3,4,5]
    y_prueba4=[1,1,1,1,1]
    title_prueba4='Prueba 5'
    plotly_plot4 = generate_scatter_plot(x_prueba4, y_prueba4, title_prueba4)
    plots.append(plotly_plot4)

    return render_template('analytics.html',plots=plots)



