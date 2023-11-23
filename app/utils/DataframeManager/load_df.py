
import pandas as pd
import os 
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime

from app import Config
from app.utils.graph_functions.functions import *
from app.utils.graph_functions.generate_dashboard_graphics import *
from app.utils.DataframeManager.DataBase import df_from_scratch
from app.utils.DataframeManager.dataframe_treatment import df_filter_data
from app.utils.DataframeManager.dataframe_storage import df_append_data

def generate_cache_dash_name():
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year

    name = Config.PATH_CACHE_DASHBOARD + "_" + str(current_month) + "_" + str(current_year) +".zlib"

    return name

def generate_cache_analytics_name():
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year

    name = Config.PATH_CACHE_ANALYTICS + "_" + str(current_month) + "_" + str(current_year) +".zlib"

    return name

def generate_df_name(type:str) -> str:
    #current_month = datetime.datetime.now().month
    #current_year = datetime.datetime.now().year
    current_month = "07"
    current_year = "2023"
    name = Config.PATH_DATAFRAMES + str(current_year) + "_" + str(current_month) + "_" + type +".parquet"

    return name


def check_exists_df(name:str) -> int:   
    return os.path.isfile(name)
        
def test_generate_parquet_from_df(origin_file,parquet_file):
    LIST_COLUMNS = ['City (km)','Sport (km)','Flow (km)','Sail (km)','Regen (km)',
                    'City energy (Wh)','Sport energy (Wh)','Flow energy (Wh)','City regen (Wh)','Sport regen (Wh)',
                    'Total energy (Wh)','Total regen (Wh)',
                    'End odometer','Min cell V','Max cell V',
                    'Total (km)','Avg temp','SoC delta (%)',
                    'Motor min T (°C)','Motor max T (°C)',
                    'Inv  min T (°C)','Inv max T (°C)']
    
    INDEX = 'VIN'
    KEY_COLS = ['VIN','Id','Timestamp']

    
    # Generate a dataframe containing all columns listed before
    df = df_from_xlsx_elements(origin_file,INDEX,None,KEY_COLS,LIST_COLUMNS)
    table = pa.Table.from_pandas(df)
    pq.write_table(table,parquet_file)


def load_current_df_memory(samples=None) -> pd.DataFrame:
    name = generate_df_name("trip")

    # WHAT HAPPENS IF DOES NOT EXIST? 
    if not check_exists_df(name):
        #test_generate_parquet_from_df("app\database\dfs\Ray 7.7_modificat.xlsx",name)
        df_trip,df_charge = df_from_scratch()
        df_filter_data(df_trip,'trip',True)
        df_filter_data(df_charge,'charge',True)
        df_append_data(df_trip,'trip')
        df_append_data(df_charge,'charge')

    if samples:
        pf = pq.ParquetFile(name)
        first_N_rows = next(pf.iter_batches(batch_size=samples))
        return pa.Table.from_batches([first_N_rows]).to_pandas()
    else:
        table = pq.read_table(name)
        return table.to_pandas()
        


    
