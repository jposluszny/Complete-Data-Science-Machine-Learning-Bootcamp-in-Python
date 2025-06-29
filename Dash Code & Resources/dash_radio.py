from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.express as px
import pandas as pd

app = Dash(__name__)

df = pd.read_csv("kiva_el.csv")
months = df["month"].unique()
sectors = df["sector"].unique()

app.layout = html.Div(
    [
        html.Div(
            [
                dcc.Dropdown(
                    id="sectors-field",
                    options=[{"label": sector, "value": sector} for sector in sectors],
                    multi=True,
                    value=["Agriculture"],
                )
            ],
            style={"width": "50%"},
        ),
        html.Div(
            [
                dcc.RadioItems(
                    id="months-field",
                    options=[{"label": month, "value": month} for month in months],
                    value="January",
                )
            ],
            style={"width": "48%", "float": "right"},
        ),
        html.Div([dcc.Graph(id="my-graph")], style={"marginTop": "50px"}),
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
    Output("my-graph", "figure"),
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
        & (df["month"] == month)
    ]
    fig = px.scatter(dff, x="funded_amount", y="lender_count", color="day")
    fig.update_layout(transition_duration=1000)

    return fig


if __name__ == "__main__":
    app.run_server()
