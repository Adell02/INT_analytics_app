import plotly.express as px
from flask import jsonify
def generate_scatter_plot(x_data, y_data, title):
    fig = px.scatter(x=x_data, y=y_data, title=title)   

    fig.update_layout({'paper_bgcolor': 'rgba(0, 0, 0, 0)'},margin=dict(l=20, r=20, t=55, b=20))
    serialized_fig = fig.to_json()

    return serialized_fig
