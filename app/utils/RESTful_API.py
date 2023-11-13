import json,zlib

from app.utils.account.token import *
from app.utils.DataframeManager.load_df import generate_df_name,generate_cache_dash_name,load_current_df_memory,check_exists_df
from app.utils.graph_functions.generate_dasboard_graphics import generate_dashboard_graphics


def cache_dashboard(token):
    if confirm_token(token) == "cache_dashboard_admin":
        parquet_name = generate_df_name("run")
        cache_path = generate_cache_dash_name()
        
        if not check_exists_df(parquet_name):
            return "No data available"
        
        dataframe = load_current_df_memory()
        plots = generate_dashboard_graphics(dataframe)                        
            
        compressed_dashboard = zlib.compress(json.dumps(plots).encode('utf-8'),level=zlib.Z_BEST_COMPRESSION)
        with open(cache_path, "wb") as file:
            file.write(compressed_dashboard)

        return plots

    return "Authentication error"

def compute_dash_from_VIN(token,vin):
    if confirm_token(token) == "dash_from_vin_admin":
        parquet_name = generate_df_name("run")
        
        if not check_exists_df(parquet_name):
            return "No data available"
        ##### TO BE REPLACED WITH FUNCTION TO GENERATE FROM VIN ########    
        raw_dataframe = load_current_df_memory()        
        dataframe = raw_dataframe[raw_dataframe.index == vin]
        ################################################################
        plots = generate_dashboard_graphics(dataframe,vin)
                    
        return plots

    return "Authentication error"

