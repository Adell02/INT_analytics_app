import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import statsmodels.api as sm
import os
import json
from scipy import interpolate
import pyarrow as pa
import pyarrow.parquet as pq
import datetime



"""********************     Trace generation    ********************"""

def trace_pie(dataframe,elements,title='Unnamed pie chart'):
    # Pie chart figure generator given a dataframe, which contains all the necessary data,
    # elements to display and the title of the pie chart

    # This is an auxiliary function, it doesn't generate a Figure capable of being plotted
    # instead, this function helps 'pie_chart' to generate a subplot in case the user wants
    # to plot more than one pie_chart at a time
    # 
    # INPUTS:
    #   - dataframe
    #   - elements
    #   -title
    # 
    # OUTPUTS
    #   - go.Pie trace 
    
    # For each element (column), add all its values and save it into a data vector
    total_value=[]

    for element in elements:
        aux_value = 0
        for value in dataframe[element]:
            aux_value += value
        total_value.append(aux_value)
    
    # Generate pie chart
    trace = go.Pie(
        labels=elements,
        values=total_value,
        name=title
    )

    return trace

def trace_trendline(dataframe,element_x,elements_y,title='Trendline'):

    # This function generates a trendline (performing OLS) given a element to display on the
    # x_axis and allows multiple elements for the y_axis (thus, multiple trendlines)
    # 
    # INPUT:
    #   - dataframe: containing all data
    #   - element_x: which element will be display on the x_axis
    #   - elements_y: elements, trendline of which, will be displayed on the y_axis
    # OUTPUT:
    #   - trandline_vector: contains all traces to be added in a figure


    trendline_vector=[]
    
    if isinstance(elements_y,str):
        elements_X_aux = sm.add_constant(dataframe[element_x])      # elements_x but adding a '1' column for the reg line
        model = sm.OLS(dataframe[elements_y],elements_X_aux).fit()       # generate model 
        trendline = model.predict(elements_X_aux)                   # generate trendline   

        # Now generate the trace for the trendline and add it at the data_vector
        trendline_trace = go.Scatter(
            x=dataframe[element_x],
            y=trendline,
            mode='lines',
            name=f'{title}: {elements_y}'
        )
        trendline_trace.line.dash = 'longdashdot'  #['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']

        trendline_vector.append(trendline_trace)
    
    else:
        for element in elements_y:

            elements_X_aux = sm.add_constant(dataframe[element_x])      # elements_x but adding a '1' column for the reg line
            model = sm.OLS(dataframe[element],elements_X_aux).fit()       # generate model 
            trendline = model.predict(elements_X_aux)                   # generate trendline   

            # Now generate the trace for the trendline and add it at the data_vector
            trendline_trace = go.Scatter(
                x=dataframe[element_x],
                y=trendline,
                mode='lines',
                name=f'{title}: {element}'
            )
            trendline_trace.line.dash = 'longdashdot'  #['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']

            trendline_vector.append(trendline_trace)
    
    return trendline_vector

def trace_scatter_plot(dataframe,element_x,elements_y,reg_line=False):
    # Returns a scatter plot trace vector, given a dataframe, and elements to plot, can integrate a regression
    # line if specified
    # 
    # INPUTS:
    #   - dataframe: containing all data
    #   - element_x: x axis data
    #   - elements_y: vector that contains all the different data to be plotted
    #   - title: title of the graph
    #   - reg_line: boolean to indicate if a reg_line is wanted. Default value is False
    # OUTPUTS:
    #   - plotly trace if OK
    #   - None if error occured
    
    # Plot generation for each data source passed as parameter elements_y
        
    trace_vector=[]          # This vector will contain all traces, one for each element_y
    
    # We have to differentiate if elements_y is a vector or a string, because the for loop won't
    # act as intended if elements_y contains one single string
    if isinstance(elements_y,str):
        trace = go.Scatter(
            x=dataframe[element_x],
            y=dataframe[elements_y],
            mode='markers',
            name=elements_y
        )
        trace_vector.append(trace)

    else:
        for element in elements_y:
            trace = go.Scatter(
                x=dataframe[element_x],
                y=dataframe[element],
                mode='markers',
                name=element
            )
            trace_vector.append(trace)
        
    # A trendline is needed if reg_line is True
    if reg_line:
        trace_trend = trace_trendline(dataframe,element_x,elements_y)
        for trace in trace_trend:
            trace_vector.append(trace)

    return trace_vector

