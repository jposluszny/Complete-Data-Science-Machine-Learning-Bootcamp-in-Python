from datetime import datetime as dt
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.express as px

df = pd.read_csv("kiva_el.csv")
df['date'] = pd.to_datetime(df['date'])

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.DatePickerRange(
            id="my-date-picker",
            min_date_allowed=dt(2014, 1, 1),
            max_date_allowed=dt(2018, 1, 1),
            start_date=dt(2014, 2, 17),
            end_date=dt(2018, 2, 17),
        ),
        html.Div([dcc.Graph(id="chart")]),
    ]
)


@app.callback(
    Output("chart", "figure"),
    [Input("my-date-picker", "start_date"), Input("my-date-picker", "end_date")],
)
def chart(start_date, end_date):
    if (start_date is not None) & (end_date is not None):
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        dff = df[df["date"].isin(pd.date_range(start_date, end_date))]
        fig = px.scatter(dff, x="funded_amount", y="lender_count")
        return fig


if __name__ == "__main__":
    app.run_server()