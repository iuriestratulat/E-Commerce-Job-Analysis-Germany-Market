# tab_content.py - Contains visual layout components for the dashboard
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd

def get_responsive_navbar():
    """
    Creates a dual-bar navigation system:
    1. A top header bar exclusively for the dashboard title.
    2. A secondary navigation bar for the tabs, aligned to the left and 
       collapsible into a hamburger menu on mobile.
    """
    return html.Div([
        # BRAND HEADER BAR (Top Bar - Title Only)
        html.Div(
            dbc.Container(
                html.H1("E-commerce Job Market Analysis - Germany, November 2025", className="text-white fw-bold fs-4 m-0 py-2 text-center text-md-start"),
                fluid=True
            ),
            className="bg-primary border-bottom border-light border-opacity-10 py-1"
        ),
        
        # NAVIGATION TABS BAR (Bottom Bar - Tabs Menu)
        dbc.Navbar(
            dbc.Container([
                # 📱 Text label visible ONLY on mobile to fill the empty space on the left
                html.Span(
                    "📊 Select Analysis Tab", 
                    className="text-white fw-medium d-block d-md-none ps-2"
                ),
                
                # The Hamburger Button for mobile
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0, className="border-light"),
                
                # Collapsible Tabs Menu (Aligned to the left on desktop)
                dbc.Collapse(
                    dbc.Nav([
                        dbc.NavItem(dbc.NavLink("📊 Overview", href="#", id="tab-overview-link", active=True, className="text-white px-3 nav-link-custom")),
                        dbc.NavItem(dbc.NavLink("🗺️ Geographic Analysis", href="#", id="tab-geo-link", className="text-white px-3 nav-link-custom")),
                        dbc.NavItem(dbc.NavLink("🔧 Skills Analysis", href="#", id="tab-skills-link", className="text-white px-3 nav-link-custom")),
                        dbc.NavItem(dbc.NavLink("💼 Job Distribution", href="#", id="tab-jobs-link", className="text-white px-3 nav-link-custom")),
                        dbc.NavItem(dbc.NavLink("🎯 Career Progression", href="#", id="tab-career-link", className="text-white px-3 nav-link-custom")),
                        dbc.NavItem(dbc.NavLink("📈 Temporal Analysis", href="#", id="tab-temporal-link", className="text-white px-3 nav-link-custom")),
                        dbc.NavItem(dbc.NavLink("🎓 Conclusions", href="#", id="tab-conclusions-link", className="text-white px-3 nav-link-custom")),
                    ], 
                    className="me-auto justify-content-start flex-column flex-md-row w-100", 
                    navbar=True),
                    id="navbar-collapse",
                    navbar=True,
                    is_open=False
                ),
            ], fluid=True),
            color="primary",
            dark=True,
            className="mb-4 rounded-bottom shadow-sm py-1",
        )
    ])

