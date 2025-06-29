import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html
import pandas as pd
import plotly.express as px
import json

app = dash.Dash(__name__)

df = pd.read_csv("kiva_el.csv")

sectors = df["sector"].unique()
customdata = ["sector", "region", "term_in_months", "year", "day"]

app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            id="sector-field",
                            options=[
                                {"label": sector, "value": sector} for sector in sectors
                            ],
                            value="Agriculture",
                        ),
                    ],
                    style={"width": "48%", "display": "inline-block"},
                )
            ]
        ),
        html.Div(
            [dcc.Graph(id="scatter-plot")],
            style={"width": "48%", "display": "inline-block"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Markdown(
                            """
        **Hover Data**
        """
                        ),
                        html.Pre(id="hover-data"),
                    ]
                ),
                html.Div(
                    [
                        dcc.Markdown(
                            """
        **Click  Data**
        """
                        ),
                        html.Pre(id="click-data"),
                    ]
                ),
                html.Div(
                    [
                        dcc.Markdown(
                            """
        **Seleted Data**
        """
                        ),
                        html.Pre(id="selected-data"),
                    ]
                ),
            ],
            style={"float": "right", "display": "inline-block", "width": "49%"},
        ),
    ]
)


@app.callback(Output("scatter-plot", "figure"), [Input("sector-field", "value")])
def scatter_plot(sector):
    dff = df[df["sector"] == sector]
    fig = px.scatter(dff, x="funded_amount", y="lender_count", custom_data=customdata)

    return fig


@app.callback(Output("hover-data", "children"), [Input("scatter-plot", "hoverData")])
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)


@app.callback(Output("click-data", "children"), [Input("scatter-plot", "clickData")])
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)


@app.callback(
    Output("selected-data", "children"), [Input("scatter-plot", "selectedData")]
)
def display_selected_data(selectedData):
    return json.dumps(selectedData, indent=2)


if __name__ == "__main__":
    app.run_server()