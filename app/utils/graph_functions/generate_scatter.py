import plotly.express as px
from flask import jsonify
def generate_scatter_plot(x_data, y_data, title):
    fig = px.scatter(x=x_data, y=y_data, title=title)   

    #fig.update_layout(width=850,height=390)
    fig.update_layout({'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    serialized_fig = fig.to_json()

    return serialized_fig
