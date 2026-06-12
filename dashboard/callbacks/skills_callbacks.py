# skills_callbacks.py - Modular callback functions for the Skills Analysis tab
from dash import Output, Input
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def register_skills_callbacks(app, df):
    """
    Registers all callbacks related to the Skills Analysis tab,
    including the top skills bar chart, the treemap, and the regional heatmap.
    """
    
    # 1. Callback for Top 15 Skills Bar Chart
    @app.callback(
        [Output('skills-bar-chart', 'figure'),
         Output('skills-bar-title', 'children')],
        Input('skills-exp-filter', 'value')
    )
    def update_skills_bar(exp_level):
        filtered_df = df.copy()
        
        if exp_level and exp_level != 'all':
            filtered_df = filtered_df[filtered_df['Experience'] == exp_level]
        
        # Extract skills safely
        all_skills = []
        for skills_list in filtered_df['Skills'].dropna():
            if isinstance(skills_list, list):
                all_skills.extend(skills_list)
        
        skill_counts = pd.Series(all_skills).value_counts().head(15).reset_index()
        skill_counts.columns = ['skill', 'count']
        skill_counts = skill_counts.sort_values('count', ascending=True)
        
        num_skills = len(skill_counts)
        title_text = f"📊 Top {num_skills} Skills" if num_skills > 0 else "📊 No Skills Found"
        
        fig = px.bar(
            skill_counts, x='count', y='skill', orientation='h',
            color='count', color_continuous_scale='Viridis', title='',
            labels={'count': 'Jobs', 'skill': 'Skills'}
        )
        
        fig.update_layout(
            height=400, title_x=0.5, xaxis_title="Number of Jobs",
            yaxis_title="Skills", showlegend=False
        )
        fig.update_coloraxes(showscale=False)
        
        return fig, title_text

    # 2. Callback for Skills Treemap
    @app.callback(
        Output('word-cloud-plot', 'figure'),
        Input('skills-exp-filter', 'value')
    )
    def update_treemap(exp_level):
        filtered_df = df.copy()
        
        if exp_level and exp_level != 'all':
            filtered_df = filtered_df[filtered_df['Experience'] == exp_level]
        
        all_skills = []
        for skills_list in filtered_df['Skills'].dropna():
            if isinstance(skills_list, list):
                all_skills.extend(skills_list)
        
        skill_counts = pd.Series(all_skills).value_counts().head(30).reset_index()
        skill_counts.columns = ['skill', 'count']
        
        if skill_counts.empty:
            return go.Figure()
        
        fig = px.treemap(
            skill_counts, path=['skill'], values='count',
            color='count', color_continuous_scale='Viridis', title='',
            labels={'count': 'Jobs', 'skill': 'Skills'}
        )
        
        fig.update_layout(height=400, title_x=0.5, margin=dict(t=0, l=0, r=0, b=0))
        fig.update_traces(
            textinfo='label+value', textposition='middle center',
            textfont=dict(size=12), hovertemplate='<b>%{label}</b><br>Jobs: %{value}<extra></extra>'
        )
        
        return fig

    # 3. Callback for Skills Regional Heatmap
    @app.callback(
        Output('skills-heatmap', 'figure'),
        Input('skills-exp-filter', 'value')
    )
    def update_skills_heatmap(exp_level):
        filtered_df = df.copy()
        
        if exp_level and exp_level != 'all':
            filtered_df = filtered_df[filtered_df['Experience'] == exp_level]
        
        top_regions = filtered_df['region'].value_counts().head(10).index.tolist()
        
        all_skills = []
        for skills_list in filtered_df['Skills'].dropna():
            if isinstance(skills_list, list):
                all_skills.extend(skills_list)
        top_skills = pd.Series(all_skills).value_counts().head(15).index.tolist()
        
        if not top_regions or not top_skills:
            return go.Figure()
        
        heatmap_data = []
        for region in top_regions:
            region_df = filtered_df[filtered_df['region'] == region]
            region_skills = []
            for skill in top_skills:
                count = sum(region_df['Skills'].apply(
                    lambda x: skill in x if isinstance(x, list) else False
                ))
                region_skills.append(count)
            heatmap_data.append(region_skills)
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data, x=top_skills, y=top_regions,
            colorscale='Viridis', text=np.array(heatmap_data),
            texttemplate='%{text}', textfont={"size": 10},
            hoverongaps=False, colorbar_title="Jobs"
        ))
        
        fig.update_layout(
            title='', xaxis=dict(title='Skills', tickangle=45, tickfont=dict(size=10)),
            yaxis=dict(title='Region'), height=500, title_x=0.5
        )
        
        return fig