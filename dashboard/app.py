# app.py - aplicația principală Dash
import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import json
import os

# Importă componentele din data_loader
from data_loader import (load_data, get_unique_skills, filter_by_country, 
                         get_city_counts, get_skills_dataframe, 
                         get_job_titles_dataframe,
                         prepare_region_data, prepare_city_data)

# Importă componentele vizuale
from components.map_components import create_choropleth_map, create_bubble_map
from components.skills_components import create_word_cloud_plot, create_skills_heatmap, create_skills_bar_chart
from components.temporal_components import create_temporal_line_chart, create_work_type_chart, create_contract_type_chart
from components.career_components import (
    create_target_roles_table, 
    create_career_path_chart, 
    create_skills_recommendation_chart,
    create_top_companies_chart,
    create_job_source_chart
)

# Inițializare aplicație
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                assets_folder='assets')

# Încărcare date
df = load_data()

# Curăță nivelurile de experiență
from data_loader import clean_experience_level
df = clean_experience_level(df)

# === ANALIZĂ TEMPORALĂ ===
if not df.empty:
    # Extrage doar data (primii 10 caractere) și convertește
    df['PublishedDate'] = pd.to_datetime(df['PublishedDate'].str[:10], errors='coerce')
    
    # Elimină rândurile cu date nule (dacă există)
    df = df.dropna(subset=['PublishedDate'])
    
    # Adaugă coloane utile
    df['Month'] = df['PublishedDate'].dt.month
    df['Year'] = df['PublishedDate'].dt.year
    df['YearMonth'] = df['PublishedDate'].dt.strftime('%Y-%m')
    
    print(f"Perioadă date: {df['PublishedDate'].min()} -> {df['PublishedDate'].max()}")
    print(f"Total joburi după curățare date: {len(df)}")
# === SFÂRȘIT ANALIZĂ TEMPORALĂ ===

# Verificare date încărcate și creare DataFrame-uri
if not df.empty:
    city_counts = get_city_counts(df)
    skills_df = get_skills_dataframe(df)
    job_titles_df = get_job_titles_dataframe(df)
    
    print(f"Top orașe: {len(city_counts)}")
    print(f"Top skills: {len(skills_df)}")
    print(f"Top job titles: {len(job_titles_df)}")
else:
    city_counts = pd.DataFrame()
    skills_df = pd.DataFrame()
    job_titles_df = pd.DataFrame()
    print("ATENȚIE: Nu s-au putut încărca datele!")

# variabile 
if not city_counts.empty:
    top_city = city_counts.iloc[0]['city']
    top_city_count = city_counts.iloc[0]['count']
else:
    top_city = "N/A"
    top_city_count = 0

if not skills_df.empty:
    top_skill = skills_df.iloc[0]['skill']
    top_skill_count = skills_df.iloc[0]['count']
else:
    top_skill = "N/A"
    top_skill_count = 0

if not job_titles_df.empty:
    top_job = job_titles_df.iloc[0]['job_title']
    top_job_count = job_titles_df.iloc[0]['count']
else:
    top_job = "N/A"
    top_job_count = 0

# DEBUG: Afișează opțiunile dropdown-ului
print("=== DROPDOWN OPTIONS ===")
experience_options = [{'label': 'All', 'value': 'all'}] + [{'label': l, 'value': l} for l in df['Experience'].unique()]
print("Experience options:", experience_options)

