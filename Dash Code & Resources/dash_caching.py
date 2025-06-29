import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output
from flask_caching import Cache  # pip install flask_caching
from plotly import express as px

app = dash.Dash(__name__)

cache = Cache(
    app.server, config={"CACHE_TYPE": "filesystem", "CACHE_DIR": "cache-folder"}
)

TIMEOUT = 60


@cache.memoize(timeout=TIMEOUT)
def fetch_data():
    df = pd.read_csv("kiva_el.csv")
    return df


app.layout = html.Div(
    [
        dcc.Dropdown(
            id="sector",
            value="Agriculture",
            options=[{"label": i, "value": i} for i in fetch_data()["sector"].unique()],
        ),
        dcc.Graph(id="chart"),
    ]
)


@app.callback(Output("chart", "figure"), [Input("sector", "value")])
def my_chart(value):
    df = fetch_data()
    dff = df[df["sector"] == value]
    fig = px.pie(dff, names="repayment_interval", values="lender_count")

    return fig


if __name__ == "__main__":
    app.run_server()