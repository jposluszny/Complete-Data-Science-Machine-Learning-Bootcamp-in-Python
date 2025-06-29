import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output
from plotly import express as px

app = dash.Dash(__name__)

px.set_mapbox_access_token("YOUR_MAP_BOX_KEY")

df = pd.read_csv("kiva_el.csv")
sectors = df["sector"].unique()

app.layout = html.Div(
    [
        dcc.Dropdown(
            id="sector",
            value=["Agriculture"],
            options=[{"label": i, "value": i} for i in sectors],
            multi=True,
        ),
        dcc.Loading(children=[dcc.Graph(id="chart")], type="circle"),
    ]
)


@app.callback(Output("chart", "figure"), [Input("sector", "value")])
def my_chart(value):
    dff = df[df["sector"].isin(value)]
    fig = px.scatter_mapbox(
        dff,
        lat="lat",
        lon="lon",
        color="region",
        size="loan_amount",
        color_continuous_scale=px.colors.cyclical.IceFire,
        size_max=15,
    )
    return fig


if __name__ == "__main__":
    app.run_server()