def trace_bar_chart(dataframe,element_x,elements_y):
    
    # Generate a trace_vector to contain all traces for a Bar Chart
    trace_vector = []
    # Check if elements_y is a single element or multiple
    if isinstance(elements_y,str):
        trace_vector.append(go.Bar(x=dataframe[element_x],y=dataframe[elements_y],name = elements_y))
    
    else:
        for element in elements_y:
            trace_vector.append(go.Bar(x=dataframe[element_x],y=dataframe[element],name = element))
    
    
    return trace_vector


"""********************     Figures generation    ********************"""

def generate_pie_chart(dataframe,elements,title='Unnamed pie chart'):

    # This function creates a plotable pie chart figure. It can create subplots containing
    # multiple pie_charts in case it is needed to segregate certain information into different
    # categories but visualised together
    # 
    # INPUTS:
    #   - dataframe
    #   - elements: this is an array of arrays (every position of which contains the names of a
    #               single pie_chart)
    #   - title
    # 
    # OUTPUTS:
    #   - pie chart figure  

    # Get the number of elements passed as parameter
    num_elements = len(elements)

    # Check if elements is a single vector or multiple to generate one or multiple pie_charts
    if isinstance(elements,(list,tuple)) and isinstance(elements[0],str):
        # elements is a vector (only 1 pie chart is needed)
        fig_trace = trace_pie(dataframe,elements,'')
        fig = go.Figure(fig_trace)

    else:
        # elements is a vector (more than 1 pie chart is needed)
        # Create subplots, we suppose that the user wants the plots to be one next to the other
        fig = make_subplots(
            rows=1,
            cols=num_elements,
            specs=[[{'type':'domain'}, {'type':'domain'}]]
        )
        
        # We use a integer loop so we can assign the subplot position of each pie chart
        for i in range(num_elements):
            fig.add_trace(trace_pie(dataframe,elements[i],''),1,i+1)

    fig.update_traces(hole=.4, hoverinfo="label+percent+name")

    fig.update_layout(title_text=title)
    
    return fig

def generate_multi_histogram(dataframe,elements,units='',start=-200,end=200,step=10, title='Unnamed distribution'):
    

    #First we generate the figure
    fig = go.Figure()
    
    # First, we need to check if elements is a vector or a string
    if isinstance(elements,str):
        x_values=[]
        for value in dataframe[elements]:
          x_values.append(value)  
        
        fig.add_trace(go.Histogram(
            x=x_values,
            histnorm='percent',
            name=elements,
            xbins=dict(
                start=start,
                end=end,
                size=step
            ),
            opacity=0.85
        ))
    else:
        #Now we add a new trace for every element
        num_elements = len(elements)
        for i in range(num_elements):
            x_values=[]
            for value in dataframe[elements[i]]:
                x_values.append(value)  
            
            fig.add_trace(go.Histogram(
                x=x_values,
                histnorm='percent',
                name=elements[i],
                xbins=dict(
                    start=start,
                    end=end,
                    size=step
                ),
                opacity=0.85
            ))
    
    #Final configuration of the figure
    fig.update_layout(
        title_text=title, # title of plot
        xaxis_title_text=units, # xaxis label
        yaxis_title_text='Percentage', # yaxis label
        bargap=0.2, # gap between bars of adjacent location coordinates
        bargroupgap=0.1 # gap between bars of the same location coordinates
    )

    # Add legend and display it in the top-right corner of the graph
    fig.update_layout(showlegend=True, legend=dict(x=0.85, y=0.95, traceorder='normal', orientation='v'))


    return fig