# Layout aplicație
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("E-Commerce Job Market Dashboard - Germany, November 2025", 
                        className="text-center my-4"), width=12)
    ]),
    
    # Tabs pentru navigare
    dbc.Tabs([
        # Tab 1: Prezentare generală
            dbc.Tab(label="📊 Overview", children=[
            # Rândul 1: 4 carduri egale
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H4("Total Jobs Analyzed", className="card-title"),
                        html.H2(f"{len(df):,}", className="card-text text-primary")
                    ])
                ], color="light"), width=3),
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H4("Time Period", className="card-title"),
                        html.H2("Last 6 Months", className="card-text text-success")
                    ])
                ], color="light"), width=3),
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H4("Top City", className="card-title"),
                        html.H2(f"{top_city}", className="card-text text-info")
                    ])
                ], color="light"), width=3),
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H4("Top Skill", className="card-title"),
                        html.H2(f"{top_skill}", className="card-text text-warning")
                    ])
                ], color="light"), width=3),
            ], className="mb-4"),
            
            # Rândul 2: Top Skills (6) + Contract Type (6)
            dbc.Row([
                dbc.Col(dcc.Graph(figure=create_skills_bar_chart(skills_df)), width=6),
                dbc.Col(dcc.Graph(figure=create_contract_type_chart(df)), width=6),
            ], className="mb-4"),
            
            # Rândul 3: Top Companies (6) + Job Source Distribution (6)
            dbc.Row([
                dbc.Col(dcc.Graph(figure=create_top_companies_chart(df)), width=6),
                dbc.Col(dcc.Graph(figure=create_job_source_chart(df)), width=6),
            ]),
        ]),    
        
        # Tab 2: Geographic Analysis - Versiunea cu carduri
        dbc.Tab(label="🗺️ Geographic Analysis", children=[
            # Rândul 1: Filtre (2 coloane)
            dbc.Row([
                dbc.Col([
                    html.Label("Filter by Experience Level:", className="fw-bold"),
                    dcc.Dropdown(
                        id='exp-filter-map',
                        options=[{'label': 'All', 'value': 'all'}] + 
                                [{'label': str(l), 'value': str(l)} for l in df['Experience'].unique() if pd.notna(l)],
                        value='all',
                        clearable=False
                    )
                ], width=6, className="mb-3"),
                dbc.Col([
                    html.Label("Filter by Contract Type:", className="fw-bold"),
                    dcc.Dropdown(
                        id='contract-filter-map',
                        options=[{'label': 'All', 'value': 'all'}] + 
                                [{'label': str(l), 'value': str(l)} for l in df['JobType'].unique() if pd.notna(l)],
                        value='all',
                        clearable=False
                    )
                ], width=6, className="mb-3"),
            ], className="mb-4"),
            
            # Rândul 2: Graficele (2 coloane egale)
            dbc.Row([
                # Coloana 1: Bar Chart pentru Regiuni
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H4(id='region-chart-title', className="text-center mb-0")),
                        dbc.CardBody([
                            dcc.Graph(id='choropleth-map', style={'height': '500px'}, config={'displayModeBar': True})
                        ])
                    ], className="shadow-sm h-100")
                ], width=6, className="mb-3"),  # width=6 = jumătate
                
                # Coloana 2: Bubble Map pentru Orașe
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H4(id='bubble-map-title', className="text-center mb-0")),
                        dbc.CardBody([
                            dcc.Graph(id='bubble-map', style={'height': '500px'}, config={'displayModeBar': True})
                        ])
                    ], className="shadow-sm h-100")
                ], width=6, className="mb-3"),  # width=6 = jumătate
            ]),
        ]),

        # Tab 3: Skills Analysis
        dbc.Tab(label="🔧 Skills Analysis", children=[
            # Rândul 1: Filtru Experience Level
            dbc.Row([
                dbc.Col([
                    html.Label("Filter by Experience Level:", className="fw-bold"),
                    dcc.Dropdown(
                        id='skills-exp-filter',
                        options=[{'label': 'All', 'value': 'all'}] + 
                                [{'label': str(l), 'value': str(l)} for l in df['Experience'].unique() if pd.notna(l)],
                        value='all',
                        clearable=False
                    )
                ], width=4, className="mb-3"),
            ], className="mb-4"),
            
            # Rândul 2: Top 15 Skills + Word Cloud (două coloane)
            dbc.Row([
                # Coloana 1: Top 15 Skills Bar Chart
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H4(id='skills-bar-title', className="text-center mb-0")),
                        dbc.CardBody([
                            dcc.Graph(id='skills-bar-chart', style={'height': '500px'}, config={'displayModeBar': True})
                        ])
                    ], className="shadow-sm h-100")
                ], width=6, className="mb-3"),
                
                # Coloana 2: Word Cloud
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H4("🌳 Skills Treemap", className="text-center mb-0")),
                        dbc.CardBody([
                            dcc.Graph(id='word-cloud-plot', style={'height': '500px'}, config={'displayModeBar': True})
                        ])
                    ], className="shadow-sm h-100")
                ], width=6, className="mb-3"),
            ], className="mb-4"),
            
            # Rândul 3: Skills Distribution by Region (Heatmap)
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H4("🔥 Skills Distribution by Region", className="text-center mb-0")),
                        dbc.CardBody([
                            dcc.Graph(id='skills-heatmap', style={'height': '600px'}, config={'displayModeBar': True})
                        ])
                    ], className="shadow-sm")
                ], width=12)
            ]),
        ]),
        
        # Tab 4: Job Distribution - Format 2x2 cu tooltip-uri
        dbc.Tab(label="💼 Job Distribution", children=[
            # Rândul 1: Experience Level + Contract Type
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.Div([
                                html.H4("📈 Job Distribution by Experience Level", className="mb-0 d-inline"),
                                html.Span(
                                    " ⓘ",
                                    id="experience-info-tooltip",
                                    style={"cursor": "pointer", "fontSize": "18px", "marginLeft": "10px", "color": "#17a2b8", "fontWeight": "bold"}
                                ),
                                dbc.Tooltip(
                                    "📌 **Level Descriptions:**\n\n"
                                    "• **Entry level:** Jobs for beginners or those with minimal experience.\n\n"
                                    "• **Mid-Senior level:** Roles requiring established experience and autonomy.\n\n"
                                    "• **Associate:** Typically requires 2-4 years of experience.\n\n"
                                    "• **Internship:** Temporary positions for students or trainees.\n\n"
                                    "• **Director:** Senior leadership role, manages departments.\n\n"
                                    "• **Executive:** Highest-level strategic roles (C-level, VP, etc.)\n\n"
                                    "• **Not Applicable:** Experience level not specified.",
                                    target="experience-info-tooltip",
                                    placement="top",
                                    style={"whiteSpace": "pre-line", "maxWidth": "350px", "fontSize": "12px"}
                                )
                            ], className="text-center")
                        ]),
                        dbc.CardBody([
                            dcc.Graph(id='experience-level-chart', style={'height': '400px'}, config={'displayModeBar': True})
                        ])
                    ], className="shadow-sm h-100")
                ], width=6, className="mb-3"),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.Div([
                                html.H4("📝 Job Distribution by Contract Type", className="mb-0 d-inline"),
                                html.Span(
                                    " ⓘ",
                                    id="contract-info-tooltip",
                                    style={"cursor": "pointer", "fontSize": "18px", "marginLeft": "10px", "color": "#17a2b8", "fontWeight": "bold"}
                                ),
                                dbc.Tooltip(
                                    "📌 **Type Descriptions:**\n\n"
                                    "• **Full-time:** Standard ~40-hour work week, permanent position.\n\n"
                                    "• **Part-time:** Position with fewer hours than a full-time role.\n\n"
                                    "• **Contract:** A temporary role for a specific project or time period.\n\n"
                                    "• **Internship:** Temporary position for students or trainees.\n\n"
                                    "• **Other:** A non-standard employment type not otherwise categorized.\n\n"
                                    "• **Temporary:** A short-term, non-contract position.\n\n"
                                    "• **Apprentice/Trainee:** A role focused on training and learning a new trade/skill.",
                                    target="contract-info-tooltip",
                                    placement="top",
                                    style={"whiteSpace": "pre-line", "maxWidth": "350px", "fontSize": "12px"}
                                )
                            ], className="text-center")
                        ]),
                        dbc.CardBody([
                            dcc.Graph(id='contract-type-chart', style={'height': '400px'}, config={'displayModeBar': True})
                        ])
                    ], className="shadow-sm h-100")
                ], width=6, className="mb-3"),
            ], className="mb-3"),
            
            # Rândul 2: Work Type + Company Market Share
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.Div([
                                html.H4("💼 Top 15 Job Distribution by Work Type", className="mb-0 d-inline"),
                                html.Span(
                                    " ⓘ",
                                    id="worktype-info-tooltip",
                                    style={"cursor": "pointer", "fontSize": "18px", "marginLeft": "10px", "color": "#17a2b8", "fontWeight": "bold"}
                                ),
                                dbc.Tooltip(
                                    "📌 **Work Type Descriptions:**\n\n"
                                    "• **Work sectors** represent the functional area of the job.\n\n"
                                    "• Examples include: Marketing, Sales, IT, Management, Customer Service.\n\n"
                                    "• Many roles combine multiple functions (e.g., Sales & Marketing).\n\n"
                                    "• This chart shows the top 15 most common work type combinations.",
                                    target="worktype-info-tooltip",
                                    placement="top",
                                    style={"whiteSpace": "pre-line", "maxWidth": "350px", "fontSize": "12px"}
                                )
                            ], className="text-center")
                        ]),
                        dbc.CardBody([
                            dcc.Graph(id='work-type-chart', style={'height': '400px'}, config={'displayModeBar': True})
                        ])
                    ], className="shadow-sm h-100")
                ], width=6, className="mb-3"),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.Div([
                                html.H4("🏢 Top 5 Company Market Share", className="mb-0 d-inline"),
                                html.Span(
                                    " ⓘ",
                                    id="company-info-tooltip",
                                    style={"cursor": "pointer", "fontSize": "18px", "marginLeft": "10px", "color": "#17a2b8", "fontWeight": "bold"}
                                ),
                                dbc.Tooltip(
                                    "📌 **Chart Explanation:**\n\n"
                                    "• Shows market share of top 5 companies across top 5 regions.\n\n"
                                    "• Companies outside top 5 are excluded from the bars.\n\n"
                                    "• The percentage in parentheses shows how much of the market is 'Other' companies.\n\n"
                                    "• Example: 'Berlin (95% Other)' means 95% of jobs are from companies outside top 5.",
                                    target="company-info-tooltip",
                                    placement="top",
                                    style={"whiteSpace": "pre-line", "maxWidth": "350px", "fontSize": "12px"}
                                )
                            ], className="text-center")
                        ]),
                        dbc.CardBody([
                            dcc.Graph(id='company-market-share', style={'height': '400px'}, config={'displayModeBar': True})
                        ])
                    ], className="shadow-sm h-100")
                ], width=6, className="mb-3"),
            ]),
        ]),

        # Tab 5: Career Progression - CU DECOMPOSITION TREE
        dbc.Tab(label="🎯 Career Progression", children=[
            # Rândul 1: Filtru Experience Level
            dbc.Row([
                dbc.Col([
                    html.Label("Filter by Experience Level:", className="fw-bold"),
                    dcc.Dropdown(
                        id='career-exp-filter',
                        options=[{'label': 'All', 'value': 'all'}] + 
                                [{'label': str(l), 'value': str(l)} for l in df['Experience'].unique() if pd.notna(l)],
                        value='all',
                        clearable=False
                    )
                ], width=4, className="mb-3"),
            ], className="mb-4"),
            
            # Rândul 2: Două coloane (Contract Types + Decomposition Tree)
            dbc.Row([
                # Coloana 1: Contract Types by Experience Level
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H4("📊 Contract Types by Experience Level", className="text-center mb-0")),
                        dbc.CardBody([
                            dcc.Graph(id='career-contract-chart', style={'height': '450px'})
                        ])
                    ], className="shadow-sm h-100")
                ], width=6, className="mb-3"),
                
                # Coloana 2: Decomposition Tree (Sunburst)
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.Div([
                                html.H4("🌲 Decomposition Tree: Experience → Work Type → Contract", className="text-center mb-0 d-inline"),
                                html.Span(
                                    " ⓘ",
                                    id="sunburst-tooltip",
                                    style={"cursor": "pointer", "fontSize": "18px", "marginLeft": "10px", "color": "#17a2b8", "fontWeight": "bold"}
                                ),
                                dbc.Tooltip(
                                    "📌 **How to read:**\n\n"
                                    "• **Inner ring:** Experience Level\n\n"
                                    "• **Middle ring:** Work Type\n\n"
                                    "• **Outer ring:** Contract Type\n\n"
                                    "• Size of each segment = number of jobs\n\n"
                                    "• Click on any segment to zoom in\n\n"
                                    "• Hover for detailed information",
                                    target="sunburst-tooltip",
                                    placement="top",
                                    style={"whiteSpace": "pre-line", "maxWidth": "350px", "fontSize": "12px"}
                                )
                            ], className="text-center")
                        ]),
                        dbc.CardBody([
                            dcc.Graph(id='career-sunburst', style={'height': '450px'})
                        ])
                    ], className="shadow-sm h-100")
                ], width=6, className="mb-3"),
            ], className="mb-4"),
            
            # Rândul 3: Work Types by Experience Level + (al doilea Decomposition Tree - poate alt nivel)
            dbc.Row([
                # Coloana 1: Work Types by Experience Level (Stacked Horizontal)
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H4("📊 Work Types by Experience Level", className="text-center mb-0")),
                        dbc.CardBody([
                            dcc.Graph(id='career-worktype-stacked', style={'height': '450px'})
                        ])
                    ], className="shadow-sm h-100")
                ], width=6, className="mb-3"),
                
                # Coloana 2: Sankey Diagram (Experience → Region → City)
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.Div([
                                html.H4("🌊 Sankey Diagram: Experience → Region → City", className="text-center mb-0 d-inline"),
                                html.Span(
                                    " ⓘ",
                                    id="sankey-tooltip",
                                    style={"cursor": "pointer", "fontSize": "18px", "marginLeft": "10px", "color": "#17a2b8", "fontWeight": "bold"}
                                ),
                                dbc.Tooltip(
                                    "📌 **How to read:**\n\n"
                                    "• **Left nodes:** Experience Level\n\n"
                                    "• **Middle nodes:** Region in Germany\n\n"
                                    "• **Right nodes:** City\n\n"
                                    "• Thicker lines = more job postings\n\n"
                                    "• Hover over lines for details",
                                    target="sankey-tooltip",
                                    placement="top",
                                    style={"whiteSpace": "pre-line", "maxWidth": "350px", "fontSize": "12px"}
                                )
                            ], className="text-center")
                        ]),
                        dbc.CardBody([
                            dcc.Graph(id='career-sankey', style={'height': '500px'})
                        ])
                    ], className="shadow-sm h-100")
                ], width=6, className="mb-3"),
            ]),
        ]),

        # Tab 6: Temporal Trends
        dbc.Tab(label="📈 Temporal Analysis", children=[
            # Rândul 1: Filtre
            dbc.Row([
                dbc.Col([
                    html.Label("Select Month:", className="fw-bold"),
                    dcc.Dropdown(
                        id='trends-month-filter',
                        options=[{'label': 'All Months', 'value': 'all'}] +
                                [{'label': month, 'value': month} for month in sorted(df['YearMonth'].unique())],
                        value='all',
                        clearable=False
                    )
                ], width=5, className="mb-3"),
                dbc.Col([
                    html.Label("Filter by Experience Level:", className="fw-bold"),
                    dcc.Dropdown(
                        id='trends-exp-filter',
                        options=[{'label': 'All', 'value': 'all'}] + 
                                [{'label': str(l), 'value': str(l)} for l in df['Experience'].unique() if pd.notna(l)],
                        value='all',
                        clearable=False
                    )
                ], width=5, className="mb-3"),
            ], className="mb-4"),
            
            # Rândul 2: Weekly Job Posting Trend (full width)
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H4("📅 Weekly Job Posting Trend (Last 6 Months)", className="text-center mb-0")),
                        dbc.CardBody([
                            dcc.Graph(id='trends-line-chart', style={'height': '400px'}, config={'displayModeBar': True})
                        ])
                    ], className="shadow-sm")
                ], width=12, className="mb-4"),
            ]),
            
            # Rândul 3: Job Type Stacked (stânga) + Region Bar (dreapta)
            dbc.Row([
                # Coloana 1: Job Type Distribution by Month
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H4("📊 Job Type Distribution by Month", className="text-center mb-0")),
                        dbc.CardBody([
                            dcc.Graph(id='trends-jobtype-stacked', style={'height': '450px'}, config={'displayModeBar': True})
                        ])
                    ], className="shadow-sm h-100")
                ], width=6, className="mb-3"),
                
                # Coloana 2: Job Distribution by Region (toate regiunile)
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H4("📍 Job Distribution by Region", className="text-center mb-0")),
                        dbc.CardBody([
                            dcc.Graph(id='trends-region-chart', style={'height': '450px'}, config={'displayModeBar': True})
                        ])
                    ], className="shadow-sm h-100")
                ], width=6, className="mb-3"),
            ]),
        ]),

        # Tab 7: Conclusions
        dbc.Tab(label="🎓 Conclusions", children=[
            dbc.Row([
                dbc.Col([
                    html.H3("E-Commerce Job Market Analysis - Key Takeaways for Graduates", 
                            className="text-center mb-4 text-primary"),
                    html.Hr(),
                ], width=12),
            ]),
            
            # Row 1: Market Overview
            dbc.Row([
                dbc.Col([
                    html.H4("📊 Market Overview", className="mt-2 mb-3"),
                    html.P([
                        "The E-Commerce job market in Germany shows a ", 
                        html.Strong("robust and growing ecosystem"), 
                        f", with a total of ", html.Strong(f"{len(df):,} jobs"), 
                        " posted in the last 6 months."
                    ]),
                    html.Ul([
                        html.Li([html.Strong("Berlin"), f" is the undisputed hub ({top_city_count} jobs, {top_city_count/len(df)*100:.1f}% of total)"]),
                        html.Li("The market is concentrated in western and southern Germany (Berlin, Hamburg, Munich, Cologne, Frankfurt)"),
                        html.Li("Eastern regions (Saxony, Brandenburg) offer fewer opportunities but are developing"),
                    ]),
                ], width=12),
            ], className="mb-4"),
            
            # Row 2: Essential Skills
            dbc.Row([
                dbc.Col([
                    html.H4("🔧 Essential Skills for Success", className="mb-3"),
                    html.P("Most sought-after competencies in the current market:"),
                    html.Ol([
                        html.Li([html.Strong("Digital Marketing"), " - most demanded skill (over 15% of jobs)"]),
                        html.Li([html.Strong("E-Commerce"), " - fundamental for the industry"]),
                        html.Li([html.Strong("Analytics / Google Analytics"), " - data-driven decisions are essential"]),
                        html.Li([html.Strong("SEO / SEM"), " - online visibility is key to success"]),
                        html.Li([html.Strong("IT / Technical Skills"), " - key differentiator for advancement"]),
                    ]),
                ], width=6),
                
                dbc.Col([
                    html.H4("🌍 Language Requirements", className="mb-3"),
                    html.P("Bilingualism is a major advantage in the German market:"),
                    html.Ul([
                        html.Li([html.Strong("English"), " - mandatory for most jobs (85%+ of postings)"]),
                        html.Li([html.Strong("German"), " - required for local roles (60%+ of postings)"]),
                        html.Li("Bilingual candidates have a significant competitive advantage"),
                        html.Li("Startups and international companies are more flexible with language"),
                    ]),
                ], width=6),
            ], className="mb-4"),
            
            # Row 3: Contract & Experience
            dbc.Row([
                dbc.Col([
                    html.H4("📝 Contract & Experience Distribution", className="mb-3"),
                    html.P("Predominant contract types:"),
                    html.Ul([
                        html.Li([html.Strong("84% Full-time"), " - market dominated by full-time positions"]),
                        html.Li([html.Strong("9% Part-time"), " - opportunities for flexibility"]),
                        html.Li("Temporary contracts represent only 7% of the market"),
                    ]),
                    html.P("Experience levels:", className="mt-3"),
                    html.Ul([
                        html.Li([html.Strong("Mid-Senior level"), " dominates the market (over 50% of jobs)"]),
                        html.Li([html.Strong("Entry level"), " has significant presence (~15%) - opportunities for graduates"]),
                        html.Li("Internships are limited - approximately 5% of the market"),
                    ]),
                ], width=6),
                
                dbc.Col([
                    html.H4("🏢 Top Hiring Hubs", className="mb-3"),
                    html.P("Most active regions for E-Commerce jobs:"),
                    html.Ul([
                        html.Li([html.Strong("Berlin"), " - #1 hub (391 jobs)"]),
                        html.Li([html.Strong("Hamburg & Munich"), " - tier 2, dozens of opportunities"]),
                        html.Li([html.Strong("North Rhine-Westphalia"), " - multiple cities (Cologne, Düsseldorf, Dortmund)"]),
                        html.Li("Frankfurt (Hesse) - financial and growing e-commerce hub"),
                    ]),
                ], width=6),
            ], className="mb-4"),
            
            # Row 4: Target Roles & Salary
            dbc.Row([
                dbc.Col([
                    html.H4("💼 Target Roles Validated for Graduates", className="mb-3"),
                    html.P("Most accessible and promising roles for graduates:"),
                    html.Ul([
                        html.Li([html.Strong("Online Marketing Manager (m/w/d)"), " - most frequent entry-level role"]),
                        html.Li([html.Strong("E-Commerce Specialist / Manager"), " - rapid growth potential"]),
                        html.Li([html.Strong("Digital Marketing Manager"), " - marketing+tech combination"]),
                        html.Li([html.Strong("Sales Specialist / Category Manager"), " - commercial roles"]),
                    ]),
                ], width=6),
                
                dbc.Col([
                    html.H4("💰 Career Progression & Salary", className="mb-3"),
                    html.P("Estimated salary progression (E-Commerce track):"),
                    html.Ul([
                        html.Li([html.Strong("Entry Level"), ": €38K - €48K"]),
                        html.Li([html.Strong("Junior"), ": €48K - €55K"]),
                        html.Li([html.Strong("Mid-Level"), ": €55K - €70K"]),
                        html.Li([html.Strong("Senior"), ": €70K - €90K+"]),
                        html.Li([html.Strong("Lead/Manager"), ": €90K - €120K+"]),
                    ]),
                    html.P("Marketing and E-Commerce tracks have the best salary progression.", 
                        className="mt-2 text-muted small"),
                ], width=6),
            ], className="mb-4"),
            
            # Row 5: Final Recommendations
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H4("🎯 Final Recommendations for Graduates", className="text-center mb-0")),
                        dbc.CardBody([
                            html.H5("📌 To enter the market:", className="mt-2"),
                            html.Ol([
                                html.Li([html.Strong("Invest in Digital Marketing and Google Analytics skills")]),
                                html.Li([html.Strong("Learn E-Commerce fundamentals"), " (platforms, logistics, customer journey)"]),
                                html.Li([html.Strong("German language"), " is a major differentiator - start courses ASAP"]),
                                html.Li("Build a portfolio with practical projects (Google Analytics certified, etc.)"),
                            ]),
                            html.H5("📌 Professional development:", className="mt-3"),
                            html.Ol([
                                html.Li([html.Strong("Start as a Junior E-Commerce Manager"), " or ", html.Strong("Online Marketing Specialist")]),
                                html.Li([html.Strong("After 2-3 years, advance to Mid-Level with €55K+")]),
                                html.Li("Specialize in a niche (SEO, Analytics, Marketplace Management)"),
                            ]),
                            html.H5("📌 Market Outlook:", className="mt-3"),
                            html.P([
                                "The German E-Commerce market shows ", html.Strong("strong growth"), 
                                " with increasing demand for hybrid skills combining marketing, technology, and data analytics. ",
                                "Graduates who invest in ", html.Strong("digital skills + German language"), 
                                " have the highest chances of quick employment and career advancement."
                            ]),
                        ])
                    ], className="shadow-sm border-primary")
                ], width=12)
            ], className="mt-2"),
            
            # Footer
            dbc.Row([
                dbc.Col(html.Hr(), width=12),
                dbc.Col(html.P("Data source: LinkedIn, Glassdoor, Stepstone | Analysis based on 1,581 job postings | Dashboard built with Plotly Dash", 
                            className="text-center text-muted small"), width=12),
            ], className="mt-3"),
        ]),
     #End Tabs pentru navigare 
    ]),
    
    # Footer
    dbc.Row([
        dbc.Col(html.Hr(), width=12),
        dbc.Col(html.P("Data source: LinkedIn, Glassdoor, Stepstone | Dashboard built with Plotly Dash", 
                       className="text-center text-muted"), width=12),
    ]),
], fluid=True)

