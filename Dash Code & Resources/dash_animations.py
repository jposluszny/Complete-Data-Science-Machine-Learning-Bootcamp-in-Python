import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output
from plotly import express as px

app = dash.Dash(__name__)

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
    fig = px.scatter(
        dff,
        x="loan_amount",
        y="lender_count",
        animation_frame="month",
        animation_group="activity",
        size="lender_count",
        color="sector",
        category_orders={
            "month": [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December",
            ]
        },
    )
    return fig


if __name__ == "__main__":
    app.run_server()