def generate_scatter_plot(dataframe,element_x,elements_y,title='Unnamed Scatter Plot',reg_line=False):
    # Returns a scatter plot trace, given a dataframe, and elements to plot, can integrate a regression
    # line if specified
    # 
    # INPUTS:
    #   - dataframe: containing all data
    #   - element_x: x axis data
    #   - elements_y: vector that contains all the different data to be plotted
    #   - title: title of the graph
    #   - reg_line: boolean to indicate if a reg_line is wanted. Default value is False
    # OUTPUTS:
    #   - plotly trace if OK
    #   - None if error occured
    
    # Plot generation for each data source passed as parameter elements_y
    
    # Generate a vector containing all traces to be plotted
    data_vector = trace_scatter_plot(dataframe,element_x,elements_y,reg_line)
    
    # Definition of the basic layout of the graphic, adding graphic title and the x_axis name
    layout = go.Layout(
        title = title,
        xaxis=dict(title=element_x)
    )

    # From all traces, we generate the figure
    fig = go.Figure(data=data_vector,layout=layout)

    # Add legend and display it in the top-right corner of the graph
    fig.update_layout(showlegend=True, legend=dict(x=0.85, y=0.95, traceorder='normal', orientation='v'))

    return fig

def generate_scatter_plot_user(dataframe,key_user,element_x,elements_y,title="Unnamed Scatter Plot",user_reg_line=False,reg_line=False):
    # Returns a scatter plot, given a dataframe, user and elements to plot, can integrate a regression
    # line if specified
    # 
    # INPUTS:
    #   - dataframe: containing all data
    #   - key user: ID of the user that data is needed
    #   - element_x: x axis data
    #   - elements_y: vector that contains all the different data to be plotted
    #   - title: title of the graph
    #   - user_reg_line: boolean to indicate if a reg_line for the user data is wanted. Default value is False
    #   - reg_line: boolean to indicate if a generic reg_line is needed (for generic, we mean a reg_line of all data of all vehicles)
    # OUTPUTS:
    #   - plotly figure if OK
    #   - None if error occured
  
    
    # Get user dataframe, if user is not found or '' is passed, plot a generic scatter plot
    # (omits the user particularity and generates a simple scatter plot)
    if key_user in dataframe.index:
        user_df = dataframe.loc[dataframe.index == key_user]
    else:
        fig = generate_scatter_plot(dataframe,element_x,elements_y,title,reg_line)
        return fig
        fig = generate_scatter_plot(dataframe,element_x,elements_y,title,reg_line)
        return fig

    # Use trace_scatter_plot to generate a figure containing all data, to do so, we'll use
    # an auxiliary vector containing all traces
    trace_vector = []

    # Append user data
    user_trace_vector = trace_scatter_plot(user_df,element_x,elements_y,user_reg_line)
    for user_trace in user_trace_vector:
        trace_vector.append(user_trace)

    # If a general trace is wanted
    if reg_line:
        generic_trace_vector = trace_trendline(dataframe,element_x,elements_y,'Generic Trendline')
        for generic_trace in generic_trace_vector:
            trace_vector.append(generic_trace)


   
    # Definition of the basic layout of the graphic, adding graphic title and the x_axis name
    layout = go.Layout(
        title = title,
        xaxis=dict(title=element_x)
    )

    # From all traces, we generate the figure
    fig = go.Figure(data=trace_vector,layout=layout)

    # Get the maximum and minimum value of element_x for better graph visualization
    x_max = user_df[element_x].max() 
    x_min = user_df[element_x].min() 
    fig.update_xaxes(range=[x_min,x_max])

    # Add legend and display it in the top-right corner of the graph
    fig.update_layout(showlegend=True, legend=dict(x=0.85, y=0.95, traceorder='normal', orientation='v'))


    return fig

def generate_line_chart(dataframe,element_x,elements_y,title='Unnamed Line Chart'):

    trace_vector=[]
    for element in elements_y:
        dataframe = dataframe.sort_values(by=[element_x,element])
        trace = go.Scatter(x=dataframe[element_x], y=dataframe[element], mode='lines', name=element)
        trace_vector.append(trace)

    # Definition of the basic layout of the graphic, adding graphic title and the x_axis name
    layout = go.Layout(
        title = title,
        xaxis=dict(title=element_x)
    )

    # From all traces, we generate the figure
    fig = go.Figure(data=trace_vector,layout=layout)
    
    return fig

