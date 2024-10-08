import plotly.express as px
import plotly.graph_objects as go
from dash_app.data.data_processing import merge_names

# Creates Histogram displaying the amount of proposals per Area, divided per Status

def create_histogram(proposal_data, area_data):
    proposal_area_data = proposal_data.explode('areas')
    merged_data = proposal_area_data.merge(area_data, how='left', left_on='areas', right_on='id')
    grouped_data = merged_data.groupby(['name', 'status']).size().reset_index(name='count').sort_values(by='count', ascending=False)
    total_proposals = grouped_data.groupby('name')['count'].sum().reset_index(name='total_count')
    fig_histogram = px.bar(grouped_data, x='name', y='count', color='status', barmode='stack',
                           labels={'name': 'Area', 'count': 'Number of Proposals'},
                           title='Proposals per Area by Status')
    fig_histogram.update_layout(font=dict(family='Poppins, sans-serif'))

    for idx, row in total_proposals.iterrows():
        fig_histogram.add_annotation(
            x=row['name'], 
            y=row['total_count'], 
            text=str(row['total_count']),
            showarrow=False,
            yshift=10
        )

    return fig_histogram

# Creates a line graph displaying the total amount of cumulative proposals over time & a bar chart displaying the weekly amount of proposals that came in

def create_proposals_figure(proposal_data):
    proposal_data = proposal_data.sort_values('created_at')
    proposal_data['cumulative_total'] = range(1, len(proposal_data) + 1)
    proposal_data['cumulative_converted'] = proposal_data['status'].eq('CONFIRMED').cumsum()
    proposal_data['total_conversion_rate'] = (proposal_data['cumulative_converted'] / proposal_data['cumulative_total']).fillna(0)
    weekly_data = proposal_data.resample('W-Mon', on='created_at').size().reset_index(name='weekly_count')
    weekly_data['cumulative_count'] = weekly_data['weekly_count'].cumsum()

    fig_proposals = go.Figure()
    fig_proposals.add_trace(go.Bar(x=weekly_data['created_at'], y=weekly_data['weekly_count'], name='Weekly Count'))
    fig_proposals.add_trace(go.Scatter(x=weekly_data['created_at'], y=weekly_data['cumulative_count'], mode='lines', name='Cumulative Count'))
    fig_proposals.update_layout(title='Proposals Created Over Time',
                                xaxis_title='Date',
                                yaxis_title='Number of Proposals',
                                legend_title='Metric',
                                font=dict(family='Poppins, sans-serif'))
    return fig_proposals


# Creates Line graph displaying the conversion rate over time, using the created_at_itinerary

def create_conversion_figure(conversion_data):

    fig_conversion = go.Figure()
    fig_conversion.add_trace(go.Scatter(x=conversion_data['created_at_proposal'], y=conversion_data['total_conversion_rate'],
                                        mode='lines', name='Conversion Rate'))
    fig_conversion.update_layout(
        title='Total Conversion Rate Over Time',
        xaxis_title='Date',
        yaxis_title='Conversion Rate (%)',
        legend_title='Metric',
        yaxis=dict(tickformat='.2%'),
        font=dict(family='Poppins, sans-serif')
    )
    return fig_conversion


# Creates a pie chart displaying the requests/proposals by status

def create_pie_chart(data, column, title):
    status_counts = data[column].value_counts()
    fig_pie = go.Figure(data=[go.Pie(labels=status_counts.index, values=status_counts.values, hole=.3)])
    fig_pie.update_layout(title=title, font=dict(family='Poppins, sans-serif'))
    return fig_pie

# Creates a line graph displaying the cumulative count of requests over time & a bar chart with the weekly added requests

def create_requests_figure(request_data):
    request_data = request_data.sort_values('created_at')
    request_data['cumulative_count'] = request_data.index + 1
    weekly_data = request_data.resample('W-Mon', on='created_at').size().reset_index(name='weekly_count')
    weekly_data['cumulative_count'] = weekly_data['weekly_count'].cumsum()

    fig_requests = go.Figure()
    fig_requests.add_trace(go.Bar(x=weekly_data['created_at'], y=weekly_data['weekly_count'], name='Weekly Count'))
    fig_requests.add_trace(go.Scatter(x=weekly_data['created_at'], y=weekly_data['cumulative_count'], mode='lines', name='Cumulative Count'))
    fig_requests.update_layout(title='Requests Over Time',
                               xaxis_title='Date',
                               yaxis_title='Number of Requests',
                               legend_title='Metric',
                               font=dict(family='Poppins, sans-serif'))
    return fig_requests

# Creates a bar chart displaying the amount of services per supplier sold

def create_supplier_bar_chart(merged_data):
        # Group by supplier and count the number of services
    supplier_service_count = merged_data.groupby('name')['service_id'].count().reset_index()
    supplier_service_count.columns = ['Supplier', 'Number of Services']

    supplier_service_count = supplier_service_count[supplier_service_count['Supplier'] != 'sami daik tours']

# Sort the DataFrame by 'Number_of_Services' in descending order
    df_sorted = supplier_service_count.sort_values(by='Number of Services', ascending=False)
    df_top_20 = df_sorted.head(30)

    # Create the bar chart
    fig = px.bar(df_top_20, x='Supplier', y='Number of Services', title='Top 30 Number of Services Provided by Each Supplier')

    return fig 

# Creates a bar chart with the money spent per service

def create_service_price_bar_chart(merged_data):
    # Group by 'service_name' and calculate the total amount spent per service
    spending_per_service = merged_data.groupby('title')['price'].sum().reset_index()
    spending_per_service_sorted = spending_per_service.sort_values(by='price', ascending = False)

    spending_per_service_top30 = spending_per_service_sorted.head(40)

    # Create a bar chart using Plotly Express
    fig = px.bar(spending_per_service_top30, x='title', y='price', title='Top 40 Total Amount Spent per Service')

    # Customize the layout of the chart
    fig.update_layout(
        xaxis_title='Service',
        yaxis_title='Total Amount Spent',
        xaxis_tickangle=-45,
    )

    return fig

# Creates Histogram displaying the amount of proposals per Area, divided per Status

def create_user_conversion_chart(proposal_data, user_data):
    merged_data = proposal_data.merge(user_data, how='left', left_on='owner_id', right_on='id')
    merged_data = merge_names(merged_data, 'name')

    grouped_data = merged_data.groupby(['name', 'status']).size().reset_index(name='count').sort_values(by='count', ascending=False)
    total_proposals = grouped_data.groupby('name')['count'].sum().reset_index(name='total_count')
    fig_histogram = px.bar(grouped_data, x='name', y='count', color='status', barmode='stack',
                           labels={'status': 'status', 'count': 'Number of Proposals'},
                           title='Proposals per User per Status')
    fig_histogram.update_layout(font=dict(family='Poppins, sans-serif'))

    for idx, row in total_proposals.iterrows():
        fig_histogram.add_annotation(
            x=row['name'], 
            y=row['total_count'], 
            text=str(row['total_count']),
            showarrow=False,
            yshift=10
        )

    return fig_histogram