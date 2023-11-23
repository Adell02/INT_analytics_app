import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import statsmodels.api as sm
import os

from app.utils.graph_functions.functions import *

"""
Consumo vs temperatura.

La idea es conseguir generar un grafico significativo que relacione el consumo (medio seguramente) a traves del tiempo en funcion de la temperatura de la
batería, inversor, motor ...?

La idea es ir vehiculo por vehiculo y obtener los siguientes datos:
    1)  Consumo, definido como delta_SOC(%) / km. Para ello usaremos el campo SoC delta (%) en B1 y Total(km) en C2. Nos indican, respectivamente, qué SoC
        se ha consumido en el trayecto y cuantos km se ha recorrido.
    
    2)  Temperatura. No se puede estimar temperatura ambiente, por lo que recurriremos a realizar la comparativa según alguna de las siguientes temperaturas:
        del BMC (o de la batería), del inversor i/o del motor. Una idea es representar las tres tendencias juntas

    3)  Relacionarlas, una idea es mediante un scatter plot con lineas de tendencia, de esta manera se puede observar con más facilidad si hay alguna relación
        Sería interesante poder generar una función que te haga una recta de regresión pero que sea por tramos y no lineal, para ver si en algun rango de temp.
        el comportamiento es diferente al esperado.

    4) Una opción es incluír en el gráfico un vehiculo concreto para ver el comportamiento genérico vs el de un usuario en concreto
"""

INDEX = 'VIN'
KEY_COLUMNS = ['VIN','Id','Timestamp']
NUM_ROWS = 10000
DISTANCE_COLUMN = 'Total distance'
# TEMP_COLUMN = 'Motor min T (°C)'
TEMP_COLUMN = 'Avg temp'
# TEMP_COLUMN = 'Inv  min T (°C)'
# TEMP_COLUMN = 'Average V'
SOC_COLUMN = 'SoC delta'
TEXT_OFFSET = 500


def weigh(value,mean,std_dev):
    # Gives a weight to the value, following a mean and standard deviation passed
    # as parameters
    # 
    # INPUTS
    #   - value:    what value needs to be weighed
    #   - mean:     desired mean
    #   - std_dev:  desired standard deviation
    # OUTPUTS
    #   - Weighted value

    z_score = (value - mean) / std_dev
    weighted_val = 1 / (std_dev * np.sqrt(2 * np.pi)) * np.exp(-0.5 * z_score**2)
    return weighted_val


def get_consumption_vs_temp(df):
    # Generates a figure showing the relation of two variables: battery temperature and consumption
    # of motorcycle
    # 
    # INPUTS:
    #   - df: it must contain the necessary columns to generate the graphic
    # OUTPUTS:
    #   - -1 if df does not contain all necessary columns
    #   - figure to be plotted, it includes the Pearson correlation of both variables
    # 
    
    # 1. Check if dataframe contains all data necessary:
    #   - Total (km)
    #   - SoC delta (%)
    #   - Avg temp (ºC * 10)  --> average temperature of the BMS (then, battery temp)
    KEY_ELEMENTS = [DISTANCE_COLUMN,SOC_COLUMN,TEMP_COLUMN]
    check = 0
    for element in KEY_ELEMENTS:
        if element in df:
            check += 1
    if check != len(KEY_ELEMENTS):
        return -1

    # 2. Generate and compute the consume column. Since generate_df_from_elements assures that 
    # the dataframe is well ordered, we don't have to check the index
    CONSUMPTION_COLUMN = 'Consumption SoC(%)/km'
    df[CONSUMPTION_COLUMN] = df[SOC_COLUMN]/df[DISTANCE_COLUMN]

    # 3. We want to show only the 95% of points below that percentile
    column_filtered_above = df[CONSUMPTION_COLUMN].quantile(0.975)
    column_filtered_below = df[CONSUMPTION_COLUMN].quantile(0.025)

    # Modify the dataframe so the points that are going to be shown are those that are comprised
    # between the 2.5% and 97.5% of the samples.
    # Essentially, we're filetring a total of 5% of points that are furthest from the mean
    df_filtered = df[(df[CONSUMPTION_COLUMN] <= column_filtered_above) & (df[CONSUMPTION_COLUMN] >= column_filtered_below)]
    
    # 4. Get a scatter plot
    fig_filtered = generate_scatter_plot(df_filtered,TEMP_COLUMN,CONSUMPTION_COLUMN,'Consumption vs Temp Filtered',True)
    fig_filtered.update_layout(scene=dict(
        xaxis = dict(range=[min(df[TEMP_COLUMN]),max(df[TEMP_COLUMN])])
    ))
    # 5. Get the correlation between variables

    """
    Developer comment: From the emprical analysis it is known that there could be a linear relation between
    the motorcycle consumption and the battery temperature, to measure by how much these two variables are
    related we'll get the Pearson correlation of them
    """
    # Get correlation using filtered points
    correlation = df_filtered[CONSUMPTION_COLUMN].corr(df_filtered[TEMP_COLUMN])

    # 6. Display the correlation on the figures
    
    # Get the position of the top-right corner to display the text in that point
   
    x_position_filtered = min(df_filtered[TEMP_COLUMN])+TEXT_OFFSET
    y_position_filtered = max(df_filtered[CONSUMPTION_COLUMN])

    # Generate text to display the correlation and place it in the legend
    fig_text = f'r: {round(correlation*100,2)}%'
    fig_filtered.add_trace(go.Scatter(x=[x_position_filtered], y=[y_position_filtered], mode="text",name = fig_text ,showlegend=True))
    fig_filtered.update_traces(marker=dict(size=3))
    fig_filtered.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=0.99
))
    
    return fig_filtered

