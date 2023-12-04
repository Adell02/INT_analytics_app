import json,zlib,requests
from datetime import datetime,timedelta, timezone
from flask import Blueprint,request,url_for
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from app import socketio
from app.utils.account.token import *
from app.database.seeder import edit_data,fetch_data_params, fetch_ray_trip, fetch_ray_charge
from app.utils.DataframeManager.load_df import *
from app.utils.graph_functions.generate_dashboard_graphics import generate_dashboard_graphics
from app.utils.graph_functions.generate_analytics_graphics import generate_analytics_graphics

from app.utils.DataframeManager.from_server_to_df import from_server_to_parquet

api_bp = Blueprint("api",__name__)

# This API serves the server or any other service to fetch new data from an external DDBB 
# and compute the necessary resources to accelerate user loading process

def write_log(note:str):
    with open("log_server.txt","a") as file:
        file.write(str(datetime.now())+" - "+ note+"\n")
    return 

@api_bp.route("/<token>/server_process", methods=['GET'],defaults={'timestamp_i':'','timestamp_f':''}) 
@api_bp.route("/<token>/server_process/<timestamp_i>", methods=['GET'],defaults={'timestamp_f':''})
@api_bp.route("/<token>/server_process/<timestamp_i>/<timestamp_f>", methods=['GET'])
def server_process(token,timestamp_i,timestamp_f):
    """
    This function will fetch data from Ray's database, build the corresponding dataframes and treat its values
    to be appended to the current data storage.

    INPUTS:
        - token
        - timestamp_i, timestamp_f:     These two timestamps mark the begining and end of the data to be stored. If both
                                        are None, that means the function has been executed automatically and only last
                                        day's data is needed.
    """
    if token == Config.SERVER_TOKEN:
        
        # If timestamps are None, get all data since the day before @ 00:00:00 UTC until today @ 00:00:00 UTC
        # For debugging purposes, this operation is done for two months before, since there's no data for "today".
        if timestamp_i == '' and timestamp_f == '':
            # timestamp_i = int((datetime.now(timezone.utc) - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
            # timestamp_f = int(datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
            timestamp_i = int((datetime.now(timezone.utc) - timedelta(days=1,weeks=8)).replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
            timestamp_f = int((datetime.now(timezone.utc)-timedelta(weeks=8)).replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
            df_trip = fetch_ray_trip(timestamp_i,timestamp_f)
            df_charge = fetch_ray_charge(timestamp_i,timestamp_f)
        
        # If the first timestamp is not None, that means we want to fetch all data since timestamp_i and until now (if timestamp_f)
        # is None, or until the specified timestamp_f 

        # If a specific timestamp_i, two situations are possible:
        # 1) No timestamp_f is specified --> In this case, get the current timestamp and set it as timestamp_f
        # 2) timestamp_f has been specified as well --> Fetch with timestamp_i and timestamp_f with theur respective values.

        elif(timestamp_i != ''):
            if timestamp_f == '':
                timestamp_f = int(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp())

            df_trip = fetch_ray_trip(timestamp_i,timestamp_f)
            df_charge = fetch_ray_charge(timestamp_i,timestamp_f)


        # Under no circumstances timestamp_f != None while timestamp_i == None, so that call will be discarted
        else:
            return

        write_log("OK Data Fetch")
       
        # With df_trip and df_charge, convert them into "depurated" dataframes.
        df_trip_appended = from_server_to_parquet(df_trip)
        from_server_to_parquet(df_charge)

        write_log("OK Parquet Generation")

        # Pass to Miquel's function -> generate df
        # Pass to df_append -> generate .parquet for months and filter
        # update Timestamp, VINs and Columns : Mysql params = org_token,last_timestamp,columnes,VINs
        # df_ = load_current_df_memory()
        # df = process_coords_for_df(df_trip_appended)        
        
        last_timestamp = fetch_data_params("last_timestamp")
        if last_timestamp is None:
            # the parameter should be timestamp, instead we are loading the first day september 
            last_timestamp = 1693526400
        
        df = load_current_df_memory()

        if not process_coords_for_df(df):
            write_log("NAK Coords Error")
            return "GPS Coords Fetch Error"
        write_log("OK Coords Fetch")


        last_timestamp = df['Timestamp CT'].max()
        columns = list(pd.read_json(Config.PATH_BATTERY_PARAMS).columns)
        vins = list(df['Id'].keys().unique())
        
        edit_data("last_timestamp",last_timestamp)
        edit_data("columnes",columns)
        edit_data("VINs",",".join(vins))
        
        
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
        
        if not os.path.exists(Config.PATH_CACHE):
            os.makedirs(Config.PATH_CACHE)

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


@api_bp.route("/<token>/production_api", methods=['GET','POST'])
def production_api_call(token):
    if token == Config.SERVER_TOKEN:
        content = request.get_json(silent=True)
        df_received = pd.DataFrame(content)
        if os.path.isfile(Config.PATH_PRODUCTION_DATA):
            df_received = pd.concat([df_received,pd.read_parquet(Config.PATH_PRODUCTION_DATA)])        
        table = pa.Table.from_pandas(df_received)
        pq.write_table(table,Config.PATH_PRODUCTION_DATA)

        html_table = df_received.to_html(classes="table_class",header=True)    
        socketio.emit("html_table",html_table)
        return "API - Data received correctly."
    return "API - Authentication Error"


@api_bp.route("/production_api_test", methods=['GET','POST'])
def production_api_call_test():
    url = "http://13.48.135.195/"+Config.SERVER_TOKEN+"/production_api"
    response = requests.post(url,json=[{"Data1":1,"Data2":1},{"Data1":2,"Data2":2}])    
    return response.text