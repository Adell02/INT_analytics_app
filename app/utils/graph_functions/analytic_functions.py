
from app.utils.graph_functions.plots_generation import*
def delta_SoC_vs_Total_Energy(df_trip):
    '''
    This function takes a DataFrame df_trip as input. It calculates the change in State of Charge (SoC) and the total energy consumption from the DataFrame. It then generates a scatter plot using the generate_scatter_plot function, with the total energy on the x-axis and the change in SoC on the y-axis. The function returns the generated scatter plot.
        Input: df_trip (DataFrame)
        Output: fig (plotly.graph_objects.Figure)
    '''
    DIF_SOC = '∂SoC'
    TOTAL_ENERGY = 'Total energy'
    DELTA_SOC = 'SoC delta'
    fig = generate_scatter_plot(df_trip,TOTAL_ENERGY,DELTA_SOC,title= DIF_SOC, reg_line=True)
    return fig


def mode_energy_vs_kilometers(df_trip):
    '''
    This function takes a DataFrame df_trip as input. It calculates the differential energy consumption per kilometer for different driving modes (Sport, City, and Flow) based on the energy consumed and the distance traveled in each mode. It creates a new DataFrame df_final with the calculated differential energy values. It then generates a box plot using the generate_box_plot function, with the differential energy values on the y-axis and the driving modes on the x-axis. The function returns the generated box plot.
        Input: df_trip (DataFrame)
        Output: fig (plotly.graph_objects.Figure)
    '''
    SPORT_MODE = 'Sport energy' 
    CITY_MODE = 'City energy'
    FLOW_MODE = 'Flow energy'
    DISTANCE = 'End odometer'
    DISTANCE_CITY = 'City distance'
    DISTANCE_SPORT = 'Sport distance' 
    DISTANCE_FLOW = 'Flow distance'
    DIF_SPORT_MODE = 'Differential Sport energy (Wh/km)'
    DIF_CITY_MODE = 'Differential city energy (Wh/km)'
    DIF_FLOW_MODE = 'Differential flow energy (Wh/km)'
    TITLE = 'Mode_energy_vs_kilometers (Wh/km)'
    ELEMENTS_Y = [DIF_CITY_MODE,DIF_SPORT_MODE,DIF_FLOW_MODE]

    df_final = pd.DataFrame()
    df_final[DIF_SPORT_MODE]= df_trip[SPORT_MODE]/df_trip[DISTANCE_SPORT]
    df_final[DIF_CITY_MODE]= df_trip[CITY_MODE]/df_trip[DISTANCE_CITY]
    df_final[DIF_FLOW_MODE]= df_trip[FLOW_MODE]/df_trip[DISTANCE_FLOW]
    fig = generate_box_plot(df_final,ELEMENTS_Y,title = TITLE)
    return fig


def delta_soc_vs_inv_min_temp(df_trip):
    """
    Calculate the change in State of Charge (SoC) per unit temperature for a given trip dataset.

    Input:
        df_trip (DataFrame): The input trip dataset containing the following columns:
            - 'Inv min T (°C)': The minimum temperature recorded during the trip for the inverter.
            - 'SoC delta (%)': The change in State of Charge (SoC) during the trip.
            - 'Consumption SoC(%)/km': The SoC consumption per kilometer.
            - 'Total (km)': The total distance traveled during the trip.

    Output:
        fig (Figure): The scatter plot figure showing the relationship between the change in SoC per unit temperature and the inverter minimum temperature. The figure includes a regression line.

    Raises:
        Exception: If an error occurs while generating the scatter plot.

    Notes:
        - The function filters out outliers by considering only the 95% of points within the specified percentiles.
        - The function calculates the average change in SoC per unit temperature for each inverter minimum temperature.

    """
    INV_MIN_T = 'Inv min T'
    DELTA_SOC = 'SoC delta'
    TITLE = '∂SoC'
    SOC_VS_TEMP = 'Soc Delta vs Inv min T(%/°C)'
    CONSUMPTION_COLUMN = 'Consumption SoC(%)/km'
    DISTANCE_COLUMN = 'Total distance'
    df_final = pd.DataFrame()
    df_final[CONSUMPTION_COLUMN] = df_trip[DELTA_SOC] / df_trip[DISTANCE_COLUMN]
    df_final[INV_MIN_T] = df_trip[INV_MIN_T]

    # Check for missing data
    if df_trip[[INV_MIN_T, DELTA_SOC]].isnull().values.any():
        print("Warning! There is missing data in the relevant columns.")

    # Filter out outliers
    column_filtered_above = df_final[CONSUMPTION_COLUMN].quantile(0.975)
    column_filtered_below = df_final[CONSUMPTION_COLUMN].quantile(0.025)
    df_filtered = df_final[(df_final[CONSUMPTION_COLUMN] <= column_filtered_above) & (df_final[CONSUMPTION_COLUMN] >= column_filtered_below)]

    # Calculate the average of the DELTA_SOC values for each INV_MIN_T
    media_por_rango = df_filtered.groupby(INV_MIN_T)[CONSUMPTION_COLUMN].mean().reset_index()

    try:
        fig = generate_scatter_plot(media_por_rango, INV_MIN_T, CONSUMPTION_COLUMN, title=TITLE, reg_line=True)
        return fig
    except Exception as e:
        print(f"Error generating graph! Mistake: {e}")
        return None