def generate_bar_chart(dataframe,element_x,elements_y,title='Unnamed Bar Chart'):
    
    trace_vector = trace_bar_chart(dataframe,element_x,elements_y)

    fig = go.Figure(data=trace_vector)

    fig.update_layout(
        title = title,
        xaxis_title = element_x,
        barmode = 'group'               #Options available: group, stack, relative
    )

    # Add legend and display it in the top-right corner of the graph
    fig.update_layout(showlegend=True, legend=dict(x=0.85, y=0.95, traceorder='normal', orientation='v'))
    
    return fig

def generate_response_surface(dataframe,element_x,element_y,element_z,title='Unnamed Response Surface'):
    
    # To simplify notation, specify axis
    x = dataframe[element_x]
    y = dataframe[element_y]
    z = dataframe[element_z]

    # Generate a grid that will be used to display the 3D data. The xi and y1 rank, must 
    # reach all data from element_x and element_y
    x_grid = np.linspace(min(x),max(x),500)
    y_grid = np.linspace(min(y),max(y),500)
    x_grid, y_grid = np.meshgrid(x_grid,y_grid)

    # Interpolate data in the grid
    z_grid = interpolate.griddata((x, y), z, (x_grid, y_grid), method='cubic')
    
    # Generate surface from the interpolated grid
    fig = go.Figure(data=[go.Surface(z=z_grid, x=x_grid, y=y_grid)])
    
    # Add a topographic map to the figure
    fig.update_traces(contours_z=dict(
        show=True, 
        usecolormap=True,
        highlightcolor="limegreen",
        project_z=True))
    
    # Edit axis' names and aspect of the figure
    fig.update_layout(scene=dict(
        xaxis_title = element_x,
        yaxis_title = element_y,
        zaxis_title = element_z,
        aspectmode = 'cube'
    ))
    return fig

def generate_note(dataframe,notes):
    html_note = "<div class='note-container'>"+ "<ul class='list-notes'>"
    for note in notes:
        html_note += "<li class='list-notes-element'>"+note+"</li>"
    html_note += "</ul></div>"

    return html_note

"""********************     Dataframe funcitons    ********************"""

def df_from_xlsx_elements(file_route,index,rows,key_cols,elements):
    # Returns a dataframe containing all data passed as 'elements' structured following
    # 'key_cols'. Additionally, an index and number of rows has to be added.
    # Note that the dataframe is generated from an excel
    # 
    # INPUTS
    #   - file_route:   relative route to the excel file
    #   - index:        name of the column used as index
    #   - rows:         number of rows wanted for the dataframe 
    #   - key_cols:     name of the columns used to identify each vehicle in the dataframe
    #   - elements:     name of the data columns that we need to include in the dataframe
    # 
    # OUTPUT  
    #   -   dataframe generated

    # Read and save the xlsx file in 'excel' variable
    excel = pd.ExcelFile(file_route)

    # Generate an empty dataframe to which 'key_cols' will be added and index will be
    # determined
    custom_df = pd.DataFrame()
    num_key_cols = len(key_cols)
    key_cols_found = 0

    # This loop finds whether there are all 'key_cols' in one sheet, if so, copy them
    # onto the custom dataframe 'custom_df' and sets the index
    for sheet in excel.sheet_names:
        df = pd.read_excel(file_route, sheet_name=sheet, nrows=rows)

        for column_name in df.columns:
            for key_column in key_cols:
                if column_name == key_column:
                    key_cols_found += 1

        if key_cols_found == num_key_cols:
            custom_df = df[key_cols].copy()
            custom_df.set_index(index,inplace=True)
            break
        
        key_cols_found=0
    
    # Once the custom dataframe has all the key columns, add the elements to be included
    # in the custom dataframe

    num_elements = len(elements) # used to stop the for loop when all elements have been added
    elements_found = 0

    # Create auxiliary list used to merge both the custom_df with the data selected
    columns_to_merge=[]
    for element in key_cols:
        if element != index:
            columns_to_merge.append(element)

    # Iterate through the excel sheets
    for sheet in excel.sheet_names:
        df = pd.read_excel(file_route, sheet_name=sheet, index_col=index, nrows=rows)

        for column_name in df.columns:
            for element in elements:
                if column_name == element:
                    columns_to_merge.append(element)                                #add to the auxiliary list the element to merge
                    custom_df.drop_duplicates(subset=custom_df, inplace=True)       # Drop duplicates is used to prevent duplicated rows
                    df.drop_duplicates(subset=df, inplace=True)
                    custom_df = pd.merge(custom_df,df[columns_to_merge],on=key_cols,how='inner')
                    columns_to_merge.pop()                                          #retrieve it for the next iteration
                    elements_found += 1
        
        if(elements_found == num_elements):
            break
    custom_df = custom_df.dropna(axis=1) # erase any column with NaN

    # Reorganise data (not strictly necessary, helpfull to debug)
    custom_df = custom_df.sort_values(by=key_cols)

    return custom_df

