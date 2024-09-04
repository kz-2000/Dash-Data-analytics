from dash.dependencies import Input, Output, State
from dash import dcc, callback_context
import plotly.express as px
import plotly.graph_objects as go
from dash_app.data.data_import import fetch_proposals_data, fetch_requests_data, fetch_area_data, fetch_supplier_data, fetch_proposal_service_data, fetch_service_data, fetch_proposal_history_data, fetch_travel_agent_data, fetch_profiles_data, fetch_itinerary_service_data, fetch_conversion_fig_data, fetch_area_hist_data, fetch_itinerary_data, fetch_prop_data_user_hist
from dash_app.figures.figures import create_histogram, create_conversion_figure, create_pie_chart, create_proposals_figure, create_requests_figure, create_supplier_bar_chart, create_service_price_bar_chart, create_user_conversion_chart
from dash_app.data.data_processing import calculate_conversion_rate, merge_tables, merge_names, pick_columns
import pandas as pd
import openpyxl

def register_callbacks(app):
    @app.callback(
        [
            Output('live-update-graph-proposals', 'figure'),
            Output('live-update-graph-conversion', 'figure'),
            Output('pie-chart-proposals-status', 'figure'),
           # Output('pie-chart-requests-status', 'figure'),
            Output('histogram-confirmed-proposals-area', 'figure')
        ],
        [Input('fetch-button', 'n_clicks')]
    )
    def update_graph_proposals(n_clicks):
        if n_clicks == 0:
            return empty_figures(4)

        proposal_data = fetch_proposals_data()
        itinerary_data = fetch_itinerary_data()
        area_data = fetch_area_data()
        conversion_fig_data = fetch_conversion_fig_data()
        proposal_data_hist = fetch_area_hist_data()

        # Calculate conversion rate only for the conversion figure
        conversion_data = calculate_conversion_rate(conversion_fig_data, itinerary_data)

        fig_histogram = create_histogram(proposal_data_hist, area_data)
        fig_proposals = create_proposals_figure(proposal_data)
        fig_conversion = create_conversion_figure(conversion_data)
        fig_pie = create_pie_chart(proposal_data, 'status', 'Proposals by Status')
     #   request_data = fetch_requests_data()
     #   fig_pie_requests = create_pie_chart(request_data, 'status', 'Requests by Status')

       # return fig_proposals, fig_conversion, fig_pie, fig_pie_requests, fig_histogram
        return fig_proposals, fig_conversion, fig_pie, fig_histogram

   # @app.callback(Output('live-update-graph-requests', 'figure'), [Input('fetch-button', 'n_clicks')])
   # def update_graph_requests(n_clicks):
   #     if n_clicks == 0:
   #         return empty_figures(1)[0]

   #     request_data = fetch_requests_data()
   #     request_data = request_data[request_data['created_at'] >= '2024-01-01']
   #     fig_requests = create_requests_figure(request_data)

   #     return fig_requests

    @app.callback(Output('supplier-bar-chart', 'figure'), [Input('fetch-button', 'n_clicks')])
    def update_supplier_barchart(n_clicks):
        if n_clicks == 0:
            return empty_figures(1)[0]

        supplier_data = fetch_supplier_data()
        itinerary_service_data = fetch_itinerary_service_data()
        merged_data = merge_tables(itinerary_service_data, supplier_data, 'supplier_id', 'id')
        fig_suppliers = create_supplier_bar_chart(merged_data)

        return fig_suppliers

    @app.callback(Output('service-spending-bar-chart', 'figure'), [Input('fetch-button', 'n_clicks')])
    def update_service_spending_barchart(n_clicks):
        if n_clicks == 0:
            return empty_figures(1)[0]

        itinerary_service_data = fetch_itinerary_service_data()
        service_data = fetch_service_data()

        # Filter the data to include only 'CONFIRMED' or 'COMPLETED' statuses
     #   itinerary_service_data = itinerary_service_data[itinerary_service_data['status'].isin(['CONFIRMED', 'COMPLETED'])]
        merged_data = merge_tables(service_data, itinerary_service_data, 'id', 'service_id')

        # Filter out rows where 'supplier_id' is missing
        merged_data = merged_data[merged_data['supplier_id'].notna()]
        
        # Filter out rows where 'amount' is 0
        merged_data = merged_data[merged_data['price'] != 0]

        # Divide the 'amount' column by 100
        merged_data['price'] = merged_data['price'] / 100


        fig_service_spending = create_service_price_bar_chart(merged_data)

        return fig_service_spending

    # Report download callback

    @app.callback(
        Output("download-report", "data"),
        Input("download-report-button", "n_clicks"),
        [Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date')],
        prevent_initial_call=True
    )

    def download_sales_report(n_clicks, start_date, end_date):

        # Check which input triggered the callback
        ctx = callback_context
        if not ctx.triggered:
            return None
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id != 'download-report-button':
            return None

        print('this fuction is being called')
        proposal_data = fetch_proposals_data()
        request_data = fetch_requests_data()
        travel_agent_data = fetch_travel_agent_data()
        profile_data = fetch_profiles_data()
        proposal_history_data = fetch_proposal_history_data()


        merged_proposal_history = merge_tables(proposal_data, proposal_history_data, 'id', 'proposal_id')
        merged_proposal_history = pick_columns(merged_proposal_history, 'title_x','request_id_x','status_x','owner_id_x','created_at_y','version_y','proposal_id')
        exclude_ids = [
            'cf5e54ff-f7b6-4ac9-b26c-b1a53a6ff421',
            '356ed23b-ea02-41b0-98ab-89ba686e1ab2',
            'dc424d6e-dd04-4850-be63-19b4f557ffdc'
        ]
        merged_proposal_history = merged_proposal_history[~merged_proposal_history['owner_id_x'].isin(exclude_ids)]
        merged_request = merge_tables(merged_proposal_history, request_data, 'request_id_x', 'id')
        merged_profiles = merge_tables(merged_request, profile_data, 'owner_id_x', 'id')
        merged_profiles = merge_names(merged_profiles, 'owner')
        merged_profiles = pick_columns(merged_profiles, 'title_x','request_id_x','status_x','created_at_y','version_y','owner','travel_agent','proposal_id_x')
        merged_travel_agent = merge_tables(merged_profiles, travel_agent_data, 'travel_agent', 'id')

        sorted_data = merged_travel_agent.sort_values(by='version_y', ascending=False)
        sent_df = sorted_data[sorted_data['status_x']=='SENT']
        no_dups_df = sent_df.drop_duplicates(subset='proposal_id_x', keep='first')

        copy_df = no_dups_df.copy()
        copy_df['created_at_y'] = pd.to_datetime(copy_df['created_at_y']).dt.tz_localize(None)

         # Filter by date range
        if start_date is not None and end_date is not None:
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)
            copy_df = copy_df[(copy_df['created_at_y'] >= start_date) & (copy_df['created_at_y'] <= end_date)]

        copy_df['created_at_y'] = copy_df['created_at_y'].dt.strftime('%Y-%m-%d %H:%M-%S')
        final_df = copy_df.sort_values(by='created_at_y', ascending=False)

        final_df['first_name'] = final_df['first_name'].fillna('')
        final_df['last_name'] = final_df['last_name'].fillna('')

        final_df = merge_names(final_df, 'travel_agent')
        final_df['travel_agent'] = final_df['travel_agent'].str.strip()

        final_df = final_df[~final_df['title_x'].str.contains('sample|test|ivo|nadine', case=False)]


        final_df = pick_columns(final_df, 'title_x','created_at_y','version_y','owner','travel_agent','agency','email')
        
        new_column_names = {
        'title_x': 'Title',
        'created_at_y': 'Sent At',
        'version_y': 'Version',
        'owner': 'Owner',
        'travel_agent': 'Travel Agent',
        'agency':'Agency',
        'email':'Email'
        }


        final_df = final_df.rename(columns=new_column_names)

        return dcc.send_data_frame(final_df.to_excel, "sales_report.xlsx", sheet_name="Sales_report", index=False)

    @app.callback(Output('user_conversion_chart', 'figure'), [Input('fetch-button', 'n_clicks')])

    def update_user_conversion_chart(n_clicks):
        if n_clicks == 0:
            return empty_figures(1)[0]

        proposal_data = fetch_prop_data_user_hist()
        user_data = fetch_profiles_data()

        user_conversion_chart = create_user_conversion_chart(proposal_data, user_data)
        
        return user_conversion_chart


def empty_figures(n):
    return [go.Figure() for _ in range(n)]