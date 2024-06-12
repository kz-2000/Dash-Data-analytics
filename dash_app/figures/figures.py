import plotly.express as px
import plotly.graph_objects as go

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

def create_conversion_figure(proposal_data):
    conversion_rate_data = proposal_data.resample('D', on='updated_at').last().reset_index()

    fig_conversion = go.Figure()
    fig_conversion.add_trace(go.Scatter(x=conversion_rate_data['updated_at'], y=conversion_rate_data['total_conversion_rate'],
                                        mode='lines+markers', name='Conversion Rate'))
    fig_conversion.update_layout(
        title='Total Conversion Rate Over Time',
        xaxis_title='Date',
        yaxis_title='Conversion Rate',
        legend_title='Metric',
        yaxis=dict(tickformat='.0%'),
        font=dict(family='Poppins, sans-serif')
    )
    return fig_conversion

def create_pie_chart(data, column, title):
    status_counts = data[column].value_counts()
    fig_pie = go.Figure(data=[go.Pie(labels=status_counts.index, values=status_counts.values, hole=.3)])
    fig_pie.update_layout(title=title, font=dict(family='Poppins, sans-serif'))
    return fig_pie

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