from datetime import datetime as dt
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.express as px

df = pd.read_csv("kiva_el.csv")

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.DatePickerSingle(
            id="my-date-picker",
            min_date_allowed=dt(2014, 1, 1),
            max_date_allowed=dt(2018, 1, 1),
            date=str(dt(2014, 2, 17)),
        ),
        html.Div([dcc.Graph(id="chart")]),
    ]
)


@app.callback(Output("chart", "figure"), [Input("my-date-picker", "date")])
def chart(picked_date):
    if picked_date is not None:
        picked_date = dt.strptime(picked_date[0:10], "%Y-%m-%d").date()
        dff = df[df["date"] == str(picked_date)]
        fig = px.scatter(dff, x="funded_amount", y="lender_count")
        return fig


if __name__ == "__main__":
    app.run_server()