#Para entregar
def inv_min_t_vs_cell_min_t_vs_total_energy(df_trip):
    """
    Calculate the response surface for the relationship between the inverse of the minimum temperature,
    the minimum cell temperature, and the total energy.
        Input: df_trip (DataFrame): The input DataFrame containing the trip data.
        Output: DataFrame: The response surface DataFrame.

    """
    INV_MIN_T = 'Inv min T'
    TOTAL_ENERGY = 'Total energy'
    CELL_MIN_T = 'Min temp CT'
    return generate_response_surface(df_trip, INV_MIN_T, CELL_MIN_T, TOTAL_ENERGY, title='Temperature Response Surface')
#Para entregar
def correlation(df, columns):
    """
    Calculate the correlation matrix for the selected columns in a DataFrame.

    Inputs:
        df (pandas.DataFrame): The input DataFrame.
        columns (list): A list of column names to include in the correlation calculation.

    Outputs:
        correlation_matrix (pandas.DataFrame): The correlation matrix of the selected columns.
    """
    #selected_df = df[columns]
    #correlation_matrix = selected_df.corr()
    #return px.imshow(correlation_matrix, labels=dict(x="Columnas", y="Columnas", color="Correlación"))
    pass


def batery_temp_vs_distance(df):
    """
    Batery temperature average vs distance
    Inputs:
        df (pandas.DataFrame): The input DataFrame.
        columns (list): A list of column names to include in the correlation calculation.

    Outputs:
        generate_bar_chart()
    """  
    AVERAGE_TEMP = 'Avg temp'
    DISTANCE_COLUMN = 'Total distance'
    
    # Divide todos los valores de la columna "average temp" por 100 para convertirlos a grados Celsius
    df[AVERAGE_TEMP] = df[AVERAGE_TEMP] / 100

    # Create a new column representing 10 km intervals
    df['Intervalo_10'] = (df[DISTANCE_COLUMN] // 10) * 10

    # Group the data by the new column and calculate the average temperature
    temperatura_media_por_intervalo = df.groupby('Intervalo_10')[AVERAGE_TEMP].mean().reset_index()

    # The .mean() method calculates the mean temperature for each distance interval group
     # .reset_index() resets the index of the DataFrame

    fig = generate_bar_chart(temperatura_media_por_intervalo, element_x='Intervalo_10', elements_y=AVERAGE_TEMP, title='Temperatura Media de la Batería por Intervalo de Distancia')

    fig.update_layout(
        xaxis_title='Trayectos agrupados por intervalos de 10 km',
        yaxis_title='Temperatura (°C)'
    )

    return fig

def regen_vs_temp(df):
    """
    Regen (%) vs average temperature
    Inputs:
        df (pandas.DataFrame): The input DataFrame.
        columns (list): A list of column names to include in the correlation calculation.

    Outputs:
        generate_scatter_plot()
    """ 
    AVERAGE_TEMP = 'Avg temp'
    CITY = 'City energy'
    SPORT = 'Sport energy'
    FLOW = 'Flow energy'
    CITY_REG = 'City regen'
    SPORT_REG = 'Sport regen'

    df[AVERAGE_TEMP] = df[AVERAGE_TEMP] / 100

    df['Total energy'] = df[SPORT] + df[FLOW] + df[CITY]
    df['Total regen'] =  df[SPORT_REG] + df[CITY_REG] 
    df['Regen en (%)'] = (df['Total regen'] / df['Total energy']) * 100
    
    # 3. We want to show only the 95% of points below that percentile
    column_filtered_above = df['Regen en (%)'].quantile(0.975)
    column_filtered_below = df['Regen en (%)'].quantile(0.025)

    # Modify the dataframe so the points that are going to be shown are those that are comprised
    # between the 2.5% and 97.5% of the samples.
    # Essentially, we're filetring a total of 5% of points that are furthest from the mean
    df_filtered = df[(df['Regen en (%)'] <= column_filtered_above) & (df['Regen en (%)'] >= column_filtered_below)]
    
    df_filtered = df_filtered.copy()
    df_filtered.loc[:, 'Interval'] = (df_filtered[AVERAGE_TEMP] // 0.01) * 0.01

    df_regen = df_filtered.groupby('Interval')['Regen en (%)'].mean().reset_index()
    # The .mean() method calculates the mean temperature for each distance interval group
    # .reset_index() resets the index of the DataFrame

    fig = generate_scatter_plot(df_regen,element_x='Interval' ,elements_y='Regen en (%)',title='Regeneracion de la bateria vs Temperatura',reg_line=True)

    fig.update_layout(
        xaxis_title='Temperatura (°C)',
        yaxis_title='Regen (%)'
    )

    return fig