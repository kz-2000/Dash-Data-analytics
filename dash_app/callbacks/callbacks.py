from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from data.data_import import fetch_proposals_data, clean_data, fetch_requests_data, clean_request_data, fetch_area_data

def register_callbacks(app):
    @app.callback([Output('live-update-graph-proposals', 'figure'),
                   Output('live-update-graph-conversion', 'figure'),
                   Output('pie-chart-proposals-status', 'figure'),
                   Output('pie-chart-requests-status', 'figure'),
                   Output('histogram-confirmed-proposals-area', 'figure'),
                  Input('fetch-button', 'n_clicks')])
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
        proposal_area_data = proposal_data.explode('areas')

        # Merge proposals with area data to get area names
        merged_data = proposal_area_data.merge(area_data, how='left', left_on='areas', right_on='id')
       # print(f"Proposals data after merging with area data: {merged_data['name'].head()}")

        # Group by area and status
        grouped_data = merged_data.groupby(['name', 'status']).size().reset_index(name='count').sort_values(by='count', ascending=False)

        # Calculate total proposals per area
        total_proposals = grouped_data.groupby('name')['count'].sum().reset_index(name='total_count')

        # Create a grouped bar chart
        fig_histogram = px.bar(grouped_data, x='name', y='count', color='status', barmode='stack',
                               labels={'name': 'Area', 'count': 'Number of Proposals'},
                               title='Proposals per Area by Status')
        fig_histogram.update_layout(font=dict(family='Poppins, sans-serif'))

                # Add total proposals as text annotations
        for idx, row in total_proposals.iterrows():
            fig_histogram.add_annotation(
                x=row['name'], 
                y=row['total_count'], 
                text=str(row['total_count']),
                showarrow=False,
                yshift=10
            )


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
                                       name='Weekly Count'))

        # Add cumulative count line
        fig_proposals.add_trace(go.Scatter(x=weekly_data['created_at'], y=weekly_data['cumulative_count'],
                                           mode='lines', name='Cumulative Count'))

        # Update the layout
        fig_proposals.update_layout(title='Proposals Created Over Time',
                                    xaxis_title='Date',
                                    yaxis_title='Number of Proposals',
                                    legend_title='Metric',
                                    font=dict(family='Poppins, sans-serif'))
        
        # Resample to weekly for plotting conversion rate
        conversion_rate_data = proposal_data.resample('W-Mon', on='updated_at').last().reset_index()

        fig_conversion = go.Figure()

        # Add conversion rate line
        fig_conversion.add_trace(go.Scatter(x=conversion_rate_data['updated_at'], y=conversion_rate_data['total_conversion_rate'],
                                            mode='lines+markers', name='Conversion Rate'))

        # Update the layout
        fig_conversion.update_layout(
            title='Total Conversion Rate Over Time',
            xaxis_title='Date',
            yaxis_title='Conversion Rate',
            legend_title='Metric',
            yaxis=dict(tickformat='.0%'),
            font=dict(family='Poppins, sans-serif')
        )

        # Create pie chart for proposal status
        status_counts = proposal_data['status'].value_counts()
        fig_pie = go.Figure(data=[go.Pie(labels=status_counts.index, values=status_counts.values, hole=.3)])

        # Update the layout for the pie chart
        fig_pie.update_layout(title='Proposals by Status', font=dict(family='Poppins, sans-serif'))

        request_data = fetch_requests_data()

        request_status_counts = request_data['status'].value_counts()
        fig_pie_requests = go.Figure(data=[go.Pie(labels=request_status_counts.index, values=request_status_counts.values, hole=.3)])
        fig_pie_requests.update_layout(title='Requests by Status', font=dict(family='Poppins, sans-serif'))

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
                                        name='Weekly Count'))

        # Add cumulative count line
        fig_requests.add_trace(go.Scatter(x=weekly_data['created_at'], y=weekly_data['cumulative_count'],
                                            mode='lines', name='Cumulative Count'))

        # Update the layout
        fig_requests.update_layout(title='Requests Over Time',
                                    xaxis_title='Date',
                                    yaxis_title='Number of Requests',
                                    legend_title='Metric',
                                    font=dict(family='Poppins, sans-serif'))

        return fig_requests
