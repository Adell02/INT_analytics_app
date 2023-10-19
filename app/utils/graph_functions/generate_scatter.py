import plotly.express as px

def generate_scatter_plot(x_data, y_data, title):
    fig = px.scatter(x=x_data, y=y_data, title=title)   

    fig.update_layout(width=850,height=390)
    fig.update_layout({'paper_bgcolor': 'rgba(0, 0, 0, 0)'})

    return fig.to_html(full_html=False)
