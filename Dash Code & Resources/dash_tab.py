import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px

df = pd.read_csv("kiva_el.csv")

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Tabs(
            id="tabs",
            children=[
                dcc.Tab(label="Scatter Plot", value="tab-1"),
                dcc.Tab(label="Pie Chart", value="tab-2"),
                dcc.Tab(label="Bar Chart", value="tab-3"),
            ],
        ),
        html.Div(id="tabs-content"),
    ]
)

scatter = px.scatter(
    df,
    x="funded_amount",
    color="day",
    y="lender_count",
    title="Funded Amount and Lender Count Scatterplot",
)

pie = px.pie(df, values="funded_amount", names="day", title="Funded Amount vs Day")
bar = px.bar(df, x="activity", y="term_in_months", title="Activity and Term in Months")


@app.callback(Output("tabs-content", "children"), [Input("tabs", "value")])
def render_content(tab):
    if tab == "tab-1":
        return html.Div([dcc.Graph(figure=scatter)])
    elif tab == "tab-2":
        return html.Div([dcc.Graph(figure=pie)])
    elif tab == "tab-3":
        return html.Div([dcc.Graph(figure=bar)])


if __name__ == "__main__":
    app.run_server()