def render_overview_tab(df, top_city, top_city_count, top_skill, top_job, 
                        skills_df, create_skills_bar_chart, create_contract_type_chart, 
                        create_top_companies_chart, create_job_source_chart):
    """Generates the content for the Overview tab with responsive KPI cards."""
    return html.Div([
        # 📱 Responsive Alert Note for Mobile Users
        dbc.Alert(
            [
                html.I(className="bi bi-info-circle-fill me-2"),
                "📱 The app works on all devices. If you access it from your phone, ",
                html.Strong("rotate the device (Landscape)"),
                " for better visibility of the charts."
            ],
            color="info",
            className="d-block d-md-none text-center mb-3 shadow-sm py-2 px-3 fw-medium rounded",
        ),

        # KPI Summary Cards (xs=12 makes them stack on mobile, md=3 places them side by side)
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H6("Total Jobs Analyzed", className="card-title text-muted fs-7 mb-1"),
                    html.H3(f"{len(df):,}", className="card-text fw-bold text-primary")
                ])
            ], className="mb-3 border-0 shadow-sm rounded"), xs=12, md=3),
            
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H6("Time Period", className="card-title text-muted fs-7 mb-1"),
                    html.H3("Last 6 Months", className="card-text fw-bold text-success")
                ])
            ], className="mb-3 border-0 shadow-sm rounded"), xs=12, md=3),
            
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H6("Top City", className="card-title text-muted fs-7 mb-1"),
                    html.H3(top_city, className="card-text fw-bold text-info text-truncate")
                ])
            ], className="mb-3 border-0 shadow-sm rounded"), xs=12, md=3),
            
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H6("Top Skill", className="card-title text-muted fs-7 mb-1"),
                    html.H3(top_skill, className="card-text fw-bold text-warning text-truncate")
                ])
            ], className="mb-3 border-0 shadow-sm rounded"), xs=12, md=3),
        ], className="mb-2"),

        # Row 1: Charts
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("💡 Market Overview", className="fw-bold fs-6 text-dark bg-transparent border-0 pt-3 pb-0"),
                dbc.CardBody(dcc.Graph(figure=create_skills_bar_chart(skills_df), config={'displayModeBar': False}))
            ], className="mb-4 border-0 shadow-sm rounded"), xs=12, md=6),
            
            dbc.Col(dbc.Card([
                dbc.CardHeader("📊 Contract Types", className="fw-bold fs-6 text-dark bg-transparent border-0 pt-3 pb-0"),
                dbc.CardBody(dcc.Graph(figure=create_contract_type_chart(df), config={'displayModeBar': False}))
            ], className="mb-4 border-0 shadow-sm rounded"), xs=12, md=6),
        ]),

        # Row 2: Charts
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("🏢 Top Companies", className="fw-bold fs-6 text-dark bg-transparent border-0 pt-3 pb-0"),
                dbc.CardBody(dcc.Graph(figure=create_top_companies_chart(df), config={'displayModeBar': False}))
            ], className="mb-4 border-0 shadow-sm rounded"), xs=12, md=6),
            
            dbc.Col(dbc.Card([
                dbc.CardHeader("🔌 Job Sources", className="fw-bold fs-6 text-dark bg-transparent border-0 pt-3 pb-0"),
                dbc.CardBody(dcc.Graph(figure=create_job_source_chart(df), config={'displayModeBar': False}))
            ], className="mb-4 border-0 shadow-sm rounded"), xs=12, md=6),
        ]),
    ])

def render_geographic_tab(df):
    """
    Generates the HTML layout for the Geographic Analysis Tab with adaptive filters.
    """
    return html.Div([
        # Row 1: Filters (Stack on mobile, side-by-side on desktop)
        dbc.Row([
            dbc.Col([
                html.Label("Filter by Experience Level:", className="fw-bold mb-1"),
                dcc.Dropdown(
                    id='exp-filter-map',
                    options=[{'label': 'All', 'value': 'all'}] + 
                            [{'label': str(l), 'value': str(l)} for l in df['Experience'].unique() if pd.notna(l)],
                    value='all',
                    clearable=False
                )
            ], xs=12, md=6, className="mb-3"),
            
            dbc.Col([
                html.Label("Filter by Contract Type:", className="fw-bold mb-1"),
                dcc.Dropdown(
                    id='contract-filter-map',
                    options=[{'label': 'All', 'value': 'all'}] + 
                            [{'label': str(l), 'value': str(l)} for l in df['JobType'].unique() if pd.notna(l)],
                    value='all',
                    clearable=False
                )
            ], xs=12, md=6, className="mb-3"),
        ], className="mb-4"),
        
        # Row 2: Charts
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H4(id='region-chart-title', className="text-center mb-0 fs-5")),
                    dbc.CardBody([
                        dcc.Graph(id='choropleth-map', style={'height': '400px'}, config={'responsive': True})
                    ])
                ], className="shadow-sm h-100 mb-3")
            ], xs=12, md=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H4(id='bubble-map-title', className="text-center mb-0 fs-5")),
                    dbc.CardBody([
                        dcc.Graph(id='bubble-map', style={'height': '400px'}, config={'responsive': True})
                    ])
                ], className="shadow-sm h-100 mb-3")
            ], xs=12, md=6),
        ], className="g-3"),
    ])

