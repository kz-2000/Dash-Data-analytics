import dash_bootstrap_components as dbc
from dash import dcc, html

def create_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col(html.Div([
                html.Img(src='/assets/logo.svg', className="logo")
            ], className="d-flex justify-content-center align-items-center"), width=12)
        ], className="mb-4"),


# Download Report button + Date Picker
        dbc.Row([
            dbc.Col(dcc.DatePickerRange(
            id='date-picker-range',
            start_date_placeholder_text='Start Date',
            end_date_placeholder_text='End Date'
        ), width='auto'),
            dbc.Col(dbc.Button('Download Report', id='download-report-button', n_clicks=0, color='primary', className="mb-3"), width='auto')
        ], className="mb-4"), dcc.Download(id='download-report'),

# Fetch data button
        dbc.Row([
            dbc.Col(dbc.Button('Fetch Data', id='fetch-button', n_clicks=0, color='primary', className="mb-3"), width='auto')
        ], className="mb-4"),

# Supplier Bar chart
        dbc.Row([
            dbc.Col(dcc.Graph(id='supplier-bar-chart', config={'displayModeBar': True}), width=12)
        ], className="mb-4 rounded-row"),

# Service Spending Bar Chart
        dbc.Row([
            dbc.Col(dcc.Graph(id='service-spending-bar-chart', config={'displayModeBar': True}), width=12)
        ], className="mb-4 rounded-row"),
        
# Proposals over time and weekly 
        dbc.Row([
            dbc.Col(dcc.Graph(id='live-update-graph-proposals', config={'displayModeBar': True}), width=12)
        ], className="mb-4 rounded-row"),

# Conversion graph 
        dbc.Row([
            dbc.Col(dcc.Graph(id='live-update-graph-conversion', config={'displayModeBar': True}), width=12)
        ], className="mb-4 rounded-row"),

# Pie charts Proposals & Requests by status
        dbc.Row([
            dbc.Col(dcc.Graph(id='pie-chart-proposals-status', config={'displayModeBar': True}), width=6),
            dbc.Col(dcc.Graph(id='pie-chart-requests-status', config={'displayModeBar': True}), width=6),
        ], className="mb-4 rounded-row"),

# Histogram for proposals per status per area
        dbc.Row([
            dbc.Col(dcc.Graph(id='histogram-confirmed-proposals-area', config={'displayModeBar': True}), width=12)
        ], className="mb-4 rounded-row"),

# Request cumulative over time and weekly
        dbc.Row([
            dbc.Col(dcc.Graph(id='live-update-graph-requests', config={'displayModeBar': True}), width=12)
        ], className="mb-4 rounded-row"),

    ], fluid=True)