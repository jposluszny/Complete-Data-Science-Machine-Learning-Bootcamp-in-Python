import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from app import app
import pandas as pd

df = pd.read_csv("../kiva_el.csv")

layout = html.Div(
    [
        html.Nav(
            [
                dcc.Link(
                    "Home with Drop Down ",
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


@app.callback(Output("graph-with-slider", "figure"), [Input("year-slider", "value")])
def update_figure(selected_year):
    filtered_df = df[df["year"] == selected_year]

    fig = px.scatter(
        filtered_df,
        x="funded_amount",
        y="term_in_months",
        size="lender_count",
        color="sector",
        hover_name="region",
        log_x=True,
        size_max=45,
    )

    fig.update_layout(transition_duration=600)

    return fig
