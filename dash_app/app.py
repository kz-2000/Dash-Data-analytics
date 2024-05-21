# app.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from data_import import fetch_proposals_data, clean_data, fetch_requests_data, clean_request_data, fetch_area_data # import functions
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    html.H1("ESSNTL ANALYTICS 📊"),
    
    # Button to fetch data
    html.Button('Fetch Data', id='fetch-button', n_clicks=0),
    
    # First chart for requests
    dcc.Graph(id='live-update-graph-requests'),

    # Pie charts for proposals and requests status
    html.Div([
        dcc.Graph(id='pie-chart-proposals-status', style={'display': 'inline-block', 'width': '49%'}),
        dcc.Graph(id='pie-chart-requests-status', style={'display': 'inline-block', 'width': '49%'}),
    ]),

    # Conversion chart for proposals
    dcc.Graph(id='live-update-graph-proposals'),

    # Second chart for requests
    dcc.Graph(id='live-update-graph-conversion'),

        # Chart for confirmed proposals per area
    dcc.Graph(id='histogram-confirmed-proposals-area')
])

@app.callback([Output('live-update-graph-proposals', 'figure'),
               Output('live-update-graph-conversion', 'figure'),
               Output('pie-chart-proposals-status', 'figure'),
               Output('pie-chart-requests-status', 'figure'),
               Output('histogram-confirmed-proposals-area', 'figure')],
              [Input('fetch-button', 'n_clicks')])
def update_graph_proposals(n_clicks):
    if n_clicks == 0:
        return go.Figure(), go.Figure(), go.Figure(), go.Figure(), go.Figure()

    print("Fetching Proposal data...")
    proposal_data = fetch_proposals_data()
    
    # Clean the data
    proposal_data = clean_data(proposal_data)

    # Fetching Area data
    print("Fetching Area data...")
    area_data = fetch_area_data()

    # Explode the 'areas' column to create a row for each area_id
    proposal_data = proposal_data.explode('areas')

    # Merge proposals with area data to get area names
    merged_data = proposal_data.merge(area_data, how='left', left_on='areas', right_on='id')
    print(f"Proposals data after merging with area data: {merged_data['name'].head()}")

    # Filter confirmed proposals
    confirmed_proposals = merged_data[merged_data['status'] == 'CONFIRMED']
    
    # Histogram for confirmed proposals per area
    area_counts = confirmed_proposals['name'].value_counts()
    fig_histogram = go.Figure(data=[go.Bar(x=area_counts.index, y=area_counts.values, marker_color='blue')])
    fig_histogram.update_layout(title='Confirmed Proposals per Area',xaxis_title='Area',yaxis_title='Number of Confirmed Proposals')


    # Sort data by created_at
    proposal_data = proposal_data.sort_values('created_at')
    
    # Calculate cumulative counts
    proposal_data['cumulative_total'] = range(1, len(proposal_data) + 1)
    proposal_data['cumulative_converted'] = proposal_data['status'].eq('CONFIRMED').cumsum()
    
    # Calculate total conversion rate
    proposal_data['total_conversion_rate'] = (proposal_data['cumulative_converted'] / proposal_data['cumulative_total']).fillna(0)
    
    # Resample data by week for counts
    weekly_data = proposal_data.resample('W-Mon', on='created_at').size().reset_index(name='weekly_count')
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
    conversion_rate_data = proposal_data.resample('W-Mon', on='created_at').last().reset_index()

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
    status_counts = proposal_data['status'].value_counts()
    fig_pie = go.Figure(data=[go.Pie(labels=status_counts.index, values=status_counts.values, hole=.3)])

    # Update the layout for the pie chart
    fig_pie.update_layout(title='Proposals by Status')

    request_data = fetch_requests_data()

    request_status_counts = request_data['status'].value_counts()
    fig_pie_requests = go.Figure(data=[go.Pie(labels=request_status_counts.index, values=request_status_counts.values, hole=.3)])
    fig_pie_requests.update_layout(title='Requests by Status')

    return fig_proposals, fig_conversion, fig_pie, fig_pie_requests, fig_histogram


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
