import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

df = pd.read_csv("kiva_el.csv")

fig = px.bar(df, x="sector", y="loan_amount")

fig.update_layout(plot_bgcolor="#ea4663", paper_bgcolor="#ea4663", font_color="#ffffff")

app.layout = html.Div(
    style={"backgroundColor": "#ea4663"},
    children=[
        html.H1(children="Data Science Application", style={"textAlign": "center"}),
        dcc.Graph(id="bar-plot", figure=fig),
    ],
)

if __name__ == "__main__":
    app.run_server()