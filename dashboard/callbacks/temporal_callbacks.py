# temporal_callbacks.py - Modular callback functions for the Temporal Analysis tab
from dash import Output, Input
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def register_temporal_callbacks(app, df):
    """
    Registers all callbacks for the Temporal Analysis tab,
    including the weekly trend line chart, monthly contract types, and regional distribution.
    """
    
    # 1. Callback for Job Type Distribution by Month
    @app.callback(
        Output('trends-jobtype-stacked', 'figure'),
        [Input('trends-month-filter', 'value'),
         Input('trends-exp-filter', 'value')]
    )
    def update_trends_jobtype(selected_month, exp_level):
        filtered_df = df.copy()
        
        if exp_level and exp_level != 'all':
            filtered_df = filtered_df[filtered_df['Experience'] == exp_level]
        
        if selected_month and selected_month != 'all':
            filtered_df = filtered_df[filtered_df['YearMonth'] == selected_month]
        
        if filtered_df.empty:
            return go.Figure()
        
        jobtype_monthly = filtered_df.groupby(['YearMonth', 'JobType']).size().reset_index(name='count')
        months_order = sorted(filtered_df['YearMonth'].unique())
        
        fig = px.bar(
            jobtype_monthly, x='YearMonth', y='count', color='JobType', title='',
            labels={'YearMonth': '', 'count': 'Number of Jobs', 'JobType': 'Contract Type'},
            color_discrete_sequence=px.colors.qualitative.Set2,
            category_orders={'YearMonth': months_order}, barmode='stack'
        )
        
        fig.update_layout(
            height=350, title_x=0.5, xaxis_title="", yaxis_title="Number of Jobs",
            legend=dict(orientation='v', yanchor='top', y=1, xanchor='left', x=1.02, title='Contract Type'),
            margin=dict(r=120)
        )
        return fig

    # 2. Callback for Weekly Job Posting Trend
    @app.callback(
        Output('trends-line-chart', 'figure'),
        [Input('trends-month-filter', 'value'),
         Input('trends-exp-filter', 'value')]
    )
    def update_trends_line(selected_month, exp_level):
        filtered_df = df.copy()
        
        if exp_level and exp_level != 'all':
            filtered_df = filtered_df[filtered_df['Experience'] == exp_level]
        
        if selected_month and selected_month != 'all':
            filtered_df = filtered_df[filtered_df['YearMonth'] == selected_month]
        
        if filtered_df.empty:
            return go.Figure()
        
        weekly_trends = filtered_df.set_index('PublishedDate').resample('W').size().reset_index()
        weekly_trends.columns = ['Date', 'Jobs']
        
        fig = px.line(
            weekly_trends, x='Date', y='Jobs', title='',
            labels={'Date': 'Week', 'Jobs': 'Jobs'}, markers=True,
            color_discrete_sequence=['#1f77b4']
        )
        
        fig.update_layout(height=350, title_x=0.5, xaxis_title="Week", yaxis_title="Number of Jobs", hovermode='x unified')
        fig.update_traces(marker=dict(size=4), line=dict(width=2))
        return fig

    # 3. Callback for Region Distribution (All regions)
    @app.callback(
        Output('trends-region-chart', 'figure'),
        [Input('trends-month-filter', 'value'),
         Input('trends-exp-filter', 'value')]
    )
    def update_trends_region(selected_month, exp_level):
        filtered_df = df.copy()
        
        if exp_level and exp_level != 'all':
            filtered_df = filtered_df[filtered_df['Experience'] == exp_level]
        
        if selected_month and selected_month != 'all':
            filtered_df = filtered_df[filtered_df['YearMonth'] == selected_month]
        
        if filtered_df.empty:
            return go.Figure()
        
        region_counts = filtered_df['region'].value_counts().reset_index()
        region_counts.columns = ['region', 'count']
        region_counts = region_counts.sort_values('count', ascending=True)
        
        fig = px.bar(
            region_counts, x='count', y='region', orientation='h',
            color='count', color_continuous_scale='Teal', title='',
            labels={'count': 'Jobs', 'region': 'Region'}
        )
        
        fig.update_layout(height=350, title_x=0.5, xaxis_title="Number of Jobs", yaxis_title="Region", showlegend=False, margin=dict(l=180))
        fig.update_coloraxes(showscale=False)
        return fig