def df_from_xlsx_vehicle(file_route, rack_number, index='VIN', check_columns=['Id', 'Timestamp']):
    # Read and save the xlsx file in 'excel' variable
    excel = pd.ExcelFile(file_route)

    # Generate an empty dataframe to which all information will be stored
    custom_df = pd.DataFrame()
    custom_df[index] = None
    for element in check_columns:
        custom_df[element] = None
    custom_df.set_index(index, inplace=True)

    for sheet in excel.sheet_names:
        df = pd.read_excel(file_route, sheet_name=sheet, index_col=index)

        # Check if sheet has all key columns
        if all(col in df.columns for col in check_columns):
            if rack_number in df.index:
                fila = df.loc[rack_number]
                custom_df = pd.merge(custom_df, fila, on=check_columns, how='right')
                custom_df = custom_df.dropna(axis=1)

    return custom_df

def df_from_parquet_elements(file_path:str,elements:tuple=None, samples:int=None) -> pd.DataFrame:
    # Read and save the data file (.parquet) into a dataframe. If the file_path is not found,
    # return -1
    if not os.path.exists(file_path):
        return -1
    df = pd.read_parquet(file_path)
    
    # Copy desired columns onto custom_df. If samples is None, that means that all rows need
    # to be copied. Only "samples" number of rows copied if otherwise.
    if elements == None:
        if samples == None:
            return df
        custom_df = df[:samples].copy()
        return custom_df
    
    # If we get to this point, elements is a tuple and we have to copy only the columns passed as
    # parameter

    # Checks if all elements requested are contained in the original file
    if not (all(column in df.columns for column in elements)):
        return -1
    
    if samples == None: 
        custom_df = df[elements].copy()
    else:
        custom_df = df[elements][:samples].copy()
    
    return custom_df

def df_from_parquet_vehicle(file_path:str, rack_number:int) -> pd.DataFrame:
    # This function generates a dataframe which will contain all columns given a rack_number
    # from an already existing dataframe (which contains all data from all vehicles). The file
    # path of the data source has to be passed as parameter and it has to lead to a .parquet file
    # 
    # INPUTS:
    #   - file_path: relative path to the parquet file
    #   - rack_number: VIN of vehicle needed to plot
    # 
    # OUTPUT:
    #   - -1 in case the file path is not correct
    #   - custom_df: df containing all data of VIN's vehicle
    
    # Read and save the data file (.parquet) into a dataframe. If the file_path is not found,
    # return -1
    if not os.path.exists(file_path):
        return -1
    df = pd.read_parquet(file_path)
    
    # Filter by rack_number, which in this case, is the index of the dataframe
    custom_df = df.loc[rack_number]

    return custom_df

def df_get_elements_tag(dataframe:pd.DataFrame):
    # This vector returns a vector containing all names of all columns and the name
    # of the index in case there is one given a dataframe dataframe
    # 
    # INPUTS
    #   - dataframe:    dataframe to read
    # 
    # OUTPUTS
    #   - index:        name of the index, None if index is default
    #   - tags_vector:  vector containing all names of the dataframe

    # Get all columns (this will not include the index if there is one)
    tags_vector=[]

    for element in dataframe.columns:
        tags_vector.append(element)
    
    # Check if the index is the default: 0, 1, 2, 3, .... len(dataframe)-1
    if dataframe.index.equals(pd.RangeIndex(start=0, stop=len(dataframe), step=1)):
        index = None
    
    else:
        index = dataframe.index.name

    return index, tags_vector

