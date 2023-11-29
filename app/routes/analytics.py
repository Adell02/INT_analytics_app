import os
import json
import zlib
from flask import Blueprint, render_template

from app import Config
from app.routes.auth import login_required
from app.utils.DataframeManager.load_df import load_current_df_memory,generate_cache_analytics_name
from app.routes.RESTful_API import cache_analytics


analytics_bp = Blueprint("analytics",__name__)

@analytics_bp.route('/analytics')
@login_required
def analytics():
    
    dataframe = load_current_df_memory()
    columns_list = dataframe.columns

    cached_path = generate_cache_analytics_name()
    if os.path.isfile(cached_path):
        with open(cached_path, "rb") as file:
            cached = file.read()
        plots = json.loads(zlib.decompress(cached).decode('utf-8'))
    else:        
        plots = cache_analytics(Config.SERVER_TOKEN)    

    return render_template('analytics.html',plots=plots, columns_list=columns_list)