# Callbacks pentru update-uri interactive
# Tab 2 callbacks
# Callback pentru harta regiunilor (bar chart)
@callback(
    [Output('choropleth-map', 'figure'),
     Output('region-chart-title', 'children')],
    [Input('exp-filter-map', 'value'),
     Input('contract-filter-map', 'value')]
)
def update_region_chart(exp_level, contract_type):
    # Aplică filtrele
    filtered_df = df.copy()
    
    if exp_level and exp_level != 'all':
        filtered_df = filtered_df[filtered_df['Experience'] == exp_level]
    
    if contract_type and contract_type != 'all':
        filtered_df = filtered_df[filtered_df['JobType'] == contract_type]
    
    # Creează bar chart pentru regiuni
    region_counts = filtered_df['region'].value_counts().head(15).reset_index()
    region_counts.columns = ['region', 'count']
    region_counts = region_counts.sort_values('count', ascending=True)
    
    # Creează titlul dinamic
    num_regions = len(region_counts)
    if num_regions == 0:
        title_text = "📊 No Regions Found"
    elif num_regions == 1:
        title_text = f"📊 Job Distribution by Region ({num_regions} region)"
    else:
        title_text = f"📊 Job Distribution by Region ({num_regions} regions)"
    
    fig = px.bar(
        region_counts,
        x='count',
        y='region',
        orientation='h',
        color='count',
        color_continuous_scale='Blues',
        title='',  # Golim titlul deoarece avem în CardHeader
        labels={'count': 'Jobs', 'region': 'Region'}
    )
    
    fig.update_layout(
        height=500,
        title_x=0.5,
        xaxis_title="Jobs",
        yaxis_title="Region",
        showlegend=False
    )
    
    # Ascunde bara de culori (color bar)
    fig.update_coloraxes(showscale=False)
    
    return fig, title_text

