# dash.py
from flask import Blueprint, render_template

from app.graph_functions.generate_scatter import generate_scatter_plot

dash_bp = Blueprint('dash', __name__)

@dash_bp.route('/dashboard')
def index():
    x_data = [1, 2, 3, 4, 5]
    y_data = [10, 11, 12, 13, 14]
    title = 'Sample Scatter Plot'
    plotly_plot = generate_scatter_plot(x_data, y_data, title)
    print(plotly_plot)
    return render_template('dashboard.html', plotly_plot=plotly_plot)
    
@dash_bp.route('/prueba')
def index_prueba():
    return render_template('template.html')
    