from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.express as px
import pandas as pd


df = pd.read_csv("kiva_el.csv")

app = Dash(__name__)

app.layout = html.Div(
    [
        dcc.Graph(id="graph-with-slider"),
        dcc.Slider(
            id="year-slider",
            min=df["year"].min(),
            max=df["year"].max(),
            value=df["year"].min(),
            marks={str(year): str(year) for year in df["year"].unique()},
        ),
    ]
)


@app.callback(Output("graph-with-slider", "figure"), [Input("year-slider", "value")])
def update_graph(slected_year):
    filtered_df = df[df["year"] == slected_year]
    fig = px.scatter(
        filtered_df,
        x="funded_amount",
        y="term_in_months",
        size="lender_count",
        color="sector",
        hover_name="region",
        size_max=45,
    )

    fig.update_layout(transition_duration=600)

    return fig


if __name__ == "__main__":
    app.run_server()