# Callback pentru harta cu bule (orașe)
@callback(
    [Output('bubble-map', 'figure'),
     Output('bubble-map-title', 'children')],  # ← nou Output pentru titlu
    [Input('exp-filter-map', 'value'),
     Input('contract-filter-map', 'value')]
)
def update_bubble_map(exp_level, contract_type):
    # Aplică filtrele
    filtered_df = df.copy()
    
    if exp_level and exp_level != 'all':
        filtered_df = filtered_df[filtered_df['Experience'] == exp_level]
    
    if contract_type and contract_type != 'all':
        filtered_df = filtered_df[filtered_df['JobType'] == contract_type]
    
    # Încarcă coordonatele orașelor
    coords_path = os.path.join('data', 'city_coordinates.json')
    try:
        with open(coords_path, 'r', encoding='utf-8') as f:
            city_coords = json.load(f)
    except FileNotFoundError:
        print(f"Fișierul {coords_path} nu a fost găsit!")
        city_coords = {}
    
    # Pregătește datele pentru orașe
    city_counts = filtered_df['city'].value_counts().head(30).reset_index()
    city_counts.columns = ['city', 'count']
    
    # Filtrează doar orașele care au coordonate
    city_counts = city_counts[city_counts['city'].isin(city_coords.keys())]
    
    # Adaugă coordonatele
    city_counts['lat'] = city_counts['city'].apply(lambda x: city_coords.get(x, [51.1657, 10.4515])[0])
    city_counts['lon'] = city_counts['city'].apply(lambda x: city_coords.get(x, [51.1657, 10.4515])[1])
    
    # Creează titlul dinamic
    num_cities = len(city_counts)
    if num_cities == 0:
        title_text = "📍 No E-Commerce Hubs Found"
    elif num_cities == 1:
        title_text = f"📍 {num_cities} E-Commerce Hub in Germany"
    else:
        title_text = f"📍 Top {num_cities} E-Commerce Hubs in Germany"
    
    fig = px.scatter_mapbox(
        city_counts,
        lat='lat',
        lon='lon',
        size='count',
        color='count',
        hover_name='city',
        title='',  # Golim titlul deoarece avem în CardHeader
        color_continuous_scale='Viridis',
        size_max=50,
        zoom=5,
        center={"lat": 51.1657, "lon": 10.4515},
        height=500,
        labels={'count': 'Jobs'}
    )
    
    fig.update_layout(
        mapbox_style="carto-positron",
        title_x=0.5,
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    
    fig.update_coloraxes(colorbar_title_text="Jobs")
    
    return fig, title_text  # ← Returnează și titlul

# Tab 3 callbacks
# Callback pentru Top 15 Skills Bar Chart
@callback(
    [Output('skills-bar-chart', 'figure'),
     Output('skills-bar-title', 'children')],
    Input('skills-exp-filter', 'value')
)
def update_skills_bar(exp_level):
    # Aplică filtrul
    filtered_df = df.copy()
    
    if exp_level and exp_level != 'all':
        filtered_df = filtered_df[filtered_df['Experience'] == exp_level]
    
    # Extrage skill-urile
    all_skills = []
    for skills_list in filtered_df['Skills'].dropna():
        if isinstance(skills_list, list):
            all_skills.extend(skills_list)
    
    # Creează DataFrame cu frecvențe
    skill_counts = pd.Series(all_skills).value_counts().head(15).reset_index()
    skill_counts.columns = ['skill', 'count']
    skill_counts = skill_counts.sort_values('count', ascending=True)
    
    # Titlu dinamic
    num_skills = len(skill_counts)
    title_text = f"📊 Top {num_skills} Skills" if num_skills > 0 else "📊 No Skills Found"
    
    fig = px.bar(
        skill_counts,
        x='count',
        y='skill',
        orientation='h',
        color='count',
        color_continuous_scale='Viridis',
        title='',
        labels={'count': 'Jobs', 'skill': 'Skills'}
    )
    
    fig.update_layout(
        height=500,
        title_x=0.5,
        xaxis_title="Number of Jobs",
        yaxis_title="Skills",
        showlegend=False
    )
    
    fig.update_coloraxes(showscale=False)
    
    return fig, title_text

# Callback pentru Treemap
@callback(
    Output('word-cloud-plot', 'figure'),
    Input('skills-exp-filter', 'value')
)
def update_treemap(exp_level):
    # Aplică filtrul
    filtered_df = df.copy()
    
    if exp_level and exp_level != 'all':
        filtered_df = filtered_df[filtered_df['Experience'] == exp_level]
    
    # Extrage skill-urile
    all_skills = []
    for skills_list in filtered_df['Skills'].dropna():
        if isinstance(skills_list, list):
            all_skills.extend(skills_list)
    
    # Creează DataFrame cu frecvențe
    skill_counts = pd.Series(all_skills).value_counts().head(30).reset_index()
    skill_counts.columns = ['skill', 'count']
    
    if skill_counts.empty:
        return go.Figure()
    
    # Treemap
    fig = px.treemap(
        skill_counts,
        path=['skill'],
        values='count',
        color='count',
        color_continuous_scale='Viridis',
        title='',
        labels={'count': 'Jobs', 'skill': 'Skills'}
    )
    
    fig.update_layout(
        height=500,
        title_x=0.5,
        margin=dict(t=0, l=0, r=0, b=0)
    )
    
    fig.update_traces(
        textinfo='label+value',
        textposition='middle center',
        textfont=dict(size=12),
        hovertemplate='<b>%{label}</b><br>Jobs: %{value}<extra></extra>'
    )
    
    return fig

# Callback pentru Skills Heatmap
@callback(
    Output('skills-heatmap', 'figure'),
    Input('skills-exp-filter', 'value')
)
def update_skills_heatmap(exp_level):
    # Aplică filtrul
    filtered_df = df.copy()
    
    if exp_level and exp_level != 'all':
        filtered_df = filtered_df[filtered_df['Experience'] == exp_level]
    
    # Top 10 regiuni
    top_regions = filtered_df['region'].value_counts().head(10).index.tolist()
    
    # Top 15 skills
    all_skills = []
    for skills_list in filtered_df['Skills'].dropna():
        if isinstance(skills_list, list):
            all_skills.extend(skills_list)
    top_skills = pd.Series(all_skills).value_counts().head(15).index.tolist()
    
    if not top_regions or not top_skills:
        return go.Figure()
    
    # Creează matricea pentru heatmap
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
        z=heatmap_data,
        x=top_skills,
        y=top_regions,
        colorscale='Viridis',
        text=np.array(heatmap_data),
        texttemplate='%{text}',
        textfont={"size": 10},
        hoverongaps=False,
        colorbar_title="Jobs"
    ))
    
    fig.update_layout(
        title='',
        xaxis=dict(title='Skills', tickangle=45, tickfont=dict(size=10)),
        yaxis=dict(title='Region'),
        height=600,
        title_x=0.5
    )
    
    return fig

