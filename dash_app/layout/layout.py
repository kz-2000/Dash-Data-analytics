import dash_bootstrap_components as dbc
from dash import dcc, html

def create_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col(html.Div([
                html.Img(src='/assets/logo.svg', className="logo")
            ], className="d-flex justify-content-center align-items-center"), width=12)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col(dbc.Button('Fetch Data', id='fetch-button', n_clicks=0, color='primary', className="mb-3"), width='auto')
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col(dcc.Graph(id='live-update-graph-proposals', config={'displayModeBar': True}), width=12)
        ], className="mb-4 rounded-row"),

        dbc.Row([
            dbc.Col(dcc.Graph(id='live-update-graph-conversion', config={'displayModeBar': True}), width=12)
        ], className="mb-4 rounded-row"),

        dbc.Row([
            dbc.Col(dcc.Graph(id='pie-chart-proposals-status', config={'displayModeBar': True}), width=6),
            dbc.Col(dcc.Graph(id='pie-chart-requests-status', config={'displayModeBar': True}), width=6),
        ], className="mb-4 rounded-row"),

        dbc.Row([
            dbc.Col(dcc.Graph(id='histogram-confirmed-proposals-area', config={'displayModeBar': True}), width=12)
        ], className="mb-4 rounded-row"),

        dbc.Row([
            dbc.Col(dcc.Graph(id='live-update-graph-requests', config={'displayModeBar': True}), width=12)
        ], className="mb-4 rounded-row")
    ], fluid=True)