def df_check_user_values(usr_dataframe):
    # Load the JSON file
    #INPUT
    #usr_dataframe: Un DataFrame de pandas que contiene los datos que se van a verificar. Los nombres de las columnas del DataFrame representan los elementos cuyos valores se verificarán.
    #   
    #OUTPUTS
    #   - result:Devuelve True si todos los valores están dentro de los rangos, y False si al menos un valor está fuera de los rangos o si hay elementos no encontrados en el archivo JSON.
    #elements_check: Un diccionario que contiene información detallada sobre la verificación de cada elemento. Para cada elemento, se almacenan los resultados de la verificación mínima (Check_min), la verificación máxima (Check_max).Este diccionario proporciona detalles sobre qué valores no cumplen con los criterios de verificación.
    
    with open('param_batery.json', 'r') as archivo:
        dict_param = json.load(archivo)

    result = True
    elements_check = {}

    for element in usr_dataframe.columns:
        min_value = dict_param[element]['minimum']
        max_value = dict_param[element]['maximum']
        
        check_min = True  # Initialize the verification variables
        check_max = True

        for value in usr_dataframe[element]:
            if value < min_value or value > max_value:
                check_min = False
                check_max = False

        elements_check[element] = {
            'Check_min': check_min,
            'Check_max': check_max,
            'Check': check_min or check_max
        }

        if not elements_check[element]['Check']:
            result = False

    return result, elements_check


"""********************     Parquet Files functions    ********************"""

def df_generate_month_df(file_path:str,type_name:str,year:int,month:int) -> pd.DataFrame:
    # Given a month and year, generates a dataframe containing all "data_to_save" information
    # which will be further (in another function) appended to the parquet file that contains
    # all months.
    # 
    # From the month and year, it will search the corresponding document in the folder df
    # 
    # IMPORTANT: The function saves the mean value of the columns to be saved
    # 
    # INPUT
    # INPUT
    #   - dataframe:        dataframe containing all data   
    # INPUT  
    #   - dataframe:        dataframe containing all data   
    #   - data_to_save:     columns to be "meaned" and saved in the new df
    #   - month, year:      integers to indicate the month and year of the dataframe
    # 
    # OUTPUT
    #   - -1 if no file matches the date
    #   - df_month

    """ Se suposa que els noms de les columnes son correctes i no s'ha de fer cap check """
    MONTHLY_DATA_TRIP = ['Mins','Max speed','Total (km)','Total energy (Wh)','Inv  min T (°C)']
    MONTHLY_DATA_CHARGE = ['Min temp I','Max temp I']

    df = pd.read_parquet(file_path)

    if type_name == 'trip':
        # Generate a new dataframe containing the necessary columns from both vectors    
        df_month = pd.DataFrame(columns = MONTHLY_DATA_TRIP)
        for column_tag in MONTHLY_DATA_TRIP:
            df_month[column_tag] = None   
        
        # Add to the dataframe all columns to be stored. Note that the value saved is
        # the average 
        mean_trip = pd.DataFrame(df[MONTHLY_DATA_TRIP].mean()).transpose()
        df_month[MONTHLY_DATA_TRIP] = mean_trip

    elif type_name == 'charge':
        # Generate a new dataframe containing the necessary columns from both vectors    
        df_month = pd.DataFrame(columns = MONTHLY_DATA_CHARGE)
        for column_tag in MONTHLY_DATA_CHARGE:
            df_month[column_tag] = None   
        
        # Add to the dataframe all columns to be stored. Note that the value saved is
        # the average 
        mean_trip = df[MONTHLY_DATA_CHARGE].mean()
        df_month[MONTHLY_DATA_CHARGE] = mean_trip
    
    else:
        return -1

    # Generate the date string and update df_month
    date_string = f'{year}-{month:02}'
    date = np.datetime64(date_string)
    df_month['Date'] = [date]

    return df_month