# Tab 4 callbacks
# Callback pentru Experience Level Distribution (Bar Chart)
@callback(
    Output('experience-level-chart', 'figure'),
    Input('skills-exp-filter', 'value')
)
def update_experience_chart(exp_level):
    # Aplică filtrul
    filtered_df = df.copy()
    
    if exp_level and exp_level != 'all':
        filtered_df = filtered_df[filtered_df['Experience'] == exp_level]
    
    # Numără joburile pe nivele de experiență
    exp_counts = filtered_df['Experience'].value_counts().reset_index()
    exp_counts.columns = ['experience', 'count']
    exp_counts = exp_counts.sort_values('count', ascending=False)
    
    fig = px.bar(
        exp_counts,
        x='experience',
        y='count',
        color='count',
        color_continuous_scale='Viridis',
        title='',
        labels={'count': 'Number of Jobs', 'experience': 'Experience Level'}
    )
    
    fig.update_layout(
        height=450,
        title_x=0.5,
        xaxis_title="Experience Level",
        yaxis_title="Number of Jobs",
        showlegend=False,
        xaxis={'tickangle': 45}
    )
    
    fig.update_coloraxes(showscale=False)
    
    return fig

# Callback pentru Contract Type Distribution (Donut Chart)
@callback(
    Output('contract-type-chart', 'figure'),
    Input('skills-exp-filter', 'value')
)
def update_contract_chart(exp_level):
    # Aplică filtrul
    filtered_df = df.copy()
    
    if exp_level and exp_level != 'all':
        filtered_df = filtered_df[filtered_df['Experience'] == exp_level]
    
    # Numără joburile pe tip de contract
    contract_counts = filtered_df['JobType'].value_counts().reset_index()
    contract_counts.columns = ['contract', 'count']
    
    # Calculează procentele
    total = contract_counts['count'].sum()
    contract_counts['percentage'] = (contract_counts['count'] / total) * 100
    
    # Grupează categoriile sub 5%
    under_5_sum = contract_counts[contract_counts['percentage'] < 5]['count'].sum()
    
    # Filtrează categoriile peste 5%
    main_categories = contract_counts[contract_counts['percentage'] >= 5].copy()
    
    # Adaugă categoria "Other (under 5%)" dacă există
    if under_5_sum > 0:
        other_row = pd.DataFrame({
            'contract': ['Other (under 5%)'],
            'count': [under_5_sum],
            'percentage': [(under_5_sum / total) * 100]
        })
        main_categories = pd.concat([main_categories, other_row], ignore_index=True)
    
    fig = px.pie(
        main_categories,
        values='count',
        names='contract',
        title='',
        color_discrete_sequence=px.colors.qualitative.Set2,
        hole=0.4
    )
    
    fig.update_layout(
        height=450,
        title_x=0.5,
        legend=dict(orientation='h', yanchor='bottom', y=-0.1, xanchor='center', x=0.5)
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    return fig

# Callback pentru Work Type Distribution (Horizontal Bar Chart)
@callback(
    Output('work-type-chart', 'figure'),
    Input('skills-exp-filter', 'value')
)
def update_work_type_chart(exp_level):
    # Aplică filtrul
    filtered_df = df.copy()
    
    if exp_level and exp_level != 'all':
        filtered_df = filtered_df[filtered_df['Experience'] == exp_level]
    
    # Numără joburile pe tip de muncă
    work_counts = filtered_df['WorkType'].value_counts().head(15).reset_index()
    work_counts.columns = ['work_type', 'count']
    work_counts = work_counts.sort_values('count', ascending=True)
    
    fig = px.bar(
        work_counts,
        x='count',
        y='work_type',
        orientation='h',
        color='count',
        color_continuous_scale='Teal',
        title='',
        labels={'count': 'Number of Jobs', 'work_type': 'Work Type'}
    )
    
    fig.update_layout(
        height=400,
        title_x=0.5,
        xaxis_title="Number of Jobs",
        yaxis_title="Work Type",
        showlegend=False
    )
    
    fig.update_coloraxes(showscale=False)
    
    return fig

# Callback pentru Company Market Share (Stacked Bar Chart - orizontal)
@callback(
    Output('company-market-share', 'figure'),
    Input('skills-exp-filter', 'value')
)
def update_company_market_share(exp_level):
    # Aplică filtrul
    filtered_df = df.copy()
    
    if exp_level and exp_level != 'all':
        filtered_df = filtered_df[filtered_df['Experience'] == exp_level]
    
    # Top 5 regiuni
    top_regions = filtered_df['region'].value_counts().head(5).index.tolist()
    
    # Top 5 companii
    top_companies = filtered_df['CompanyName'].value_counts().head(5).index.tolist()
    
    # Grupăm datele
    region_company = filtered_df[filtered_df['region'].isin(top_regions)].copy()
    
    # Filtrează doar companiile din top 5 (exclude Other)
    region_company_top = region_company[region_company['CompanyName'].isin(top_companies)]
    
    # Calculează numărul total de joburi per regiune
    region_totals = filtered_df[filtered_df['region'].isin(top_regions)].groupby('region').size().reset_index(name='total')
    
    # Calculează joburile din top companii per regiune
    region_top_counts = region_company_top.groupby('region').size().reset_index(name='top_count')
    
    # Îmbină pentru a calcula procentul
    region_stats = region_totals.merge(region_top_counts, on='region', how='left').fillna(0)
    region_stats['other_percentage'] = 100 - (region_stats['top_count'] / region_stats['total']) * 100
    
    # Creează nume noi pentru regiuni cu procentul Other
    region_stats['region_label'] = region_stats.apply(
        lambda x: f"{x['region']}<br>({x['other_percentage']:.0f}% Other)", axis=1
    )
    
    # Creează mapping pentru etichete
    region_label_map = dict(zip(region_stats['region'], region_stats['region_label']))
    
    # Calculează distribuția companiilor pentru stacking
    company_dist = region_company_top.groupby(['region', 'CompanyName']).size().reset_index(name='count')
    
    # Calculează procente pe regiune
    region_totals_top = company_dist.groupby('region')['count'].sum().reset_index(name='total')
    company_dist = company_dist.merge(region_totals_top, on='region')
    company_dist['percentage'] = (company_dist['count'] / company_dist['total']) * 100
    
    # Aplică etichetele noi
    company_dist['region_label'] = company_dist['region'].map(region_label_map)
    
    # Pregătește ordinea companiilor
    company_order = top_companies
    
    fig = px.bar(
        company_dist,
        x='region_label',
        y='percentage',
        color='CompanyName',
        title='',
        labels={'region_label': 'Regions', 'percentage': 'Market Share (%)', 'CompanyName': 'Company'},
        category_orders={'CompanyName': company_order},
        color_discrete_sequence=px.colors.qualitative.Set3,
        text='percentage'
    )
    
    fig.update_layout(
        height=450,
        title_x=0.5,
        xaxis_title="",
        yaxis_title="Market Share (%)",
        legend=dict(
            orientation='v',           # Verticală
            yanchor='top',             # Ancorat sus
            y=1.0,                     # Poziție sus
            xanchor='left',            # Ancorat stânga
            x=1.02,                    # Puțin în dreapta graficului
            title=''
        ),
        margin=dict(r=120, t=50, l=10, b=80),  # Spațiu pentru legendă și etichete
        barmode='stack'
    )
    
    fig.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='inside',
        insidetextanchor='middle'
    )
    
    # Adaugă nota explicativă jos
    fig.add_annotation(
        text="Note: 'Other' companies (outside top 5) are excluded - percentage shown in region label",
        xref="paper", yref="paper",
        x=0.5, y=-0.15,
        showarrow=False,
        font=dict(size=9, color="gray"),
        xanchor='center'
    )
    
    # Ajustează axa X pentru etichete pe două linii
    fig.update_xaxes(tickangle=0, tickfont=dict(size=10))
    
    return fig

