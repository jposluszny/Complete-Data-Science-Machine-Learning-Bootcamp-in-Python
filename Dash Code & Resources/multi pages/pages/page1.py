import dash
from dash import html

dash.register_page(__name__, path='/page1')

layout = html.Div([
    html.H1('This is our page1'),
    html.Div('This is our page1 content.'),
])