def df_add_df_to_parquet_file(file_path:str,df_new:pd.DataFrame) -> pd.DataFrame:
    # This function will generate and modify a new .parquet given a filename
    # and dataframe to ba added.
    # 
    # This function is internally used to generate/edit the trip, charge and critical
    # data files. In case there is no file created and placed into the df directory,
    # a new file is created. Plus, if there is no df/ directory, a new folder is created
    # in order to store subsequent data
    # 
    # INPUT:
    #   - file_path
    #   - df_new: dataframe containing new data to be stored
    # 
    # OUTPUT:
    #   - Resulting dataframe
    
    # If file exists
    if os.path.exists(file_path):
        # Read and add new data. Then deletes any duplicated rows
        # before overwriting the .parquet file
        df_exist = pd.read_parquet(file_path)
        df_final = pd.concat([df_exist,df_new])

        # Erase possible duplicates and sort rows by ascending date
        df_final.drop_duplicates(subset='Date',keep='last',inplace=True)
        df_final.sort_values(by='Date',ascending=True,inplace=True)

        # Overwrite file
        table = pa.Table.from_pandas(df_final)
        pq.write_table(table,file_path)
       
        return df_final

    # If file does not exist, check if there's a folder to add
    # the new file. If there is not any directory, create one
    if not (os.path.exists('df') and os.path.isdir('df')):
       os.makedirs('df')

    # Generate the new file
    table = pa.Table.from_pandas(df_new)
    pq.write_table(table,file_path)
    
    return df_new

def df_append_data(df_new:pd.DataFrame, type_name:str) -> int:

    timestamp_max=df_new['Timestamp'].max()
    date_max=datetime.datetime.utcfromtimestamp(timestamp_max)
    year_max=date_max.year
    month_max=date_max.month
    timestamp_min=df_new['Timestamp'].min()
    date_min=datetime.datetime.utcfromtimestamp(timestamp_min)
    year_min=date_min.year
    month_min=date_min.month

     # Get the timestamp corresponding to the start of the new month
    START_OF_MONTH = np.datetime64(f'{year_max}-{month_max:02}-01T00:00:00')
    START_OF_MONTH_TIMESTAMP = START_OF_MONTH.astype(np.int64)
    
    #All the data are from the same month
    if month_min == month_max:
        filename=f'df/{year_min}_{month_min:02}_{type_name}.parquet'
        df_add_df_to_parquet_file(filename,df_new)
    
    #Data are from the different month
    else:
        df_new_month = pd.DataFrame()
        for index, row_data in df_new.iterrows():
            # Get the timestamp corresponding to the start of the new month

            # Compare if the row corresponds to this or previous month
            if row_data['Timestamp']> START_OF_MONTH_TIMESTAMP:
                aux_df = pd.DataFrame(row_data).transpose()
                df_new_month = pd.concat([df_new_month,aux_df])
                # Delete this column (cannot use index since it will delete all rows with same index)
                df_new = df_new[~((df_new['Timestamp'] == row_data['Timestamp']) & (df_new.index == index))]
        
        filename_new_month=f'df/{year_max}_{month_max:02}_{type_name}.parquet'
        df_add_df_to_parquet_file(filename_new_month,df_new_month)

        filename_last_month=f'df/{year_min}_{month_min:02}_{type_name}.parquet'
        df_add_df_to_parquet_file(filename_last_month,df_new)
        

    
    if timestamp_min < START_OF_MONTH_TIMESTAMP:
        if month_min == 1:
            df_add_month_to_critical_data(filename_last_month,type_name, year_min-1, 12)
        else:
            df_add_month_to_critical_data(filename_last_month,type_name, year_min, month_min)
    return 0
    
