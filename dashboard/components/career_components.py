# components/career_components.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_target_roles_table(job_titles_df):
    """Creează un tabel cu target roles pentru absolvenți"""
    
    # Target roles specifice pentru absolvenți
    target_roles = ['E-Commerce Manager', 'Marketing Specialist', 'E-Commerce Specialist', 
                    'Online Marketing Manager', 'Digital Marketing Manager', 'Sales Manager',
                    'Junior E-Commerce Manager', 'Junior Marketing Manager', 'Product Manager',
                    'Category Manager']
    
    filtered_roles = job_titles_df[job_titles_df['job_title'].isin(target_roles)]
    
    fig = go.Figure(data=[go.Table(
        header=dict(values=['Target Role', 'Number of Openings', 'Validation Status'],
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[filtered_roles['job_title'], 
                           filtered_roles['count'],
                           ['✓ Validated' for _ in range(len(filtered_roles))]],
                   fill_color='lavender',
                   align='left'))
    ])
    
    fig.update_layout(
        title='Graduate Target Roles Validation',
        height=400,
        title_x=0.5
    )
    
    return fig

def create_career_path_chart():
    """Creează un grafic cu trasee de carieră"""
    
    career_paths = {
        'Stage': ['Entry Level', 'Junior', 'Mid-Level', 'Senior', 'Lead/Manager'],
        'E-Commerce Track': [15, 25, 35, 45, 60],
        'Marketing Track': [18, 28, 38, 48, 65],
        'Sales Track': [20, 30, 40, 50, 55]
    }
    
    df = pd.DataFrame(career_paths)
    
    fig = px.line(
        df,
        x='Stage',
        y=['E-Commerce Track', 'Marketing Track', 'Sales Track'],
        markers=True,
        title='Career Progression Paths (Salary Growth in €K)',
        labels={'value': 'Salary (€K)', 'variable': 'Career Track', 'Stage': 'Career Stage'}
    )
    
    fig.update_layout(height=400, title_x=0.5)
    return fig

def create_skills_recommendation_chart(skills_df):
    """Creează un grafic cu recomandări de skill-uri pentru absolvenți"""
    
    # Selectează skill-urile cele mai importante pentru entry-level
    entry_skills = ['Marketing', 'E-Commerce', 'SEO', 'Analytics', 
                    'English', 'German', 'Social Media', 'Excel']
    
    filtered_skills = skills_df[skills_df['skill'].isin(entry_skills)]
    
    fig = px.bar(
        filtered_skills,
        x='count',
        y='skill',
        orientation='h',
        color='count',
        color_continuous_scale='Viridis',
        title='Recommended Skills for Graduates',
        labels={'count': 'Number of Job Postings', 'skill': 'Skill'}
    )
    
    fig.update_layout(
        height=450,
        title_x=0.5,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig

def create_top_companies_chart(df, top_n=10):
    """Creează un column chart (vertical) cu top companii"""
    if df.empty or 'CompanyName' not in df.columns:
        return go.Figure()
    
    company_counts = df['CompanyName'].value_counts().head(top_n).reset_index()
    company_counts.columns = ['company', 'count']
    company_counts = company_counts.sort_values('count', ascending=False)
    
    fig = px.bar(
        company_counts,
        x='company',
        y='count',
        color='count',
        color_continuous_scale='Teal',
        title=f'Top {top_n} Companies Hiring in E-Commerce',
        labels={'count': 'Jobs', 'company': 'Company'}
    )
    
    fig.update_layout(
        height=500, 
        title_x=0.5,
        xaxis={'tickangle': 45}
    )
    return fig

def create_job_source_chart(df):
    """Creează un pie chart cu distribuția joburilor pe surse - legendă jos"""
    if df.empty or 'Source' not in df.columns:
        return go.Figure()
    
    source_counts = df['Source'].value_counts().reset_index()
    source_counts.columns = ['source', 'count']
    
    # Capitalizează numele surselor
    source_counts['source'] = source_counts['source'].str.capitalize()
    
    fig = px.pie(
        source_counts,
        values='count',
        names='source',
        title='Job Distribution by Source',
        color_discrete_sequence=px.colors.qualitative.Set3,
        hole=0.3
    )
    
    fig.update_layout(
        height=500, 
        title_x=0.5,
        legend=dict(
            orientation='h',
            yanchor='top',
            y=-0.15,  # Sub grafic
            xanchor='center',
            x=0.5,
            title=''
        )
    )
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        insidetextorientation='radial'
    )
    return fig
