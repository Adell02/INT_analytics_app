from flask import Blueprint, render_template, request
import pandas as pd
import numpy as np

from app.routes.auth import login_required
from app.utils.DataframeManager.load_df import load_map_df
from app.utils.graph_functions.functions import df_get_columns_tag
from app.utils.graph_functions.generate_map import generate_map,generate_void_map

mapview_bp = Blueprint("mapview",__name__)

@mapview_bp.route('/mapview', methods=["POST","GET"])
@login_required
def mapview():
    df = load_map_df()
    available_vin = list(df['Id'].keys().unique())  
    columns_list=df_get_columns_tag(df)
    columns_list.pop(-1)
    vin_selected =""
    column_selected =""
    
    if request.method == 'POST':
        vin_selected = request.form['VIN_selector']
        column_selected = request.form['map_data']

        if column_selected not in columns_list:
            column_selected=""

        if vin_selected in available_vin:
            df = df[df.index == vin_selected]
        else:
            vin_selected=""

    if column_selected =="":
        new_df = pd.DataFrame()
        new_df['lat']=[]
        new_df['lon']=[]
        new_df[""]=[]
        new_df['VIN'] = []
        new_df['ID'] = []
        fig = generate_void_map(new_df)

    else:
        values = df[df["Coordinates"] != ","][column_selected]
        latitude = get_latitude(df)
        longitude = get_longitude(df)
        new_df = pd.DataFrame()
        new_df['lat']=latitude
        new_df['lon']=longitude
        new_df[column_selected]=values   
        new_df['VIN'] = values.index
        new_df['ID'] = df[df["Coordinates"] != ","]['Id']
        fig = generate_map(new_df,column_selected)    

    return render_template('mapview.html',available_vin=available_vin,columns_list=columns_list,fig=fig,column_selected=column_selected,vin_selected=vin_selected)


def get_latitude(df:pd.DataFrame):
    # Extract degrees and minutes from the string, considering the negative sign
    degrees_str = df[df["Coordinates"] != ","]["Coordinates"].str.extract(r'(-?\d{2})\d{2}\.\d+')[0]
    minutes_str = df[df["Coordinates"] != ","]["Coordinates"].str.extract(r'-?\d{2}(\d{2}\.\d+)')[0]
    minutes_str = np.where(degrees_str.str.startswith('-'), '-' + minutes_str, minutes_str)


    # Convert to numeric and calculate latitude
    degrees = pd.to_numeric(degrees_str)
    minutes = pd.to_numeric(minutes_str) / 60.0
    
    latitude = degrees + minutes
    return latitude 

def get_longitude(df:pd.DataFrame):
    # Extract degrees and minutes from the string, considering the negative sign
    degrees_str = df[df["Coordinates"] != ","]["Coordinates"].str.extract(r'(-?\d{3})\d{2}\.\d+')[0]
    minutes_str = df[df["Coordinates"] != ","]["Coordinates"].str.extract(r'-?\d{3}(\d{2}\.\d+)')[0]
    minutes_str = np.where(degrees_str.str.startswith('-'), '-' + minutes_str, minutes_str)


    # Convert to numeric and calculate latitude
    degrees = pd.to_numeric(degrees_str)
    minutes = pd.to_numeric(minutes_str) / 60.0
    longitude = degrees + minutes
    return longitude