def render_skills_tab(df):
    """
    Generates the HTML layout for the Skills Analysis Tab.
    All components collapse cleanly into a single column on mobile screens.
    """
    return html.Div([
        # Row 1: Filter Experience Level
        dbc.Row([
            dbc.Col([
                html.Label("Filter by Experience Level:", className="fw-bold mb-1"),
                dcc.Dropdown(
                    id='skills-exp-filter',
                    options=[{'label': 'All', 'value': 'all'}] + 
                            [{'label': str(l), 'value': str(l)} for l in df['Experience'].unique() if pd.notna(l)],
                    value='all',
                    clearable=False
                )
            ], xs=12, md=4, className="mb-3"),
        ], className="mb-4"),
        
        # Row 2: Top 15 Skills + Treemap
        dbc.Row([
            # Column 1: Top 15 Skills Bar Chart
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H4(id='skills-bar-title', className="text-center mb-0 fs-5")),
                    dbc.CardBody([
                        dcc.Graph(id='skills-bar-chart', style={'height': '400px'}, config={'responsive': True})
                    ])
                ], className="shadow-sm h-100 mb-3")
            ], xs=12, md=6),
            
            # Column 2: Treemap
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H4("🌳 Skills Treemap", className="text-center mb-0 fs-5")),
                    dbc.CardBody([
                        dcc.Graph(id='word-cloud-plot', style={'height': '400px'}, config={'responsive': True})
                    ])
                ], className="shadow-sm h-100 mb-3")
            ], xs=12, md=6),
        ], className="g-3 mb-4"),
        
        # Row 3: Skills Distribution by Region (Heatmap)
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H4("🔥 Skills Distribution by Region", className="text-center mb-0 fs-5")),
                    dbc.CardBody([
                        dcc.Graph(id='skills-heatmap', style={'height': '500px'}, config={'responsive': True})
                    ])
                ], className="shadow-sm")
            ], xs=12, width=12)
        ])
    ])

def render_job_distribution_tab(df):
    """
    Generates the HTML layout for the Job Distribution Tab (2x2 Grid).
    Uses clean Bootstrap classes to stack layouts responsively on mobile.
    """
    return html.Div([
        # Row 1: Experience Level + Contract Type
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.Div([
                            html.H4("📈 Job Distribution by Experience Level", className="mb-0 d-inline fs-5"),
                            html.Span(" ⓘ", id="experience-info-tooltip", style={"cursor": "pointer", "color": "#17a2b8", "fontWeight": "bold"})
                        ], className="text-center"),
                        dbc.Tooltip(
                            "📌 Level Descriptions:\n\n• Entry level: Beginners.\n• Mid-Senior level: Autonomous experience.\n• Associate: 2-4 years.\n• Internship: Trainees.\n• Director/Executive: Leadership.\n• N/A: Not specified.",
                            target="experience-info-tooltip", placement="top", style={"whiteSpace": "pre-line"}
                        )
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='experience-level-chart', style={'height': '400px'}, config={'responsive': True})
                    ])
                ], className="shadow-sm h-100 mb-3")
            ], xs=12, md=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.Div([
                            html.H4("📝 Job Distribution by Contract Type", className="mb-0 d-inline fs-5"),
                            html.Span(" ⓘ", id="contract-info-tooltip", style={"cursor": "pointer", "color": "#17a2b8", "fontWeight": "bold"})
                        ], className="text-center"),
                        dbc.Tooltip(
                            "📌 Type Descriptions:\n\n• Full-time: ~40h/week.\n• Part-time: Fewer hours.\n• Contract: Temporary project.\n• Internship: Trainees.",
                            target="contract-info-tooltip", placement="top", style={"whiteSpace": "pre-line"}
                        )
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='contract-type-chart', style={'height': '400px'}, config={'responsive': True})
                    ])
                ], className="shadow-sm h-100 mb-3")
            ], xs=12, md=6),
        ], className="g-3 mb-3"),
        
        # Row 2: Work Type + Company Market Share
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.Div([
                            html.H4("💼 Top 15 Job Distribution by Work Type", className="mb-0 d-inline fs-5"),
                            html.Span(" ⓘ", id="worktype-info-tooltip", style={"cursor": "pointer", "color": "#17a2b8", "fontWeight": "bold"})
                        ], className="text-center"),
                        dbc.Tooltip(
                            "📌 Work Type Sectors:\n\n• Represents the functional area (Marketing, IT, Sales).\n• Shows top 15 combinations.",
                            target="worktype-info-tooltip", placement="top", style={"whiteSpace": "pre-line"}
                        )
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='work-type-chart', style={'height': '400px'}, config={'responsive': True})
                    ])
                ], className="shadow-sm h-100 mb-3")
            ], xs=12, md=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.Div([
                            html.H4("🏢 Top 5 Company Market Share", className="mb-0 d-inline fs-5"),
                            html.Span(" ⓘ", id="company-info-tooltip", style={"cursor": "pointer", "color": "#17a2b8", "fontWeight": "bold"})
                        ], className="text-center"),
                        dbc.Tooltip(
                            "📌 Market Share Explanation:\n\n• Top 5 companies across top 5 regions.\n• Percentage in labels shows 'Other' companies.",
                            target="company-info-tooltip", placement="top", style={"whiteSpace": "pre-line"}
                        )
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='company-market-share', style={'height': '400px'}, config={'responsive': True})
                    ])
                ], className="shadow-sm h-100 mb-3")
            ], xs=12, md=6),
        ], className="g-3"),
    ])

