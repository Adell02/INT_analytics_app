import plotly.express as px

from app.utils.graph_functions.generate_dashboard_graphics import serialize_figures

def generate_map(df,selected):
    fig = px.density_mapbox(
        df,
        lat='lat',
        lon='lon',
        z=selected,
        radius=10,
        center=dict(lat=df['lat'][0],lon=df['lon'][0]),
        zoom=5,
        mapbox_style="open-street-map",  
        custom_data=["VIN","ID"],             
        hover_data=["lat","lon",selected,"VIN","ID"]
    )
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))

    ser_fig = serialize_figures([fig])[0]
    return ser_fig

def generate_void_map(df):
    fig = px.density_mapbox(
        df,
        lat='lat',
        lon='lon',
        z="",
        radius=10,
        center=dict(lat=41.388074861528644 ,lon=2.112470352957808),
        zoom=5,
        mapbox_style="open-street-map",                
        #hover_data=dict(lat=False,lon=False)
    )
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))

    ser_fig = serialize_figures([fig])[0]
    return ser_fig