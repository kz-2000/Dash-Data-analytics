from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from data.data_import import fetch_proposals_data, clean_data, fetch_requests_data, clean_request_data, fetch_area_data, fetch_supplier_data, fetch_proposal_service_data, fetch_service_data
from figures.figures import create_histogram, create_conversion_figure, create_pie_chart, create_proposals_figure, create_requests_figure, create_supplier_bar_chart, create_service_price_bar_chart
from data.data_processing import calculate_conversion_rate, merge_tables
import pandas as pd

def register_callbacks(app):
    @app.callback(
        [
            Output('live-update-graph-proposals', 'figure'),
            Output('live-update-graph-conversion', 'figure'),
            Output('pie-chart-proposals-status', 'figure'),
            Output('pie-chart-requests-status', 'figure'),
            Output('histogram-confirmed-proposals-area', 'figure')
        ],
        [Input('fetch-button', 'n_clicks')]
    )
    def update_graph_proposals(n_clicks):
        if n_clicks == 0:
            return empty_figures(5)

        proposal_data = fetch_proposals_data()
        proposal_data = clean_data(proposal_data)
        area_data = fetch_area_data()

        # Calculate conversion rate only for the conversion figure
        conversion_data = calculate_conversion_rate(proposal_data.copy(deep=True))

        fig_histogram = create_histogram(proposal_data, area_data)
        fig_proposals = create_proposals_figure(proposal_data)
        fig_conversion = create_conversion_figure(conversion_data)
        fig_pie = create_pie_chart(proposal_data, 'status', 'Proposals by Status')
        request_data = fetch_requests_data()
        request_data = clean_request_data(request_data)
        fig_pie_requests = create_pie_chart(request_data, 'status', 'Requests by Status')

        return fig_proposals, fig_conversion, fig_pie, fig_pie_requests, fig_histogram

    @app.callback(Output('live-update-graph-requests', 'figure'), [Input('fetch-button', 'n_clicks')])
    def update_graph_requests(n_clicks):
        if n_clicks == 0:
            return empty_figures(1)[0]

        request_data = fetch_requests_data()
        request_data = clean_request_data(request_data)
        request_data = request_data[request_data['created_at'] >= '2024-01-01']
        fig_requests = create_requests_figure(request_data)

        return fig_requests

    @app.callback(Output('supplier-bar-chart', 'figure'), [Input('fetch-button', 'n_clicks')])
    def update_supplier_barchart(n_clicks):
        if n_clicks == 0:
            return empty_figures(1)[0]

        supplier_data = fetch_supplier_data()
        proposal_service_data = fetch_proposal_service_data()
        merged_data = merge_tables(proposal_service_data, supplier_data, 'supplier_id', 'id')
        fig_suppliers = create_supplier_bar_chart(merged_data)

        return fig_suppliers

    @app.callback(Output('service-spending-bar-chart', 'figure'), [Input('fetch-button', 'n_clicks')])
    def update_service_spending_barchart(n_clicks):
        if n_clicks == 0:
            return empty_figures(1)[0]

        proposal_service_data = fetch_proposal_service_data()
        service_data = fetch_service_data()

        # Filter the data to include only 'CONFIRMED' or 'COMPLETED' statuses
        proposal_service_data = proposal_service_data[proposal_service_data['status'].isin(['CONFIRMED', 'COMPLETED'])]
        merged_data = merge_tables(service_data, proposal_service_data, 'id', 'service_id')

        # Filter out rows where 'supplier_id' is missing
        merged_data = merged_data[merged_data['supplier_id'].notna()]
        
        # Filter out rows where 'amount' is 0
        merged_data = merged_data[merged_data['price'] != 0]

        # Divide the 'amount' column by 100
        merged_data['price'] = merged_data['price'] / 100


        fig_service_spending = create_service_price_bar_chart(merged_data)

        return fig_service_spending


def empty_figures(n):
    return [go.Figure() for _ in range(n)]