def render_career_tab(df):
    """
    Generates the HTML layout for the Career Progression Tab.
    Includes advanced visualizations like Sunburst and Sankey diagrams,
    re-arranged to stack vertically on mobile screens.
    """
    return html.Div([
        # Row 1: Filter Experience Level
        dbc.Row([
            dbc.Col([
                html.Label("Filter by Experience Level:", className="fw-bold mb-1"),
                dcc.Dropdown(
                    id='career-exp-filter',
                    options=[{'label': 'All', 'value': 'all'}] + 
                            [{'label': str(l), 'value': str(l)} for l in df['Experience'].unique() if pd.notna(l)],
                    value='all',
                    clearable=False
                )
            ], xs=12, md=4, className="mb-3"),
        ], className="mb-4"),
        
        # Row 2: Contract Types + Decomposition Tree (Sunburst)
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H4("📊 Contract Types by Experience Level", className="text-center mb-0 fs-5")),
                    dbc.CardBody([
                        dcc.Graph(id='career-contract-chart', style={'height': '400px'}, config={'responsive': True})
                    ])
                ], className="shadow-sm h-100 mb-3")
            ], xs=12, md=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.Div([
                            html.H4("🌲 Decomposition Tree: Experience → Work Type → Contract", className="text-center mb-0 d-inline fs-5"),
                            html.Span(" ⓘ", id="sunburst-tooltip", style={"cursor": "pointer", "color": "#17a2b8", "fontWeight": "bold"})
                        ], className="text-center"),
                        dbc.Tooltip(
                            "📌 How to read:\n\n• Inner ring: Experience Level\n• Middle ring: Work Type\n• Outer ring: Contract Type\n• Click a segment to zoom.",
                            target="sunburst-tooltip", placement="top"
                        )
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='career-sunburst', style={'height': '400px'}, config={'responsive': True})
                    ])
                ], className="shadow-sm h-100 mb-3")
            ], xs=12, md=6),
        ], className="g-3 mb-4"),
        
        # Row 3: Work Types + Sankey Diagram
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H4("📊 Work Types by Experience Level", className="text-center mb-0 fs-5")),
                    dbc.CardBody([
                        dcc.Graph(id='career-worktype-stacked', style={'height': '400px'}, config={'responsive': True})
                    ])
                ], className="shadow-sm h-100 mb-3")
            ], xs=12, md=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.Div([
                            html.H4("🌊 Sankey Diagram: Experience → Region → City", className="text-center mb-0 d-inline fs-5"),
                            html.Span(" ⓘ", id="sankey-tooltip", style={"cursor": "pointer", "color": "#17a2b8", "fontWeight": "bold"})
                        ], className="text-center"),
                        dbc.Tooltip(
                            "📌 How to read:\n\n• Left: Experience | Middle: Region | Right: City\n• Thicker lines = more job postings.",
                            target="sankey-tooltip", placement="top"
                        )
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='career-sankey', style={'height': '450px'}, config={'responsive': True})
                    ])
                ], className="shadow-sm h-100 mb-3")
            ], xs=12, md=6),
        ], className="g-3"),
    ])

