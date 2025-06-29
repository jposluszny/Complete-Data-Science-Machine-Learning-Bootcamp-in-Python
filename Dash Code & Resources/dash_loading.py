import dash
import time
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output
from plotly import express as px

app = dash.Dash(__name__)

df = pd.read_csv("kiva_el.csv")

app.layout = html.Div(
    [
        dcc.Dropdown(
            id="sector",
            value="Agriculture",
            options=[{"label": i, "value": i} for i in df["sector"].unique()],
        ),
        dcc.Loading(children=[dcc.Graph(id="chart")], type="graph"),
    ]
)


@app.callback(Output("chart", "figure"), [Input("sector", "value")])
def my_chart(value):
    time.sleep(3)
    dff = df[df["sector"] == value]
    fig = px.pie(dff, names="repayment_interval", values="lender_count")
    return fig


if __name__ == "__main__":
    app.run_server()
