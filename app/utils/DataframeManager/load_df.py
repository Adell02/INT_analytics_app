
import pandas as pd
import os 
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime

from app import Config
from app.utils.graph_functions.functions import *
from app.utils.graph_functions.generate_dasboard_graphics import *

def generate_cache_dash_name():
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year

    name = Config.PATH_CACHE + "_" + str(current_month) + "_" + str(current_year) +".zlib"

    return name

def generate_df_name(type:str) -> str:
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year

    name = Config.PATH_DATAFRAMES + type + "_" + str(current_month) + "_" + str(current_year) +".parquet"

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
    df = df_from_elements(origin_file,INDEX,None,KEY_COLS,LIST_COLUMNS)
    table = pa.Table.from_pandas(df)
    pq.write_table(table,parquet_file)


def load_current_df_memory(samples=None) -> pd.DataFrame:
    name = generate_df_name("run")

    # WHAT HAPPENS IF DOES NOT EXIST? 
    if not check_exists_df(name):
        test_generate_parquet_from_df("app\database\dfs\Ray 7.7_modificat.xlsx",name)
    if samples:
        pf = pq.ParquetFile(name)
        first_N_rows = next(pf.iter_batches(batch_size=samples))
        return pa.Table.from_batches([first_N_rows]).to_pandas()
    else:
        table = pq.read_table(name)
        return table.to_pandas()
        


    
