# dash.py
from flask import Blueprint, render_template

from app.routes.auth import login_required
from app.graph_functions.generate_scatter import generate_scatter_plot

dash_bp = Blueprint('dash', __name__)

@dash_bp.route('/dashboard')
#@login_required
def dashboard():
    x_data = [1, 2, 3, 4, 5]
    y_data = [10, 11, 12, 13, 14]
    title = 'Sample Scatter Plot'
    plotly_plot = generate_scatter_plot(x_data, y_data, title)
    return render_template('dashboard.html', plotly_plot=plotly_plot)
    
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



