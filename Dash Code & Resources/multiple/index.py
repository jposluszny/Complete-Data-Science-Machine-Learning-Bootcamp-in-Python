import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from layouts import layout_scatter, layout_home
import callbacks

app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/apps/home":
        return layout_home
    elif pathname == "/apps/scatter":
        return layout_scatter
    else:
        return "404"


if __name__ == "__main__":
    app.run_server()