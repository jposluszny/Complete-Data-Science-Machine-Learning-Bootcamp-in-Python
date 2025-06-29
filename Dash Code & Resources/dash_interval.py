import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from plotly import express as px
from dash.exceptions import PreventUpdate

app = dash.Dash(__name__)

df = pd.read_csv("kiva_el.csv")
sectors = df["sector"].unique()

app.layout = html.Div(
    [
        dcc.Interval(
            id="interval-component",
            interval=2000,
            max_intervals=13,
        ),
        dcc.Graph(id="chart"),
    ]
)


@app.callback(
    Output("chart", "figure"),
    [Input("interval-component", "n_intervals")],
)
def my_chart(n_intervals):
    if n_intervals is None:
        raise PreventUpdate
    else:
        dff = df[df["sector"] == sectors[n_intervals]]
        fig = px.pie(
            dff,
            names="activity",
            values="lender_count",
            title=f"{sectors[n_intervals]} Pie Chart",
        )

        return fig


if __name__ == "__main__":
    app.run_server()