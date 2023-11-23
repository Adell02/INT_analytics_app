import json,zlib
from datetime import datetime
from flask import Blueprint
import pandas as pd

from app.utils.account.token import *
from app.database.seeder import edit_data,fetch_data_params
from app.utils.DataframeManager.load_df import generate_df_name,generate_cache_dash_name,load_current_df_memory,check_exists_df
from app.utils.graph_functions.generate_dasboard_graphics import generate_dashboard_graphics

api_bp = Blueprint("api",__name__)

# This API serves the server or any other service to fetch new data from an external DDBB 
# and compute the necessary resources to accelerate user loading process

@api_bp.route("/<token>/server_process", methods=['GET'],defaults={'timestamp':''}) 
@api_bp.route("/<token>/server_process/<timestamp>", methods=['GET'])
def test_api(token,timestamp):
    if token == Config.SERVER_TOKEN:
        # TIMESTAMP IS NONE -> TODAY
        # IF TIMESTAMP -> read until then
        # Pass to Miquel's function -> generate df
        # Pass to df_append -> generate .parquet for months and filter
        # update Timestamp, VINs and Columns : Mysql params = org_token,last_timestamp,columnes,VINs
        if True or fetch_data_params("last_timestamp") == None or timestamp:
            # the parameter should be timestamp, instead we are loading the first day september 
            edit_data("last_timestamp",1693526400)  # First day september
        if True or fetch_data_params("columnes") == None:
            columns = list(pd.read_json(Config.PATH_BATTERY_PARAMS).columns)
            edit_data("columnes",columns)
        if True or fetch_data_params("VINs") == None:
            #VINs = get it from the loaded DF
            pass
        with open("log_server.txt","a") as file:
            file.write(str(datetime.now())+" - OK Updated Database \n")
        return "Server Fetch OK"

    with open("log_server.txt","a") as file:
        file.write(str(datetime.now())+" - KO Confirm Token \n")
    return "Server KO"

@api_bp.route("/<token>/cache_dashboard", methods=['GET'])
def cache_dashboard(token):
    if token == Config.SERVER_TOKEN:
        parquet_name = generate_df_name("run")
        cache_path = generate_cache_dash_name()
        
        if not check_exists_df(parquet_name):
            return "No data available"
        
        dataframe = load_current_df_memory()
        plots = generate_dashboard_graphics(Config.PATH_DASHBOARD_CONFIG,dataframe)                        
            
        compressed_dashboard = zlib.compress(json.dumps(plots).encode('utf-8'),level=zlib.Z_BEST_COMPRESSION)
        with open(cache_path, "wb") as file:
            file.write(compressed_dashboard)

        return plots

    return "Authentication error"

def compute_dash_from_VIN(token,vin):
    if token == Config.SERVER_TOKEN:
        parquet_name = generate_df_name("run")
        
        if not check_exists_df(parquet_name):
            return "No data available"
        
        ##### TO BE REPLACED WITH FUNCTION TO GENERATE FROM VIN ########    
        raw_dataframe = load_current_df_memory()        
        dataframe = raw_dataframe[raw_dataframe.index == vin]
        ################################################################
        plots = generate_dashboard_graphics(Config.PATH_DASHBOARD_CONFIG,dataframe,vin)
                    
        return plots

    return "Authentication error"

