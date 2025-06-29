import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from app import app


df = pd.read_csv("../kiva_el.csv")

sectors = df["sector"].unique()
months = df["month"].unique()

layout = html.Div(
    [
        html.Nav(
            [
                dcc.Link(
                    "Home with Drop Down",
                    href="/apps/home",
                    className="nav-item nav-link",
                ),
                dcc.Link(
                    "Scatter Plot", href="/apps/scatter", className="nav-item nav-link"
                ),
            ],
            className="navbar navbar-expand-lg navbar-light bg-light",
        ),
        html.Div([html.Img(src="/assets/logo.png")], style={"textAlign": "center"}),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Dropdown(
                                    id="sectors-field",
                                    options=[{"label": i, "value": i} for i in sectors],
                                    multi=True,
                                    value=["Agriculture"],
                                )
                            ],
                            style={"width": "48%", "display": "inline-block"},
                        ),
                        html.Div(
                            [
                                dcc.Checklist(
                                    id="months-field",
                                    options=[{"label": i, "value": i} for i in months],
                                    value=["January"],
                                    className="form-check-input",
                                )
                            ],
                            className="form-check form-check-inline",
                        ),
                    ]
                ),
                dcc.Graph(id="indicator-graphic"),
                dcc.Slider(
                    id="year-slider",
                    min=df["year"].min(),
                    max=df["year"].max(),
                    value=df["year"].max(),
                    marks={str(year): str(year) for year in df["year"].unique()},
                ),
            ],
            className="container",
        ),
    ]
)


@app.callback(
    Output("indicator-graphic", "figure"),
    [
        Input("sectors-field", "value"),
        Input("months-field", "value"),
        Input("year-slider", "value"),
    ],
)
def update_graph(sector, month, year_value):
    dff = df[
        (df["year"] == year_value)
        & (df["sector"].isin(sector))
        & (df["month"].isin(month))
    ]

    fig = px.scatter(dff, x="funded_amount", y="lender_count", color="month")

    fig.update_layout(transition_duration=1000)

    return fig
