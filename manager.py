
from dash import html, dcc
import plotly.express as px
from utils.data_loader import load_data

df = load_data()

def layout():
    fig = px.histogram(df, x="Age", title="Employee Age Distribution")

    return html.Div([
        html.H2("Admin Dashboard"),
        dcc.Graph(figure=fig)
    ])