# Tab 5 callbasks 
# Callback pentru Contract Types by Experience Level
@callback(
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
        contract_exp,
        x='Experience',
        y='count',
        color='JobType',
        title='',
        labels={'count': 'Jobs', 'Experience': 'Experience', 'JobType': 'Contract'},
        color_discrete_sequence=px.colors.qualitative.Set2,
        category_orders={'Experience': exp_order},
        barmode='stack'
    )
    fig.update_layout(
        height=450, 
        xaxis={'tickangle': 45},
        legend=dict(
            orientation='v',           # Verticală
            yanchor='top',             # Ancorat sus
            y=1,                       # Poziție sus
            xanchor='left',            # Ancorat stânga
            x=1.02,                    # În dreapta graficului
            title='Contract Type'
        ),
        margin=dict(r=150)             # Spațiu pentru legendă
    )
    return fig

# Callback pentru Work Types by Experience Level (sortat descrescător)
@callback(
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
    
    # Calculează totalul pe WorkType și sortează descrescător
    worktype_totals = worktype_exp.groupby('WorkType')['count'].sum().sort_values(ascending=False)
    sorted_worktypes = worktype_totals.index.tolist()
    
    top_worktypes = sorted_worktypes[:10]  # Top 10
    worktype_exp = worktype_exp[worktype_exp['WorkType'].isin(top_worktypes)]
    
    exp_order = ['Entry level', 'Associate', 'Mid-Senior level', 'Director', 'Executive', 'Internship']
    exp_order = [e for e in exp_order if e in worktype_exp['Experience'].unique()]
    
    fig = px.bar(
        worktype_exp,
        x='count',
        y='WorkType',
        color='Experience',
        orientation='h',
        title='',
        labels={'count': 'Jobs', 'WorkType': 'Work Type', 'Experience': 'Experience'},
        color_discrete_sequence=px.colors.qualitative.Set3,
        category_orders={'WorkType': sorted_worktypes, 'Experience': exp_order},
        barmode='stack'
    )
    fig.update_layout(
        height=450, 
        margin=dict(l=180), 
        legend=dict(orientation='h', yanchor='bottom', y=-0.15, xanchor='center', x=0.5)
    )
    return fig

# Callback pentru primul Sunburst (Experience → WorkType → JobType)
@callback(
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
        df_sunburst,
        path=['Experience', 'WorkType', 'JobType'],
        values='count',
        title='',
        color='count',
        color_continuous_scale='Viridis',
        hover_data={'count': ':,.0f'},
        labels={'count': 'Jobs'}  # ← Schimbă 'count' în 'Jobs'
    )
    
    # Actualizează titlul colorbar-ului
    fig.update_coloraxes(colorbar_title_text="Jobs")
    fig.update_layout(height=450, margin=dict(t=0, l=0, r=0, b=0))
    return fig

# Callback pentru Sankey - Top 5 Regiuni și Top 5 Orașe per Regiune
@callback(
    Output('career-sankey', 'figure'),
    Input('career-exp-filter', 'value')
)
def update_sankey(exp_level):
    filtered_df = df.copy()
    if exp_level and exp_level != 'all':
        filtered_df = filtered_df[filtered_df['Experience'] == exp_level]
    
    if filtered_df.empty:
        return go.Figure()
    
    # Nivel 1: Experience → Region
    exp_region = filtered_df.groupby(['Experience', 'region']).size().reset_index(name='count')
    
    # Nivel 2: Region → City
    region_city = filtered_df.groupby(['region', 'city']).size().reset_index(name='count')
    
    # Top 5 experiențe (sau toate dacă sunt mai puține)
    top_exp = filtered_df['Experience'].value_counts().head(6).index.tolist()
    
    # Top 5 regiuni
    top_regions = filtered_df['region'].value_counts().head(5).index.tolist()
    
    exp_region = exp_region[exp_region['Experience'].isin(top_exp)]
    exp_region = exp_region[exp_region['region'].isin(top_regions)]
    
    # Păstrăm doar regiunile din top 5
    region_city = region_city[region_city['region'].isin(top_regions)]
    
    # Pentru fiecare regiune, luăm top 5 orașe
    region_city = region_city.sort_values('count', ascending=False)
    region_city = region_city.groupby('region').head(5).reset_index(drop=True)
    
    # Creează nodurile
    exp_nodes = list(exp_region['Experience'].unique())
    region_nodes = list(exp_region['region'].unique())
    city_nodes = list(region_city['city'].unique())
    
    all_nodes = exp_nodes + region_nodes + city_nodes
    node_index = {node: i for i, node in enumerate(all_nodes)}
    
    # Creează legăturile
    sources = []
    targets = []
    values = []
    
    # Link-uri Experience → Region
    for _, row in exp_region.iterrows():
        sources.append(node_index[row['Experience']])
        targets.append(node_index[row['region']])
        values.append(int(row['count']))
    
    # Link-uri Region → City
    for _, row in region_city.iterrows():
        if row['region'] in node_index and row['city'] in node_index:
            sources.append(node_index[row['region']])
            targets.append(node_index[row['city']])
            values.append(int(row['count']))
    
    # Culori pentru noduri
    node_colors = (['#1f77b4'] * len(exp_nodes) +      # Albastru - Experience
                   ['#ff7f0e'] * len(region_nodes) +    # Portocaliu - Region
                   ['#2ca02c'] * len(city_nodes))       # Verde - City
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=15,
            line=dict(color="black", width=0.5),
            label=all_nodes,
            color=node_colors
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color='rgba(100, 100, 200, 0.4)'
        )
    )])
    
    # Adaugă titlu informativ
    num_regions = len(region_nodes)
    num_cities = len(city_nodes)
    
    fig.update_layout(
        title=dict(
            text=f"🌊 Experience → Region → City Flow (Top {num_regions} Regions, Top {num_cities} Cities)",
            x=0.5,
            font=dict(size=14)
        ),
        height=550,
        font=dict(size=9),
        margin=dict(t=50, l=20, r=20, b=20)
    )
    
    return fig

