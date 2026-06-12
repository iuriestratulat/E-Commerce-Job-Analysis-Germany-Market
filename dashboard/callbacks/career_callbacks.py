# career_callbacks.py - Modular callback functions for the Career Progression tab
from dash import Output, Input
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def register_career_callbacks(app, df):
    """
    Registers all callbacks for the Career Progression tab,
    handling contract types, work types, sunburst decomposition, and Sankey flow.
    """
    
    # 1. Callback for Contract Types by Experience Level
    @app.callback(
        Output('career-contract-chart', 'figure'),
        Input('career-exp-filter', 'value')
    )
    def update_career_contract_chart(exp_level):
        filtered_df = df.copy()
        if exp_level and exp_level != 'all':
            filtered_df = filtered_df[filtered_df['Experience'] == exp_level]
        
        if filtered_df.empty:
            return go.Figure()
        
        contract_exp = filtered_df.groupby(['Experience', 'JobType']).size().reset_index(name='count')
        
        exp_order = ['Entry level', 'Associate', 'Mid-Senior level', 'Director', 'Executive', 'Internship', 'Not Required']
        exp_order = [e for e in exp_order if e in contract_exp['Experience'].unique()]
        
        fig = px.bar(
            contract_exp, x='Experience', y='count', color='JobType', title='',
            labels={'count': 'Jobs', 'Experience': 'Experience', 'JobType': 'Contract'},
            color_discrete_sequence=px.colors.qualitative.Set2,
            category_orders={'Experience': exp_order}, barmode='stack'
        )
        fig.update_layout(
            height=400, xaxis={'tickangle': 45},
            legend=dict(orientation='v', yanchor='top', y=1, xanchor='left', x=1.02, title='Contract Type'),
            margin=dict(r=150)
        )
        return fig

    # 2. Callback for Work Types by Experience Level
    @app.callback(
        Output('career-worktype-stacked', 'figure'),
        Input('career-exp-filter', 'value')
    )
    def update_career_worktype_stacked(exp_level):
        filtered_df = df.copy()
        if exp_level and exp_level != 'all':
            filtered_df = filtered_df[filtered_df['Experience'] == exp_level]
        
        if filtered_df.empty:
            return go.Figure()
        
        worktype_exp = filtered_df.groupby(['WorkType', 'Experience']).size().reset_index(name='count')
        worktype_totals = worktype_exp.groupby('WorkType')['count'].sum().sort_values(ascending=False)
        sorted_worktypes = worktype_totals.index.tolist()
        
        top_worktypes = sorted_worktypes[:10]
        worktype_exp = worktype_exp[worktype_exp['WorkType'].isin(top_worktypes)]
        
        exp_order = ['Entry level', 'Associate', 'Mid-Senior level', 'Director', 'Executive', 'Internship']
        exp_order = [e for e in exp_order if e in worktype_exp['Experience'].unique()]
        
        fig = px.bar(
            worktype_exp, x='count', y='WorkType', color='Experience', orientation='h', title='',
            labels={'count': 'Jobs', 'WorkType': 'Work Type', 'Experience': 'Experience'},
            color_discrete_sequence=px.colors.qualitative.Set3,
            category_orders={'WorkType': sorted_worktypes, 'Experience': exp_order}, barmode='stack'
        )
        fig.update_layout(
            height=400, margin=dict(l=180), 
            legend=dict(orientation='h', yanchor='bottom', y=-0.15, xanchor='center', x=0.5)
        )
        return fig

    # 3. Callback for Decomposition Tree (Sunburst)
    @app.callback(
        Output('career-sunburst', 'figure'),
        Input('career-exp-filter', 'value')
    )
    def update_sunburst(exp_level):
        filtered_df = df.copy()
        if exp_level and exp_level != 'all':
            filtered_df = filtered_df[filtered_df['Experience'] == exp_level]
        
        if filtered_df.empty:
            return go.Figure()
        
        df_sunburst = filtered_df.groupby(['Experience', 'WorkType', 'JobType']).size().reset_index(name='count')
        top_experiences = filtered_df['Experience'].value_counts().head(5).index.tolist()
        df_sunburst = df_sunburst[df_sunburst['Experience'].isin(top_experiences)]
        
        fig = px.sunburst(
            df_sunburst, path=['Experience', 'WorkType', 'JobType'], values='count',
            title='', color='count', color_continuous_scale='Viridis',
            hover_data={'count': ':,.0f'}, labels={'count': 'Jobs'}
        )
        
        fig.update_coloraxes(colorbar_title_text="Jobs")
        fig.update_layout(height=400, margin=dict(t=0, l=0, r=0, b=0))
        return fig

    # 4. Callback for Sankey Diagram (Flow)
    @app.callback(
        Output('career-sankey', 'figure'),
        Input('career-exp-filter', 'value')
    )
    def update_sankey(exp_level):
        filtered_df = df.copy()
        if exp_level and exp_level != 'all':
            filtered_df = filtered_df[filtered_df['Experience'] == exp_level]
        
        if filtered_df.empty:
            return go.Figure()
        
        exp_region = filtered_df.groupby(['Experience', 'region']).size().reset_index(name='count')
        region_city = filtered_df.groupby(['region', 'city']).size().reset_index(name='count')
        
        top_exp = filtered_df['Experience'].value_counts().head(6).index.tolist()
        top_regions = filtered_df['region'].value_counts().head(5).index.tolist()
        
        exp_region = exp_region[exp_region['Experience'].isin(top_exp) & exp_region['region'].isin(top_regions)]
        region_city = region_city[region_city['region'].isin(top_regions)]
        
        region_city = region_city.sort_values('count', ascending=False)
        region_city = region_city.groupby('region').head(5).reset_index(drop=True)
        
        exp_nodes = list(exp_region['Experience'].unique())
        region_nodes = list(exp_region['region'].unique())
        city_nodes = list(region_city['city'].unique())
        
        all_nodes = exp_nodes + region_nodes + city_nodes
        node_index = {node: i for i, node in enumerate(all_nodes)}
        
        sources, targets, values = [], [], []
        
        for _, row in exp_region.iterrows():
            sources.append(node_index[row['Experience']])
            targets.append(node_index[row['region']])
            values.append(int(row['count']))
        
        for _, row in region_city.iterrows():
            if row['region'] in node_index and row['city'] in node_index:
                sources.append(node_index[row['region']])
                targets.append(node_index[row['city']])
                values.append(int(row['count']))
        
        node_colors = (['#1f77b4'] * len(exp_nodes) + ['#ff7f0e'] * len(region_nodes) + ['#2ca02c'] * len(city_nodes))
        
        fig = go.Figure(data=[go.Sankey(
            node=dict(pad=15, thickness=15, line=dict(color="black", width=0.5), label=all_nodes, color=node_colors),
            link=dict(source=sources, target=targets, value=values, color='rgba(100, 100, 200, 0.2)')
        )])
        
        num_regions = len(region_nodes)
        num_cities = len(city_nodes)
        
        fig.update_layout(
            title=dict(text=f"🌊 Experience → Region → City Flow (Top {num_regions} Regions, Top {num_cities} Cities)", x=0.5, font=dict(size=12)),
            height=450, font=dict(size=9), margin=dict(t=40, l=20, r=20, b=20)
        )
        return fig