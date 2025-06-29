from dash.dependencies import Input, Output
from app import app
import dash
from dash.dependencies import Input, Output
import plotly.express as px
from app import app
import pandas as pd

df = pd.read_csv("kiva_el.csv")

@app.callback(Output("graph-with-slider", "figure"), [Input("year-slider", "value")],)
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