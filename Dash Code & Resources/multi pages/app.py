import base64
import io
import pandas as pd
import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table, no_update, State
import plotly.express as px
import json
import datetime, time
from flask_caching import Cache
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

# Initialize the app with a Dash Bootstrap theme and external stylesheets
external_stylesheets = [dbc.themes.CERULEAN, 'styles.css']
app = Dash(__name__, use_pages=True, external_stylesheets=external_stylesheets)

# Create a navigation bar using Bootstrap components
navbar = dbc.NavbarSimple(
    children=[

        # Generate navigation links for each registered page
        dbc.NavItem(dbc.NavLink(f'{page["name"]}', href=page['relative_path']))
        for page in dash.page_registry.values()
    ],
    color='primary',
    dark=True,
)

# App layout, including the navigation bar and a container for subpages
app.layout = html.Div(children=[
    navbar,
    dbc.Container([

        # This is where the content of the individual pages will be rendered
        dbc.Row([
            dash.page_container
        ], className='mt-5'),
    ]),
])

if __name__ == '__main__':
    app.run(debug=True)