def render_temporal_analysis_tab(df):
    """
    Generates the HTML layout for the Temporal Analysis Tab.
    Guarantees fluid row wraps on mobile phone views.
    """
    return html.Div([
        # Row 1: Filters
        dbc.Row([
            dbc.Col([
                html.Label("Select Month:", className="fw-bold mb-1"),
                dcc.Dropdown(
                    id='trends-month-filter',
                    options=[{'label': 'All Months', 'value': 'all'}] +
                            [{'label': month, 'value': month} for month in sorted(df['YearMonth'].unique())],
                    value='all',
                    clearable=False
                )
            ], xs=12, md=6, className="mb-3"),
            
            dbc.Col([
                html.Label("Filter by Experience Level:", className="fw-bold mb-1"),
                dcc.Dropdown(
                    id='trends-exp-filter',
                    options=[{'label': 'All', 'value': 'all'}] + 
                            [{'label': str(l), 'value': str(l)} for l in df['Experience'].unique() if pd.notna(l)],
                    value='all',
                    clearable=False
                )
            ], xs=12, md=6, className="mb-3"),
        ], className="mb-4"),
        
        # Row 2: Weekly Job Posting Trend (Full width)
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H4("📅 Weekly Job Posting Trend (Last 6 Months)", className="text-center mb-0 fs-5")),
                    dbc.CardBody([
                        dcc.Graph(id='trends-line-chart', style={'height': '350px'}, config={'responsive': True})
                    ])
                ], className="shadow-sm mb-4")
            ], xs=12)
        ]),
        
        # Row 3: Job Type Stacked + Region Bar
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H4("📊 Job Type Distribution by Month", className="text-center mb-0 fs-5")),
                    dbc.CardBody([
                        dcc.Graph(id='trends-jobtype-stacked', style={'height': '400px'}, config={'responsive': True})
                    ])
                ], className="shadow-sm h-100 mb-3")
            ], xs=12, md=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H4("📍 Job Distribution by Region", className="text-center mb-0 fs-5")),
                    dbc.CardBody([
                        dcc.Graph(id='trends-region-chart', style={'height': '400px'}, config={'responsive': True})
                    ])
                ], className="shadow-sm h-100 mb-3")
            ], xs=12, md=6),
        ], className="g-3"),
    ])

