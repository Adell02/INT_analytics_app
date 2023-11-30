
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
from app.database.seeder import fetch_ray_gps


def generate_cache_dash_name():
    current_month = datetime.now().month
    current_year = datetime.now().year

    name = Config.PATH_CACHE_DASHBOARD + "_" + str(current_month) + "_" + str(current_year) +".zlib"

    return name

def generate_cache_analytics_name():
    current_month = datetime.now().month
    current_year = datetime.now().year

    name = Config.PATH_CACHE_ANALYTICS + "_" + str(current_month) + "_" + str(current_year) +".zlib"

    return name

def generate_df_name(type:str) -> str:
    #current_month = datetime.now().month
    #current_year = datetime.now().year
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
        

def load_map_df(samples = None)->pd.DataFrame:
    name = Config.PATH_MAP_DATAFRAME

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
    
def process_coords_for_df(df_:pd.DataFrame) -> pd.DataFrame:
    df_gps = None
    if os.path.exists(Config.PATH_MAP_DATAFRAME):
        df_gps = pq.read_table(Config.PATH_MAP_DATAFRAME).to_pandas()
    

    batch_size = 1000
    for start_row in range(0, len(df_),batch_size):
        print(start_row)
        end_row = min(start_row+batch_size,len(df_))
        
        df = df_.iloc[start_row:end_row]

        is_row = False
        if type(df_gps) != type(None):
            if len(df_gps) > start_row:
                first_row = df.iloc[0]
                equivalent_gps_row = df_gps.iloc[start_row]
                is_row = (first_row.name == equivalent_gps_row.name) & (first_row['Timestamp CT']==equivalent_gps_row['Timestamp CT']) & (first_row['Id']==equivalent_gps_row['Id'])
            
        if is_row == False:
            def pass_parameters_fetch_ray_gps(row):
                return ",".join(fetch_ray_gps(row.name,row['Start'],row['End'],row['Id']))
            df['Coordinates'] = df.apply(pass_parameters_fetch_ray_gps,axis=1)
            table = pa.Table.from_pandas(df)
            if start_row == 0:
                pqwriter = pq.ParquetWriter(Config.PATH_MAP_DATAFRAME, table.schema)              
            pqwriter.write_table(table)        
    if pqwriter:
        pqwriter.close()
    