# Tab 6 callbasks
# Callback pentru Weekly Job Posting Trend (Last 6 Months)
@callback(
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
        jobtype_monthly,
        x='YearMonth',
        y='count',
        color='JobType',
        title='',
        labels={'YearMonth': '', 'count': 'Number of Jobs', 'JobType': 'Contract Type'},
        color_discrete_sequence=px.colors.qualitative.Set2,
        category_orders={'YearMonth': months_order},
        barmode='stack'
    )
    
    fig.update_layout(
        height=350,
        title_x=0.5,
        xaxis_title="",  # ← Eliminat titlul axei X
        yaxis_title="Number of Jobs",
        legend=dict(
            orientation='v',           # Verticală
            yanchor='top',             # Ancorat sus
            y=1,                       # Poziție sus
            xanchor='left',            # Ancorat stânga
            x=1.02,                    # În dreapta graficului
            title='Contract Type'
        ),
        margin=dict(r=120)             # Spațiu pentru legendă
    )
    
    return fig

@callback(
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
        weekly_trends,
        x='Date',
        y='Jobs',
        title='',
        labels={'Date': 'Week', 'Jobs': 'Jobs'},
        markers=True,
        color_discrete_sequence=['#1f77b4']
    )
    
    fig.update_layout(
        height=350,
        title_x=0.5,
        xaxis_title="Week",
        yaxis_title="Number of Jobs",
        hovermode='x unified'
    )
    
    fig.update_traces(marker=dict(size=4), line=dict(width=2))
    
    return fig

