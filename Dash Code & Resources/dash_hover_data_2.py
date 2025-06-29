import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html
import pandas as pd
import plotly.express as px
import json

app = dash.Dash(__name__)

df = pd.read_csv("kiva_el.csv")

sectors = df["sector"].unique()
customdata = ["month"]


app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            id="sector-field",
                            options=[{"label": i, "value": i} for i in sectors],
                            value="Agriculture",
                        ),
                    ],
                    style={"width": "49%", "display": "inline-block"},
                ),
            ]
        ),
        html.Div(
            [
                dcc.Graph(
                    id="scatter-plot", hoverData={"points": [{"customdata": "January"}]}
                )
            ],
            style={"width": "49%", "display": "inline-block", "padding": "0 20"},
        ),
        html.Div(
            [
                dcc.Graph(id="pie-chart"),
            ],
            style={"display": "inline-block", "width": "49%", "float": "right"},
        ),
    ]
)


@app.callback(Output("scatter-plot", "figure"), [Input("sector-field", "value")])
def scatter_plot(sector):
    dff = df[df["sector"] == sector]
    fig = px.scatter(
        dff, x="funded_amount", y="lender_count", color="day", custom_data=customdata
    )

    return fig


@app.callback(
    Output("pie-chart", "figure"),
    [Input("scatter-plot", "hoverData"), Input("sector-field", "value")],
)
def pie_chart(hoverData, sector):
    dff = df[
        (df["sector"] == sector)
        & (df["month"] == hoverData["points"][0]["customdata"][0])
    ]
    fig = px.pie(
        dff,
        values="funded_amount",
        hole=0.3,
        names="day",
        title=f"Funded Amount vs Day Count for {hoverData['points'][0]['customdata'][0]} ",
    )

    return fig


if __name__ == "__main__":
    app.run_server()
