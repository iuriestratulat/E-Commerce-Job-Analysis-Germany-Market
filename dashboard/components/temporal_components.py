# components/temporal_components.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_temporal_line_chart(df):
    """Creează graficul trendului temporal"""
    
    if 'date_posted' not in df.columns or df['date_posted'].isna().all():
        # Date demo dacă nu există date reale
        return create_demo_temporal_chart()
    
    # Grupare pe săptămâni
    df['week'] = df['date_posted'].dt.isocalendar().week
    df['month'] = df['date_posted'].dt.month
    df['month_name'] = df['date_posted'].dt.strftime('%B')
    
    weekly_counts = df.groupby('week').size().reset_index(name='count')
    monthly_counts = df.groupby('month_name').size().reset_index(name='count')
    
    # Ordonează lunile
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    monthly_counts['month_name'] = pd.Categorical(monthly_counts['month_name'], categories=month_order, ordered=True)
    monthly_counts = monthly_counts.sort_values('month_name')
    
    fig = px.line(
        monthly_counts,
        x='month_name',
        y='count',
        markers=True,
        title='Monthly Job Postings Trend',
        labels={'month_name': 'Month', 'count': 'Number of Job Postings'}
    )
    
    fig.update_layout(
        height=400,
        title_x=0.5,
        xaxis_title="Month",
        yaxis_title="Number of Job Postings"
    )
    
    return fig

def create_demo_temporal_chart():
    """Creează un grafic demo pentru trend temporal"""
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    counts = [120, 145, 168, 192, 210, 245]
    
    fig = px.line(
        x=months, y=counts,
        markers=True,
        title='Monthly Job Postings Trend (Last 6 Months)',
        labels={'x': 'Month', 'y': 'Number of Job Postings'}
    )
    
    fig.update_layout(height=400, title_x=0.5)
    return fig

def create_work_type_chart(df):
    """Creează grafic pentru tipurile de muncă"""
    
    if 'work_type' in df.columns:
        work_counts = df['work_type'].value_counts().reset_index()
        work_counts.columns = ['work_type', 'count']
    else:
        work_counts = pd.DataFrame({'work_type': ['On-site', 'Hybrid', 'Remote'], 
                                    'count': [850, 420, 311]})
    
    fig = px.bar(
        work_counts,
        x='work_type',
        y='count',
        color='work_type',
        color_discrete_sequence=px.colors.sequential.Greens_r,
        title='Work Type Distribution',
        labels={'work_type': 'Work Type', 'count': 'Number of Jobs'}
    )
    
    fig.update_layout(height=400, title_x=0.5)
    return fig

def create_contract_type_chart(df):
    """Creează un donut chart cu tipurile de contract - legendă jos"""
    if df.empty or 'JobType' not in df.columns:
        return go.Figure()
    
    contract_counts = df['JobType'].value_counts().reset_index()
    contract_counts.columns = ['type', 'count']
    
    fig = px.pie(
        contract_counts,
        values='count',
        names='type',
        title='Contract Type Distribution',
        color_discrete_sequence=px.colors.qualitative.Set2,
        hole=0.4
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