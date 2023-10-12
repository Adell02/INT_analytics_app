# dash.py
from flask import Blueprint, render_template,Response,session
import pandas as pd
import zlib

from app.routes.auth import login_required
from app.utils.graph_functions.generate_scatter import generate_scatter_plot

dash_bp = Blueprint('dash', __name__)

@dash_bp.route('/dashboard')
@login_required
def dashboard():
    #df = pd.read_excel("E:/GitCode/INT_data_analysis/Ray 7.7_statistics_23-07.xlsx","G2")

    #y_data = df['Max speed']
    #x_data = df['Timestamp']
    
    title = 'Max Speed vs Timestamp'
    #plotly_plot = generate_scatter_plot(x_data, y_data, title)
    #compressed_plot = zlib.compress(plotly_plot.encode('utf-8'),level=zlib.Z_BEST_COMPRESSION)

    return render_template('dashboard.html', username = session['user_email'].split("@")[0],plotly_plot="")
    
@dash_bp.route('/prueba')
@login_required
def index_prueba():
    return render_template('template.html')
@dash_bp.route('/mapview')
#@login_required
def mapview():
    return render_template('dashboard.html')


@dash_bp.route('/analytics')
#@login_required
def analytics():
    return render_template('analytics.html')


@dash_bp.route('/settings')
#@login_required
def settings():
    return render_template('settings.html')



