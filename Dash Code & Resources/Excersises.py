import base64
import io
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input, dash_table, no_update, State

app = Dash(__name__, external_stylesheets=['style.css'], title='Storage app')

app.layout = html.Div([
    html.H3(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.Upload(
        id='upload',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),
    # Tutaj umieszczamy tabelę, która zawsze istnieje w layoucie
    
    html.Div(id='hidden_data'),
    html.Div(id='table_container')
   
])

# Callback do wczytywania pliku i aktualizowania DANYCH i KOLUMN tabeli
@callback(
    Output('hidden_data', 'children'),
    Input('upload', 'contents'),
)
def update_table_on_upload(contents):
    if contents is None:
        return no_update # Nic nie aktualizuj, jeśli brak zawartości

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
    return df.to_json(date_format='iso', orient='split')

# Callback do reagowania na zmiany w edytowalnej tabeli
@callback(
    Output('table_container', 'children'), # Wyjście do nowego diva na komunikaty
    Input('hidden_data', 'children') # Teraz 'table' zawsze istnieje w layoucie
)
def display_output_on_edit(rows):

    return rows

if __name__ == '__main__':
    app.run(debug=True)