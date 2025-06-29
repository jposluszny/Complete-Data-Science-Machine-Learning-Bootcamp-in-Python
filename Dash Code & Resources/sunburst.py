import base64
import io
from dash.exceptions import PreventUpdate
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px

import pandas as pd

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Upload(
            id="upload-data",
            children=html.Div(["Drag and Drop", html.A("Upload Data")]),
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
        dcc.Store(id="data-store", storage_type="local"),
        html.Div([dcc.Graph(id="treemap")]),
        html.Div([dcc.Graph(id="pie-chart")]),
    ]
)


@app.callback(Output("data-store", "data"), [Input("upload-data", "contents")])
def update_output(contents):
    df = pd.DataFrame()
    if contents is not None:
        _, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))

        return df.to_json()


@app.callback(Output("treemap", "figure"), [Input("data-store", "data")])
def treemap_graph(data):
    if data is None:
        raise PreventUpdate
    dff = pd.read_json(data)
    print(dff)

    fig = px.sunburst(
        dff,
        values="funded_amount",
        path=["region", "activity"],
        height=800,
        title="Sunburst",
    )

    return fig


@app.callback(Output("pie-chart", "figure"), [Input("data-store", "data")])
def pie_graph(data):
    if data is None:
        raise PreventUpdate
    dff = pd.read_json(data)
    fig = px.pie(
        dff, values="funded_amount", names="region", title="Funded Amount and Region"
    )

    return fig


if __name__ == "__main__":
    app.run_server()