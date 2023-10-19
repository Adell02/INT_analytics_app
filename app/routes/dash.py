# dash.py
from flask import Blueprint, render_template,Response,session
import pandas as pd
import zlib

from app.routes.auth import login_required
from app.utils.graph_functions.generate_scatter import generate_scatter_plot

dash_bp = Blueprint('dash', __name__)

@dash_bp.route('/dashboard')
#@login_required
def dashboard():
    #df = pd.read_excel("E:/GitCode/INT_data_analysis/Ray 7.7_statistics_23-07.xlsx","G2")

    #y_data = df['Max speed']
    #x_data = df['Timestamp']
    #title = 'Max Speed vs Timestamp'
    #plotly_plot = generate_scatter_plot(x_data, y_data, title)
    #compressed_plot = zlib.compress(plotly_plot.encode('utf-8'),level=zlib.Z_BEST_COMPRESSION)
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
    
    return render_template('dashboard.html', username = "Ari",plots=plots)
    #session['user_email'].split("@")[0]

@dash_bp.route('/prueba')
@login_required
def index_prueba():
    return render_template('template.html')

@dash_bp.route('/mapview')
#@login_required
def mapview():
    return render_template('dashboard.html')

@dash_bp.route('/newgraphic')
@login_required
def newgraphic():
    return render_template('newgraphic.html')


@dash_bp.route('/analytics')
#@login_required
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

    return render_template('analytics.html',plots=plots)


@dash_bp.route('/settings')
#@login_required
def settings():
    return render_template('settings.html',email=session['user_email'], personal_token=session['personal_token'] , entity_name=session['org_name'], entity_token=session['external_token'])



