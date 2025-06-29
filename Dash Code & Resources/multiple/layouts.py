import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

df = pd.read_csv("kiva_el.csv")
sectors = df["sector"].unique()
months = df["month"].unique()

layout_scatter = html.Div(
    [
        html.Nav(
            [
                dcc.Link("Home with Drop Down", href="/apps/home", className="nav-item nav-link"),
                dcc.Link("Scatter Plot", href="/apps/scatter", className="nav-item nav-link"),
            ],
            className="navbar navbar-expand-lg navbar-light bg-light",
        ),
        html.Div([html.Img(src="/assets/logo.png")], style={"textAlign": "center"}),
        html.Div(
            [
                dcc.Graph(id="graph-with-slider"),
                dcc.Slider(
                    id="year-slider",
                    min=df["year"].min(),
                    max=df["year"].max(),
                    value=df["year"].min(),
                    marks={str(year): str(year) for year in df["year"].unique()},
                ),
            ],
            className="container",
        ),
    ]
)

layout_home = html.Div(
    [
        html.Nav(
            [
               dcc.Link("Home with Drop Down", href="/apps/home", className="nav-item nav-link"),
                dcc.Link("Scatter Plot", href="/apps/scatter", className="nav-item nav-link"),
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