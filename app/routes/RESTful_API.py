import json,zlib
from datetime import datetime
from flask import Blueprint
import pandas as pd

from app.utils.account.token import *
from app.database.seeder import edit_data,fetch_data_params
from app.utils.DataframeManager.load_df import *
from app.utils.graph_functions.generate_dashboard_graphics import generate_dashboard_graphics
from app.utils.graph_functions.generate_analytics_graphics import generate_analytics_graphics

api_bp = Blueprint("api",__name__)

# This API serves the server or any other service to fetch new data from an external DDBB 
# and compute the necessary resources to accelerate user loading process

def write_log(note:str):
    with open("log_server.txt","a") as file:
        file.write(str(datetime.now())+" - "+ note+"\n")
    return 

@api_bp.route("/<token>/server_process", methods=['GET'],defaults={'timestamp':''}) 
@api_bp.route("/<token>/server_process/<timestamp>", methods=['GET'])
def server_process(token,timestamp):
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
        write_log("OK Updated Database")
        return "Server Fetch OK"

    write_log("KO Updated Database (Token Confirmation)")
    return "Server KO"

@api_bp.route("/<token>/cache_dashboard", methods=['GET'])
def cache_dashboard(token):
    if token == Config.SERVER_TOKEN:
        parquet_name = generate_df_name("trip")
        cache_path = generate_cache_dash_name()
        
        if not check_exists_df(parquet_name):
            write_log("KO Cache Dashboard (No data available)")
            return "No data available"
        
        dataframe = load_current_df_memory()
        plots = generate_dashboard_graphics(Config.PATH_DASHBOARD_CONFIG,dataframe)                        
            
        compressed_dashboard = zlib.compress(json.dumps(plots).encode('utf-8'),level=zlib.Z_BEST_COMPRESSION)
        with open(cache_path, "wb") as file:
            file.write(compressed_dashboard)
        write_log("OK Cache Database")
        return plots
    write_log("KO Cache Database (Token Confirmation)")
    return "Authentication error"

def compute_dash_from_VIN(token,vin):
    if token == Config.SERVER_TOKEN:
        parquet_name = generate_df_name("trip")
        
        if not check_exists_df(parquet_name):
            return "No data available"
        
        ##### TO BE REPLACED WITH FUNCTION TO GENERATE FROM VIN ########    
        raw_dataframe = load_current_df_memory()        
        dataframe = raw_dataframe[raw_dataframe.index == vin]
        ################################################################
        plots = generate_dashboard_graphics(Config.PATH_DASHBOARD_CONFIG,dataframe,vin)
                    
        return plots

    return "Authentication error"


@api_bp.route("/<token>/cache_analytics", methods=['GET'])
def cache_analytics(token):
    if token == Config.SERVER_TOKEN:
        parquet_name = generate_df_name("trip")
        cache_path = generate_cache_analytics_name()
        
        if not check_exists_df(parquet_name):
            write_log("KO Cache Analytics (No data available)")
            return "No data available"
        
        dataframe = load_current_df_memory()
        plots = generate_analytics_graphics(Config.PATH_ANALYTICS_CONFIG,dataframe)                        
            
        compressed_dashboard = zlib.compress(json.dumps(plots).encode('utf-8'),level=zlib.Z_BEST_COMPRESSION)
        with open(cache_path, "wb") as file:
            file.write(compressed_dashboard)
        write_log("OK Cache Analytics")
        return plots
    write_log("KO Cache Analytics (Token Confirmation)")
    return "Authentication error"
