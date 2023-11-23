from flask import Blueprint, render_template

from app import Config
from app.routes.auth import login_required
from app.utils.graph_functions.generate_dasboard_graphics import generate_dashboard_graphics
from app.utils.DataframeManager.load_df import load_current_df_memory


analytics_bp = Blueprint("analytics",__name__)

@analytics_bp.route('/analytics')
@login_required
def analytics():
    columns_list = ['City (km)','Sport (km)','Flow (km)','Sail (km)','Regen (km)',
                    'City energy (Wh)','Sport energy (Wh)','Flow energy (Wh)','City regen (Wh)','Sport regen (Wh)',
                    'Total energy (Wh)','Total regen (Wh)',
                    'End odometer','Min cell V','Max cell V',
                    'Total (km)','Avg temp','SoC delta (%)',
                    'Motor min T (°C)','Motor max T (°C)',
                    'Inv  min T (°C)','Inv max T (°C)']
    dataframe = load_current_df_memory()

    plots=generate_dashboard_graphics(Config.PATH_DASHBOARD_CONFIG,dataframe)

    return render_template('analytics.html',plots=plots, columns_list=columns_list)
