import plotly.express as px
import plotly.offline as opy

def generate_scatter_plot(x_data, y_data, title):
    fig = px.scatter(x=x_data, y=y_data, title=title)
    return opy.plot(fig, output_type='div', include_plotlyjs=False)
