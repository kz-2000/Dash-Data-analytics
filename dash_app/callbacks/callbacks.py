from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from data.data_import import fetch_proposals_data, clean_data, fetch_requests_data, clean_request_data, fetch_area_data

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

        fig_histogram = create_histogram(proposal_data, area_data)
        fig_proposals = create_proposals_figure(proposal_data)
        fig_conversion = create_conversion_figure(proposal_data)
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

def empty_figures(n):
    return [go.Figure() for _ in range(n)]