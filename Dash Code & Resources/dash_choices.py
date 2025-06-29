from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.express as px
import pandas as pd


df = pd.read_csv("kiva_el.csv")
sectors = df["sector"].unique()

app = Dash(__name__)

app.layout = html.Div(
    [
        html.Div(
            [
                dcc.Dropdown(
                    id="sector-field",
                    options=[{"label": sector, "value": sector} for sector in sectors],
                    multi=True,
                    value=["Agriculture"],
                )
            ],
            style={"width": "50%"},
        ),
        dcc.Graph(id="my_graph"),
        dcc.Slider(
            id="year-slider",
            min=df["year"].min(),
            max=df["year"].max(),
            value=df["year"].min(),
            marks={str(year): str(year) for year in df["year"].unique()},
        ),
    ]
)


@app.callback(
    Output("my_graph", "figure"),
    [Input("sector-field", "value"), Input("year-slider", "value")],
)
def update_graph(sector, year_value):
    dff = df[(df["year"] == year_value) & df["sector"].isin(sector)]
    fig = px.scatter(dff, x="funded_amount", y="lender_count", color="day")
    fig.update_layout(transition_duration=6000)

    return fig


if __name__ == "__main__":
    app.run_server()
