# job_callbacks.py - Modular callback functions for the Job Distribution tab
from dash import Output, Input
import plotly.express as px
import pandas as pd

def register_job_callbacks(app, df):
    """
    Registers all callbacks related to the Job Distribution tab
    by injecting the app instance and the global dataframe.
    """
    
    # 1. Experience Level Chart Callback
    @app.callback(
        Output('experience-level-chart', 'figure'),
        Input('tab-content', 'children')
    )
    def update_experience_chart(tab_children):
        exp_counts = df['Experience'].value_counts().reset_index()
        exp_counts.columns = ['experience', 'count']
        exp_counts = exp_counts.sort_values('count', ascending=False)
        
        fig = px.bar(
            exp_counts, x='experience', y='count', color='count',
            color_continuous_scale='Viridis', title='',
            labels={'count': 'Number of Jobs', 'experience': 'Experience Level'}
        )
        fig.update_layout(height=400, title_x=0.5, showlegend=False, xaxis={'tickangle': 45})
        fig.update_coloraxes(showscale=False)
        return fig

    # 2. Contract Type Chart Callback
    @app.callback(
        Output('contract-type-chart', 'figure'),
        Input('tab-content', 'children')
    )
    def update_contract_chart(tab_children):
        contract_counts = df['JobType'].value_counts().reset_index()
        contract_counts.columns = ['contract', 'count']
        
        total = contract_counts['count'].sum()
        contract_counts['percentage'] = (contract_counts['count'] / total) * 100
        main_categories = contract_counts[contract_counts['percentage'] >= 5].copy()
        under_5_sum = contract_counts[contract_counts['percentage'] < 5]['count'].sum()
        
        if under_5_sum > 0:
            other_row = pd.DataFrame({'contract': ['Other (under 5%)'], 'count': [under_5_sum], 'percentage': [(under_5_sum / total) * 100]})
            main_categories = pd.concat([main_categories, other_row], ignore_index=True)
            
        fig = px.pie(main_categories, values='count', names='contract', title='', hole=0.4)
        fig.update_layout(height=400, legend=dict(orientation='h', yanchor='bottom', y=-0.1, xanchor='center', x=0.5))
        fig.update_traces(textposition='inside', textinfo='percent+label')
        return fig

    # 3. Work Type Chart Callback
    @app.callback(
        Output('work-type-chart', 'figure'),
        Input('tab-content', 'children')
    )
    def update_work_type_chart_callback(tab_children):
        work_counts = df['WorkType'].value_counts().head(15).reset_index()
        work_counts.columns = ['work_type', 'count']
        work_counts = work_counts.sort_values('count', ascending=True)
        
        fig = px.bar(
            work_counts, x='count', y='work_type', orientation='h',
            color='count', color_continuous_scale='Teal', title='',
            labels={'count': 'Number of Jobs', 'work_type': 'Work Type'}
        )
        fig.update_layout(height=400, title_x=0.5, showlegend=False)
        fig.update_coloraxes(showscale=False)
        return fig

    # 4. Company Market Share Callback
    @app.callback(
        Output('company-market-share', 'figure'),
        Input('tab-content', 'children')
    )
    def update_company_market_share(tab_children):
        top_regions = df['region'].value_counts().head(5).index.tolist()
        top_companies = df['CompanyName'].value_counts().head(5).index.tolist()
        
        region_company = df[df['region'].isin(top_regions)].copy()
        region_company_top = region_company[region_company['CompanyName'].isin(top_companies)]
        
        region_totals = df[df['region'].isin(top_regions)].groupby('region').size().reset_index(name='total')
        region_top_counts = region_company_top.groupby('region').size().reset_index(name='top_count')
        
        region_stats = region_totals.merge(region_top_counts, on='region', how='left').fillna(0)
        region_stats['other_percentage'] = 100 - (region_stats['top_count'] / region_stats['total']) * 100
        region_stats['region_label'] = region_stats.apply(lambda x: f"{x['region']}<br>({x['other_percentage']:.0f}% Other)", axis=1)
        
        region_label_map = dict(zip(region_stats['region'], region_stats['region_label']))
        company_dist = region_company_top.groupby(['region', 'CompanyName']).size().reset_index(name='count')
        
        region_totals_top = company_dist.groupby('region')['count'].sum().reset_index(name='total')
        company_dist = company_dist.merge(region_totals_top, on='region')
        company_dist['percentage'] = (company_dist['count'] / company_dist['total']) * 100
        company_dist['region_label'] = company_dist['region'].map(region_label_map)
        
        fig = px.bar(
            company_dist, x='region_label', y='percentage', color='CompanyName', title='',
            labels={'region_label': 'Regions', 'percentage': 'Market Share (%)', 'CompanyName': 'Company'},
            category_orders={'CompanyName': top_companies}, color_discrete_sequence=px.colors.qualitative.Set3, text='percentage'
        )
        fig.update_layout(
            height=400, title_x=0.5, barmode='stack',
            legend=dict(orientation='v', yanchor='top', y=1.0, xanchor='left', x=1.02, title=''),
            margin=dict(r=120, t=50, l=10, b=80)
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='inside', insidetextanchor='middle')
        return fig