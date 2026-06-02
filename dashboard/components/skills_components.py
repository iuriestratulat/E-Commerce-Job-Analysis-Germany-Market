import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def create_skills_bar_chart(skills_df):
    """Creează un bar chart cu top skills - cel mai mare sus"""
    if skills_df.empty:
        return go.Figure()
    
    # Sortare descrescătoare (cele mai multe joburi primele)
    skills_df = skills_df.sort_values('count', ascending=False).head(15)
    # Pentru afișare pe verticală (sus-jos), trebuie inversat
    skills_df = skills_df.sort_values('count', ascending=True)
    
    fig = px.bar(
        skills_df,
        x='count',
        y='skill',
        orientation='h',
        color='count',
        color_continuous_scale='Viridis',
        title='Top 15 Skills',
        labels={'count': 'Jobs', 'skill': 'Skills'}
    )
    
    fig.update_layout(
        height=500, 
        title_x=0.5,
        xaxis_title="Jobs",
        yaxis_title="Skills",
        yaxis=dict(categoryorder='total ascending')  # Asigură sortarea corectă
    )
    return fig

def create_word_cloud_plot(skills_df):
    """Creează un plot de tip word cloud folosind Plotly - VERSIONEA CORECTATĂ"""
    if skills_df.empty:
        return go.Figure()
    
    # Pregătește datele
    skills_df = skills_df.head(30)
    
    # Normalizează frecvențele pentru a determina dimensiunea fontului
    min_count = skills_df['count'].min()
    max_count = skills_df['count'].max()
    
    if max_count == min_count:
        skills_df['size'] = 20
    else:
        skills_df['size'] = 12 + (skills_df['count'] - min_count) / (max_count - min_count) * 48
    
    # Generează poziții aleatorii pentru cuvinte
    np.random.seed(42)
    x_pos = np.random.uniform(-1, 1, len(skills_df))
    y_pos = np.random.uniform(-1, 1, len(skills_df))
    
    # Creează o listă de culori CSS valide
    color_list = []
    for i in range(len(skills_df)):
        # Culori diferite bazate pe poziție
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                  '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        color_list.append(colors[i % len(colors)])
    
    # Creează scatter plot pentru word cloud
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=x_pos,
        y=y_pos,
        mode='text',
        text=skills_df['skill'],
        textfont=dict(
            size=skills_df['size'],
            color=color_list,  # Folosește lista de culori valide
            family='Arial, sans-serif'
        ),
        hovertext=[f"{skill}: {count} joburi" for skill, count in zip(skills_df['skill'], skills_df['count'])],
        hoverinfo='text'
    ))
    
    fig.update_layout(
        title='Top Skills Word Cloud',
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        height=500,
        plot_bgcolor='white',
        hovermode='closest'
    )
    
    return fig

def create_skills_heatmap(df):
    """Creează un heatmap cu skills pe regiuni - VERSIONEA CORECTATĂ"""
    if df.empty:
        return go.Figure()
    
    # Folosește coloana 'region' care există, nu 'region_mapped'
    if 'region' not in df.columns:
        # Dacă nu există 'region', încearcă 'city' sau creează una
        if 'city' in df.columns:
            df['region'] = df['city']
        else:
            return go.Figure()
    
    if 'Skills' not in df.columns:
        return go.Figure()
    
    # Selectează top 10 regiuni și top 15 skills
    top_regions = df['region'].value_counts().head(10).index.tolist()
    
    # Extrage top skills
    all_skills = []
    for skills_list in df['Skills'].dropna():
        if isinstance(skills_list, list):
            all_skills.extend(skills_list)
    
    skill_counts = pd.Series(all_skills).value_counts().head(15)
    top_skills = skill_counts.index.tolist()
    
    # Creează matricea pentru heatmap
    heatmap_data = []
    for region in top_regions:
        region_df = df[df['region'] == region]
        region_skills = []
        for skill in top_skills:
            # Numără câte joburi din această regiune au skill-ul respectiv
            count = sum(region_df['Skills'].apply(
                lambda x: skill in x if isinstance(x, list) else False
            ))
            region_skills.append(count)
        heatmap_data.append(region_skills)
    
    # Creează heatmap-ul
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data,
        x=top_skills,
        y=top_regions,
        colorscale='Viridis',
        text=np.array(heatmap_data),
        texttemplate='%{text}',
        textfont={"size": 10},
        hoverongaps=False
    ))
    
    fig.update_layout(
        title='Skills Distribution by Region',
        xaxis=dict(title='Skills', tickangle=45),
        yaxis=dict(title='Region'),
        height=600,
        title_x=0.5
    )
    
    return fig

def create_skills_recommendation_chart(skills_df):
    """Creează un chart cu recomandări de skills"""
    if skills_df.empty:
        return go.Figure()
    
    # Folosește top 10 skills
    top_skills = skills_df.head(10)
    
    fig = px.bar(
        top_skills,
        x='count',
        y='skill',
        orientation='h',
        color='count',
        color_continuous_scale='Reds',
        title='Top 10 Recommended Skills',
        labels={'count': 'Job Postings', 'skill': 'Skills'}
    )
    
    fig.update_layout(height=400, title_x=0.5)
    return fig