def df_add_month_to_critical_data(df_file_path:str, type_name:str, year:int, month:int) -> pd.DataFrame:
    # This function will either create critical_data.parquet and add this 
    # month's critical data or just add the critical data to an existing file
    # 
    # INPUT:
    #   - df_file_path: relative path to the .parquet file that contains the month's
    #                   data
    # 
    # OUTPUT:
    #   - new_month_df: dataframe that has been stored into a .parquet file
    
    # Check if there's any months.parquet file, if not, return -1
    MONTHS_FILE_PATH = 'df/critical_data.parquet'
    month_df = df_generate_month_df(df_file_path,type_name,year,month)

    new_month_df = df_add_df_to_parquet_file(MONTHS_FILE_PATH,month_df)

    return new_month_df

def df_get_last_months_critical_data(num_months:int) -> pd.DataFrame:
    # Returns a dataframe containing the critical data stored in month.parquet.
    # The number of columns will be fixed by "num_columns" so that if the last
    # x months are requestet. A dataframe containing the last x months will be
    # returnes
    # 
    # INPUT:
    #   - num_months: number of last month that is wanted to be plotted
    # 
    # OPUTPUT:
    #   - total_df: concatenation of num_months' dataframes

    # Check if there's any months.parquet file, if not, return -1
    MONTHS_FILE_PATH = 'df/critical_data.parquet'
    if not os.path.exists(MONTHS_FILE_PATH):
        return -1
    
    aux_df = pd.read_parquet(MONTHS_FILE_PATH)

    # Get the last "num_months" columns from the critical data file
    # It checks whether num_months is greater than the number of rows available
    # to avoid errors
    last_months_df = aux_df.tail(min(num_months,aux_df.shape[0]))

    return last_months_df

def df_get_columns_tag(dataframe):
    # Given a dataframe, this function can be used to get all the columns' name
    # in a tuple
    # 
    # INPUTS:
    #   - dataframe
    # 
    # OUTPUT:
    #   - tag_vector

    tag_vector = []
    for columna in dataframe.columns:
        tag_vector.append(columna)

    return tag_vector

def resolution(df,type_name:str):
    
    # Nombres de las columnas ordenadas por resolución
    Route_resolution01 = ["End odometer", "City (km)","Sport (km)","Flow (km)","Sail (km)","Regen (km)","Motor avg T (°C)","Thermal current","Max temp","Min temp","Max delta","Avg delta"]
    Route_resolution001 = ["Regen (%)", "Start SoC ","End SoC ","SoC delta (%)","Avg temp"]
    Route_resolution0001 = ["Max discharge ", "Max regen","Avg current","Max V","Average V","Min V","Max cell V","Min cell V","Cell V diff","Min temp","Avg delta"]
    Load_resolution01 = ["Max charger current","Min temp I","Max temp I","Min temp F","Max temp F","Min temp","Max temp","Cycles","Max temp","Min temp"]
    Load_resolution001 = ["SoC i", "SoC f","Charger max P","Avg temp I","Avg temp F","Age","uSoC I","uSoC F"]
    Load_resolution0001 = ["Vmin I", "Vavg I","Vmax I","Vmin F","Delta V I","Avg final V","Max final V","Max BMS current","Min temp"]

    if type_name=="Route":
    # Iterar sobre las columnas y multiplicarlas por el factor 0,1 (Route)
        for parameter in Route_resolution01:
            df[parameter] = df[parameter] * 0.1
        
        # Iterar sobre las columnas y multiplicarlas por el factor 0,01 (Route)
        for parameter in Route_resolution001:
            df[parameter] = df[parameter] * 0.01

        # Iterar sobre las columnas y multiplicarlas por el factor 0,001 (Route)
        for parameter in Route_resolution0001:
            df[parameter] = df[parameter] * 0.001

    if type_name=="Load":
        # Iterar sobre las columnas y multiplicarlas por el factor 0,1 (Load)
        for parameter in Load_resolution01:
            df[parameter] = df[parameter] * 0.1
        
        # Iterar sobre las columnas y multiplicarlas por el factor 0,01 (Load)
        for parameter in Load_resolution001:
            df[parameter] = df[parameter] * 0.01

        # Iterar sobre las columnas y multiplicarlas por el factor 0,001 (Load)
        for parameter in Load_resolution0001:
            df[parameter] = df[parameter] * 0.001

    return df
