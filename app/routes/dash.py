# dash.py
import os
from flask import Blueprint, render_template,url_for,request,session
import zlib
import requests,json

from app.config import Config
from app.routes.auth import login_required
from app.utils.graph_functions.generate_dashboard_graphics import generate_dashboard_graphics,build_html
from app.utils.account.token import generate_token
from app.utils.DataframeManager.load_df import generate_cache_dash_name,load_current_df_memory
from app.routes.RESTful_API import cache_dashboard,compute_dash_from_VIN


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
            
        if VIN_selected in available_vin:
            plots = compute_dash_from_VIN(Config.SERVER_TOKEN,VIN_selected)
            default_vin = VIN_selected
            html_string = build_html(Config.PATH_DASHBOARD_CONFIG,dataframe,plots,VIN_selected)

            return render_template('dashboard.html', html_string = html_string,plots=plots,available_vin=available_vin,default_vin=default_vin)  

    cached_path = generate_cache_dash_name()
    if os.path.isfile(cached_path):
        with open(cached_path, "rb") as file:
            cached = file.read()
        plots = json.loads(zlib.decompress(cached).decode('utf-8'))
    else:        
        plots = cache_dashboard(Config.SERVER_TOKEN)
    
    html_string = build_html(Config.PATH_DASHBOARD_CONFIG,dataframe,plots)

    return render_template('dashboard.html', html_string = html_string, plots=plots,available_vin=available_vin,default_vin=default_vin)
    
