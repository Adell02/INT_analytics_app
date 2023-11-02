from flask import Blueprint
import json
import zlib

from app.utils.account.token import *
from app.utils.DataframeManager.load_df import generate_df_name,generate_cache_dash_name,load_current_df_memory,check_exists_df
from app.utils.graph_functions.generate_dasboard_graphics import generate_dashboard_graphics


rest_api_bp = Blueprint('rest_api', __name__)

@rest_api_bp.route('/<token>/cache_dashboard',methods=['POST','GET'])
def cache_dashboard(token):
    if confirm_token(token) == "cache_dashboard_admin":
        parquet_name = generate_df_name("run")
        cache_path = generate_cache_dash_name()
        
        if not check_exists_df(parquet_name):
            return "No data available"
        
        dataframe = load_current_df_memory()
        plots = generate_dashboard_graphics(dataframe)
        
        str_plots = json.dumps(plots).encode("utf-8")
        compressed_dashboard = zlib.compress(str_plots,level=zlib.Z_BEST_COMPRESSION)
        with open(cache_path, "wb") as file:
            file.write(compressed_dashboard)

        return plots.to_json()

    return "Authentication error"