def render_conclusions_tab(total_jobs, top_city, top_city_count, top_skill):
    """
    Generates the HTML layout for the Conclusions Tab.
    All parameters are dynamically passed to avoid data processing inside the layout.
    """
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.H3("E-Commerce Job Market Analysis - Key Takeaways for Graduates", className="text-center mb-4 text-primary fs-4"),
                html.Hr(),
            ], xs=12),
        ]),
        
        # Row 1: Market Overview
        dbc.Row([
            dbc.Col([
                html.H4("📊 Market Overview", className="mt-2 mb-3 fs-5 text-dark fw-bold"),
                html.P([
                    "The E-Commerce job market in Germany shows a ", 
                    html.Strong("robust and growing ecosystem"), 
                    f", with a total of ", html.Strong(f"{total_jobs:,} jobs"), 
                    " posted in the last 6 months."
                ]),
                html.Ul([
                    html.Li([html.Strong(f"{top_city}"), f" is the undisputed hub ({top_city_count} jobs, {top_city_count/total_jobs*100:.1f}% of total)"]),
                    html.Li("The market is concentrated in western and southern Germany (Berlin, Hamburg, Munich, Cologne, Frankfurt)"),
                    html.Li("Eastern regions (Saxony, Brandenburg) offer fewer opportunities but are developing"),
                ]),
            ], xs=12),
        ], className="mb-4"),
        
        # Row 2: Essential Skills + Languages
        dbc.Row([
            dbc.Col([
                html.H4("🔧 Essential Skills for Success", className="mb-3 fs-5 text-dark fw-bold"),
                html.P("Most sought-after competencies in the current market:"),
                html.Ol([
                    html.Li([html.Strong("Digital Marketing"), " - most demanded skill (over 15% of jobs)"]),
                    html.Li([html.Strong("E-Commerce"), " - fundamental for the industry"]),
                    html.Li([html.Strong("Analytics / Google Analytics"), " - data-driven decisions are essential"]),
                    html.Li([html.Strong("SEO / SEM"), " - online visibility is key to success"]),
                    html.Li([html.Strong("IT / Technical Skills"), " - key differentiator for advancement"]),
                ]),
            ], xs=12, md=6, className="mb-4"),
            
            dbc.Col([
                html.H4("🌍 Language Requirements", className="mb-3 fs-5 text-dark fw-bold"),
                html.P("Bilingualism is a major advantage in the German market:"),
                html.Ul([
                    html.Li([html.Strong("English"), " - mandatory for most jobs (85%+ of postings)"]),
                    html.Li([html.Strong("German"), " - required for local roles (60%+ of postings)"]),
                    html.Li("Bilingual candidates have a significant competitive advantage"),
                    html.Li("Startups and international companies are more flexible with language"),
                ]),
            ], xs=12, md=6, className="mb-4"),
        ]),
        
        # Row 3: Contract & Experience + Hiring Hubs
        dbc.Row([
            dbc.Col([
                html.H4("📝 Contract & Experience Distribution", className="mb-3 fs-5 text-dark fw-bold"),
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
            ], xs=12, md=6, className="mb-4"),
            
            dbc.Col([
                html.H4("🏢 Top Hiring Hubs", className="mb-3 fs-5 text-dark fw-bold"),
                html.P("Most active regions for E-Commerce jobs:"),
                html.Ul([
                    html.Li([html.Strong("Berlin"), " - #1 hub (391 jobs)"]),
                    html.Li([html.Strong("Hamburg & Munich"), " - tier 2, dozens of opportunities"]),
                    html.Li([html.Strong("North Rhine-Westphalia"), " - multiple cities (Cologne, Düsseldorf, Dortmund)"]),
                    html.Li("Frankfurt (Hesse) - financial and growing e-commerce hub"),
                ]),
            ], xs=12, md=6, className="mb-4"),
        ]),
        
        # Row 4: Target Roles + Salary Progression
        dbc.Row([
            dbc.Col([
                html.H4("💼 Target Roles Validated for Graduates", className="mb-3 fs-5 text-dark fw-bold"),
                html.P("Most accessible and promising roles for graduates:"),
                html.Ul([
                    html.Li([html.Strong("Online Marketing Manager (m/w/d)"), " - most frequent entry-level role"]),
                    html.Li([html.Strong("E-Commerce Specialist / Manager"), " - rapid growth potential"]),
                    html.Li([html.Strong("Digital Marketing Manager"), " - marketing+tech combination"]),
                    html.Li([html.Strong("Sales Specialist / Category Manager"), " - commercial roles"]),
                ]),
            ], xs=12, md=6, className="mb-4"),
            
            dbc.Col([
                html.H4("💰 Career Progression & Salary", className="mb-3 fs-5 text-dark fw-bold"),
                html.P("Estimated salary progression (E-Commerce track):"),
                html.Ul([
                    html.Li([html.Strong("Entry Level"), ": €38K - €48K"]),
                    html.Li([html.Strong("Junior"), ": €48K - €55K"]),
                    html.Li([html.Strong("Mid-Level"), ": €55K - €70K"]),
                    html.Li([html.Strong("Senior"), ": €70K - €90K+"]),
                    html.Li([html.Strong("Lead/Manager"), ": €90K - €120K+"]),
                ]),
            ], xs=12, md=6, className="mb-4"),
        ]),
        
        # Row 5: Final Recommendations
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H4("🎯 Final Recommendations for Graduates", className="text-center mb-0 fs-5")),
                    dbc.CardBody([
                        html.H5("📌 To enter the market:", className="mt-2 fs-6 fw-bold"),
                        html.Ol([
                            html.Li([html.Strong("Invest in Digital Marketing and Google Analytics skills")]),
                            html.Li([html.Strong("Learn E-Commerce fundamentals"), " (platforms, logistics, customer journey)"]),
                            html.Li([html.Strong("German language"), " is a major differentiator - start courses ASAP"]),
                            html.Li("Build a portfolio with practical projects (Google Analytics certified, etc.)"),
                        ]),
                        html.H5("📌 Professional development:", className="mt-3 fs-6 fw-bold"),
                        html.Ol([
                            html.Li([html.Strong("Start as a Junior E-Commerce Manager"), " or ", html.Strong("Online Marketing Specialist")]),
                            html.Li([html.Strong("After 2-3 years, advance to Mid-Level with €55K+")]),
                            html.Li("Specialize in a niche (SEO, Analytics, Marketplace Management)"),
                        ]),
                        html.H5("📌 Market Outlook:", className="mt-3 fs-6 fw-bold"),
                        html.P([
                            "The German E-Commerce market shows ", html.Strong("strong growth"), 
                            " with increasing demand for hybrid skills combining marketing, technology, and data analytics. ",
                            "Graduates who invest in ", html.Strong("digital skills + German language"), 
                            " have the highest chances of quick employment and career advancement."
                        ]),
                    ])
                ], className="shadow-sm border-primary mb-3")
            ], xs=12)
        ], className="mt-2"),
    ])




