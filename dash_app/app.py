# app.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from data_import import fetch_proposals_data, clean_data, fetch_requests_data, clean_request_data # import functions
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    html.H1("ESSNTL ANALYTICS 📊"),
    
    # Button to fetch data
    html.Button('Fetch Data', id='fetch-button', n_clicks=0),
    
    # First chart for requests
    dcc.Graph(id='live-update-graph-requests'),

    # Chart for proposals by status
    dcc.Graph(id='pie-chart-status'),

    # Conversion chart for proposals
    dcc.Graph(id='live-update-graph-proposals'),

    # Second chart for requests
    dcc.Graph(id='live-update-graph-conversion')
])

@app.callback([Output('live-update-graph-proposals', 'figure'),
               Output('live-update-graph-conversion', 'figure'),
               Output('pie-chart-status', 'figure')],
              [Input('fetch-button', 'n_clicks')])
def update_graph_proposals(n_clicks):
    if n_clicks == 0:
        return go.Figure(), go.Figure(), go.Figure()

    print("Fetching Proposal data...")
    data = fetch_proposals_data()
    
    # Clean the data
    data = clean_data(data)
    
    # Sort data by created_at
    data = data.sort_values('created_at')
    
    # Calculate cumulative counts
    data['cumulative_total'] = range(1, len(data) + 1)
    data['cumulative_converted'] = data['status'].eq('CONFIRMED').cumsum()
    
    # Calculate total conversion rate
    data['total_conversion_rate'] = (data['cumulative_converted'] / data['cumulative_total']).fillna(0)
    
    # Resample data by week for counts
    weekly_data = data.resample('W-Mon', on='created_at').size().reset_index(name='weekly_count')
    weekly_data['cumulative_count'] = weekly_data['weekly_count'].cumsum()

    fig_proposals = go.Figure()

    # Add weekly count bars
    fig_proposals.add_trace(go.Bar(x=weekly_data['created_at'], y=weekly_data['weekly_count'],
                                   name='Weekly Count', marker_color='blue'))

    # Add cumulative count line
    fig_proposals.add_trace(go.Scatter(x=weekly_data['created_at'], y=weekly_data['cumulative_count'],
                                       mode='lines', name='Cumulative Count', line=dict(color='red')))

    # Update the layout
    fig_proposals.update_layout(title='Proposals Created Over Time',
                                xaxis_title='Date',
                                yaxis_title='Number of Proposals',
                                legend_title='Metric')
    
    # Resample to weekly for plotting conversion rate
    conversion_rate_data = data.resample('W-Mon', on='created_at').last().reset_index()

    fig_conversion = go.Figure()

    # Add conversion rate line
    fig_conversion.add_trace(go.Scatter(x=conversion_rate_data['created_at'], y=conversion_rate_data['total_conversion_rate'],
                                        mode='lines+markers', name='Conversion Rate', line=dict(color='purple')))

    # Update the layout
    fig_conversion.update_layout(
        title='Total Conversion Rate Over Time',
        xaxis_title='Date',
        yaxis_title='Conversion Rate',
        legend_title='Metric',
        yaxis=dict(tickformat='.0%')
    )

        # Create pie chart for proposal status
    status_counts = data['status'].value_counts()
    fig_pie = go.Figure(data=[go.Pie(labels=status_counts.index, values=status_counts.values, hole=.3)])

    # Update the layout for the pie chart
    fig_pie.update_layout(title='Proposals by Status')

    return fig_proposals, fig_conversion, fig_pie


@app.callback(Output('live-update-graph-requests', 'figure'),
              [Input('fetch-button', 'n_clicks')])
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

    fig_requests = go.Figure()

    # Add weekly count bars
    fig_requests.add_trace(go.Bar(x=weekly_data['created_at'], y=weekly_data['weekly_count'],
                                  name='Weekly Count', marker_color='green'))

    # Add cumulative count line
    fig_requests.add_trace(go.Scatter(x=weekly_data['created_at'], y=weekly_data['cumulative_count'],
                                      mode='lines', name='Cumulative Count', line=dict(color='orange')))

    # Update the layout
    fig_requests.update_layout(title='Requests Over Time',
                               xaxis_title='Date',
                               yaxis_title='Number of Requests',
                               legend_title='Metric')

    return fig_requests




if __name__ == '__main__':
    app.run_server(debug=True)
