import base64
import datetime
import io
import json
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.graph_objects as go

import pandas as pd

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Upload(
            id="upload-data",
            children=html.Div(["Drag and Drop or ", html.A("Upload Data")]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            multiple=False,
        ),
        html.Div(id="data-store", style={"display": "none"}),
        html.Div(
            id="table",
        ),
    ]
)


@app.callback(Output("data-store", "children"), [Input("upload-data", "contents")])
def update_output(contents):
    df = pd.DataFrame()
    if contents is not None:
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))

    return df.to_json()


@app.callback(
    Output("table", "children"),
    [
        Input("data-store", "children"),
    ],
)
def update_graph(jsonified_data):
    dff = pd.read_json(jsonified_data)
    fig = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in dff.columns],
        data=dff.to_dict("records"),
        filter_action="native",
        sort_action="native",
        page_current=0,
        page_size=15,
        editable=True,
        style_header={"backgroundColor": "#ea4663"},
        style_cell={"backgroundColor": "#1a9988", "color": "white"},
        export_format="csv",
    )

    return fig


if __name__ == "__main__":
    app.run_server()
