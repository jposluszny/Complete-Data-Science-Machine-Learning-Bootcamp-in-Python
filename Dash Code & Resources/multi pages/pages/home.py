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

# Register the page and create url
dash.register_page(__name__, path='/')

path = 'Dash Code & Resources/kiva.csv'

# Create layout
layout = html.Div([

    # Create a storage component to store JSON data in the client's browser session.
    dcc.Store(id='storage', storage_type='session'),

    # Hidden div component used to trigger the initial data-loading callback.
    html.Div(id='hidden-div', style={'display': 'none'}),
    html.H3('Data used for this application'),

    # Display a loading spinner and the data table.
    dcc.Loading(id='loading', type='default', children=[ 

       ]
    ),
]),

@callback(
    Output('storage', 'data'), 
    Input('hidden-div', 'children'))
def load_data_to_store(value):
    ''' Loads data from a CSV file and stores it in the client's browser session. '''

    df = pd.read_csv(path)
    return df.to_dict('records')

@callback(
    Output('loading', 'children'), 
    Input('storage', 'data'))
def create_data_table(data):
    ''' Creates a Dash DataTable to present the data loaded from the storage. '''

    if data:
        table = dash_table.DataTable(id='table', data=data, page_action='native', page_size=7, 
        style_table={'overflowX': 'auto'}, style_cell={'textAlign': 'left', 'padding': '10px'})
        return table
    return no_update