# Callback pentru Region Distribution (TOATE regiunile, fără limită)
@callback(
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
    
    # TOATE regiunile (fără head(10))
    region_counts = filtered_df['region'].value_counts().reset_index()
    region_counts.columns = ['region', 'count']
    region_counts = region_counts.sort_values('count', ascending=True)
    
    fig = px.bar(
        region_counts,
        x='count',
        y='region',
        orientation='h',
        color='count',
        color_continuous_scale='Teal',
        title='',
        labels={'count': 'Jobs', 'region': 'Region'}
    )
    
    fig.update_layout(
        height=450,
        title_x=0.5,
        xaxis_title="Number of Jobs",
        yaxis_title="Region",
        showlegend=False,
        margin=dict(l=180)
    )
    
    fig.update_coloraxes(showscale=False)
    
    return fig

@callback(
    Output('job-titles-chart', 'figure'),
    Input('dept-filter', 'value')
)
def update_job_titles(dept):
    if dept != 'all':
        filtered_df = df[df['Title'].str.contains(dept, case=False, na=False)]
    else:
        filtered_df = df
    
    titles = filtered_df['Title'].value_counts().head(15).reset_index()
    titles.columns = ['Title', 'count']
    
    fig = px.bar(
        titles,
        x='count',
        y='Title',
        orientation='h',
        color='count',
        color_continuous_scale='Blues',
        title=f'Top Job Titles{f" ({dept})" if dept != "all" else ""}',
        labels={'count': 'Number of Postings', 'Title': 'Job Title'}
    )
    
    fig.update_layout(height=500, title_x=0.5)
    return fig

@callback(
    Output('test-map-output', 'figure'),
    Input('exp-filter-map', 'value')
)
def test_map(exp_level):
    print(f"Callback triggered! exp_level = {exp_level}")
    
    if exp_level and exp_level != 'all':
        filtered_df = df[df['Experience'] == exp_level]
    else:
        filtered_df = df
    
    print(f"Filtered rows: {len(filtered_df)}")
    
    # Creează un grafic simplu
    region_counts = filtered_df['region'].value_counts().head(10).reset_index()
    region_counts.columns = ['region', 'count']
    
    fig = px.bar(
        region_counts,
        x='count',
        y='region',
        orientation='h',
        title=f'Jobs by Region (Experience: {exp_level})'
    )
    
    return fig


server = app.server # Necesar pentru gunicorn pe Render

if __name__ == '__main__':
    app.run(debug=True, dev_tools_ui=False, dev_tools_props_check=False)