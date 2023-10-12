import plotly.express as px

def generate_scatter_plot(x_data, y_data, title):
    fig = px.scatter(x=x_data, y=y_data, title=title)   

    return fig.to_html(full_html=False)
