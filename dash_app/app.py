# app.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from data_import import fetch_proposals_data, clean_data, fetch_requests_data, clean_request_data # import functions

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    html.H1("ESSNTL ANALYTICS 📊"),
    
    # Button to fetch data
    html.Button('Fetch Data', id='fetch-button', n_clicks=0),
    
    # First chart for proposals
    dcc.Graph(id='live-update-graph-proposals'),

    # Second chart for requests
    dcc.Graph(id='live-update-graph-requests')
])

@app.callback(Output('live-update-graph-proposals', 'figure'),
              Input('fetch-button', 'n_clicks'))
def update_graph_proposals(n_clicks):
    if n_clicks == 0:
        return go.Figure()

    print("Fetching Proposal data...")
    data = fetch_proposals_data()
    
    # Clean the data
    data = clean_data(data)
    
    # Create cumulative count
    data = data.sort_values('created_at')
    data['cumulative_count'] = data.index + 1
    
    # Resample data by week
    weekly_data = data.resample('W-Mon', on='created_at').size().reset_index(name='weekly_count')
    weekly_data['cumulative_count'] = weekly_data['weekly_count'].cumsum()

    fig = go.Figure()

    # Add weekly count bars
    fig.add_trace(go.Bar(x=weekly_data['created_at'], y=weekly_data['weekly_count'],
                         name='Weekly Count', marker_color='blue'))

    # Add cumulative count line
    fig.add_trace(go.Scatter(x=weekly_data['created_at'], y=weekly_data['cumulative_count'],
                             mode='lines', name='Cumulative Count', line=dict(color='red')))

    # Update the layout
    fig.update_layout(title='Proposals Created Over Time',
                      xaxis_title='Date',
                      yaxis_title='Number of Proposals',
                      legend_title='Metric')

    return fig


@app.callback(Output('live-update-graph-requests', 'figure'),
              Input('fetch-button', 'n_clicks'))
def update_graph_requests(n_clicks):
    if n_clicks == 0:
        # Initial empty figure
        return go.Figure()

    print("Fetching Request data...")
    data = fetch_requests_data()
    
    # Clean the data if necessary
    data = clean_request_data(data)  # Assuming you have a separate cleaning function for requests

    data = data[data['created_at'] >= '2024-01-01']

    # Create cumulative count
    data = data.sort_values('created_at')
    data['cumulative_count'] = data.index + 1
    
    # Resample data by week
    weekly_data = data.resample('W-Mon', on='created_at').size().reset_index(name='weekly_count')
    weekly_data['cumulative_count'] = weekly_data['weekly_count'].cumsum()

    fig = go.Figure()

    # Add weekly count bars
    fig.add_trace(go.Bar(x=weekly_data['created_at'], y=weekly_data['weekly_count'],
                         name='Weekly Count', marker_color='green'))

    # Add cumulative count line
    fig.add_trace(go.Scatter(x=weekly_data['created_at'], y=weekly_data['cumulative_count'],
                             mode='lines', name='Cumulative Count', line=dict(color='orange')))

    # Update the layout
    fig.update_layout(title='Requests Over Time',
                      xaxis_title='Date',
                      yaxis_title='Number of Requests',
                      legend_title='Metric')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
