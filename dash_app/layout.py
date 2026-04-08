from dash import html, dcc

def get_layout():
    return html.Div([
        html.H1("Processed PDF Results"),
        html.Button("Load Latest OCR Result", id="load-btn"),
        html.Hr(),
        html.Pre(id="output-div", style={
            "whiteSpace": "pre-wrap",
            "background": "#f4f4f4",
            "padding": "15px",
            "maxHeight": "600px",
            "overflowY": "scroll"
        })
    ])
