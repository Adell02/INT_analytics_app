
import pandas as pd
import os 
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime, timedelta, timezone

from app import Config
from app.utils.DataframeManager.dataframe_storage import df_append_data
from app.utils.graph_functions.generate_dashboard_graphics import *
from app.utils.DataframeManager.DataBase import df_from_scratch
from app.utils.DataframeManager.dataframe_treatment import df_filter_data
from app.database.seeder import fetch_ray_gps


def generate_cache_dash_name():
    current_date = datetime.now(timezone.utc) - timedelta(weeks=8)
    current_month = current_date.month
    current_year = current_date.year

    current_month = "10"
    current_year = "2023"

    name = Config.PATH_CACHE_DASHBOARD + "_" + str(current_month) + "_" + str(current_year) +".zlib"

    return name

def generate_cache_analytics_name():
    current_date = datetime.now(timezone.utc) - timedelta(weeks=8)
    current_month = current_date.month
    current_year = current_date.year

    current_month = "10"
    current_year = "2023"

    name = Config.PATH_CACHE_ANALYTICS + "_" + str(current_month) + "_" + str(current_year) +".zlib"

    return name

def generate_df_name(type:str) -> str:
    current_date = datetime.now(timezone.utc) - timedelta(weeks=8)
    current_month = current_date.month
    current_year = current_date.year

    current_month = "10"
    current_year = "2023"
    
    name = Config.PATH_DATAFRAMES + str(current_year) + "_" + str(current_month) + "_" + type +".parquet"

    return name

def generate_map_df_name() -> str:
    current_date = datetime.now(timezone.utc) - timedelta(weeks=8)
    current_month = current_date.month
    current_year = current_date.year

    current_month = "10"
    current_year = "2023"
    name = Config.PATH_DATAFRAMES + str(current_year) + "_" + str(current_month) + "_" +"map.parquet"

    return name



def check_exists_df(name:str) -> int:   
    return os.path.isfile(name)
        


def load_current_df_memory(samples=None) -> pd.DataFrame:
    name = generate_df_name("trip")

    # WHAT HAPPENS IF DOES NOT EXIST? 
    if not check_exists_df(name):
        df_trip,df_charge = df_from_scratch()
        df_trip = df_filter_data(df_trip,'trip',True)
        df_charge = df_filter_data(df_charge,'charge',True)
        df_append_data(df_trip,'trip')
        df_append_data(df_charge,'charge')

    if samples:
        pf = pq.ParquetFile(name)
        first_N_rows = next(pf.iter_batches(batch_size=samples))
        return pa.Table.from_batches([first_N_rows]).to_pandas()
    else:
        table = pq.read_table(name)
        return table.to_pandas()
        

def load_map_df(samples = None)->pd.DataFrame:
    name = generate_map_df_name()

    # WHAT HAPPENS IF DOES NOT EXIST? 
    if not check_exists_df(name):
        return pd.DataFrame()

    if samples:
        pf = pq.ParquetFile(name)
        first_N_rows = next(pf.iter_batches(batch_size=samples))
        return pa.Table.from_batches([first_N_rows]).to_pandas()
    else:
        table = pq.read_table(name)
        return table.to_pandas()
    
def process_coords_for_df(df:pd.DataFrame) -> pd.DataFrame:
    df_gps = None
    ret = True
    map_df_path = generate_map_df_name()
    if os.path.exists(map_df_path):
        df_gps = pq.read_table(map_df_path).to_pandas()        
        start_row = len(df_gps)    
    else:
        start_row = 0
    
    for idx_row in range(start_row,len(df)):
        print(idx_row)
        row = df.iloc[[idx_row]] 
        try:
            coords = ",".join(fetch_ray_gps(row.index[0],row['Start'],row['End'],row['Id']))
            row['Coordinates'] = coords
            if df_gps is not None:
                df_gps = pd.concat([df_gps,row])
            else:
                df_gps = row                          
        except:
            ret = False
            break
    if df_gps is not None:
        table = pa.Table.from_pandas(df_gps)
        pqwriter = pq.ParquetWriter(map_df_path, table.schema)              
        pqwriter.write_table(table)
        pqwriter.close()
    return ret

    
