import base64
import io
from dash.exceptions import PreventUpdate
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px

import pandas as pd

df = pd.read_csv("kiva_el.csv")
sectors = df["sector"].unique()

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.Div(
            id="selected-df",
            style={
                "display": "none",
            },
        ),
        html.Div(
            [
                dcc.Dropdown(
                    id="sector-field",
                    options=[{"label": sector, "value": sector} for sector in sectors],
                    value="Agriculture",
                ),
            ],
            style={"width": "50%"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id="scatter-plot"),
                    ],
                    style={"width": "49%", "display": "inline-block"},
                ),
                html.Div(
                    [dcc.Graph(id="pie-chart")],
                    style={"width": "49%", "float": "right", "display": "inline-block"},
                ),
            ]
        ),
    ]
)


@app.callback(Output("selected-df", "children"), [Input("sector-field", "value")])
def manipulate_data(activitiy):
    data = df[df["sector"] == activitiy]
    return data.to_json()


@app.callback(Output("scatter-plot", "figure"), [Input("selected-df", "children")])
def scatter_chart(data):
    dff = pd.read_json(data)
    fig = px.scatter(dff, x="funded_amount", y="lender_count", color="day")

    return fig


@app.callback(
    Output("pie-chart", "figure"),
    [Input("selected-df", "children"), Input("sector-field", "value")],
)
def display_pie_chart(data, sector):
    dff = pd.read_json(data)
    fig = px.pie(
        dff,
        values="funded_amount",
        names="day",
        title=f"Funded Amount Vs Day for {sector}",
    )

    return fig


if __name__ == "__main__":
    app.run_server()