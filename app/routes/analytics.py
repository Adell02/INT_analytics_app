import os
import json
import zlib
from flask import Blueprint, render_template, request

from app import Config
from app.routes.auth import login_required
from app.utils.DataframeManager.load_df import load_current_df_memory,generate_cache_analytics_name
from app.routes.RESTful_API import cache_analytics,compute_analytics_from_VIN
            



analytics_bp = Blueprint("analytics",__name__)

@analytics_bp.route('/analytics', methods=["GET","POST"])
@login_required
def analytics():
    
    dataframe = load_current_df_memory()
    columns_list = list(dataframe.columns)
    available_vin = list(dataframe['Id'].keys().unique()) 
    default_vin = '' 

    if request.method == 'POST':
        req = json.loads(request.data)
        if "vin" in req.keys():
            VIN_selected = req["vin"]
        
            if VIN_selected in available_vin:
                default_vin = VIN_selected
                plots = compute_analytics_from_VIN(Config.SERVER_TOKEN,VIN_selected)
                return plots



    cached_path = generate_cache_analytics_name()
    if os.path.isfile(cached_path):
        with open(cached_path, "rb") as file:
            cached = file.read()
        plots = json.loads(zlib.decompress(cached).decode('utf-8'))
    else:        
        plots = cache_analytics(Config.SERVER_TOKEN)    

    return render_template('analytics.html',plots=plots, columns_list=columns_list,default_vin=default_vin,available_vin=available_vin)
