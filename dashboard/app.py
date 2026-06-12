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
                         prepare_region_data, prepare_city_data, prepare_dashboard_data)

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
from tab_content import (
    get_responsive_navbar, 
    render_overview_tab, 
    render_geographic_tab, 
    render_skills_tab, 
    render_job_distribution_tab,
    render_career_tab,
    render_temporal_analysis_tab,
    render_conclusions_tab
)
from callbacks.job_callbacks import register_job_callbacks
from callbacks.geographic_callbacks import register_geographic_callbacks
from callbacks.skills_callbacks import register_skills_callbacks
from callbacks.career_callbacks import register_career_callbacks
from callbacks.temporal_callbacks import register_temporal_callbacks

# Inițializare aplicație
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                assets_folder='assets')

# Încărcare și pregătire centralizată a datelor (Unpacking variables safely)
raw_df = load_data()
df, city_counts, skills_df, top_city, top_city_count, top_skill, top_job = prepare_dashboard_data(raw_df)

# Fallback block in case the initial setup encountered issues (ensures app doesn't crash)
if df.empty:
    city_counts = pd.DataFrame()
    skills_df = pd.DataFrame()
    print("ATENȚIE: Nu s-au putut încărca sau procesa datele corect!")

# DEBUG: Check and safely generate dropdown options, filtering out null values
print("=== DROPDOWN OPTIONS ===")
experience_options = [{'label': 'All', 'value': 'all'}] + [{'label': str(l), 'value': str(l)} for l in df['Experience'].unique() if pd.notna(l)]
print("Experience options:", experience_options)

# Layout-ul principal simplificat la maxim
app.layout = dbc.Container([
    # Meniu de navigare responsiv (Hamburger pe mobil, Tab-uri pe desktop)
    get_responsive_navbar(),
    
    # Containerul unde se vor încărca dinamic tab-urile
    html.Div(id="tab-content", className="mt-4"),
    
    # Footer global fixat pe pagină
    dbc.Row([
        dbc.Col(html.Hr(), width=12),
        dbc.Col(html.P("Data source: LinkedIn, Glassdoor, Stepstone | Analysis based on 1,581 job postings | Dashboard built with Plotly Dash", 
                       className="text-center text-muted small"), width=12),
    ], className="mt-4 pb-3"),
], fluid=True)

# Callback to handle main tab switching and multi-tab rendering
@app.callback(
    [Output("tab-content", "children"),
     Output("tab-overview-link", "active"),
     Output("tab-geo-link", "active"),
     Output("tab-skills-link", "active"),
     Output("tab-jobs-link", "active"),
     Output("tab-career-link", "active"),
     Output("tab-temporal-link", "active"),
     Output("tab-conclusions-link", "active")],
    [Input("tab-overview-link", "n_clicks"),
     Input("tab-geo-link", "n_clicks"),
     Input("tab-skills-link", "n_clicks"),
     Input("tab-jobs-link", "n_clicks"),
     Input("tab-career-link", "n_clicks"),
     Input("tab-temporal-link", "n_clicks"),
     Input("tab-conclusions-link", "n_clicks")]
)
def display_tab_content(*args):
    ctx = dash.callback_context

    # Default states for active links
    active_states = [False] * 7

    # If no tab was clicked yet, default to Overview (index 0)
    if not ctx.triggered:
        active_states[0] = True
        return render_overview_tab(
            df, top_city, top_city_count, top_skill, top_job, 
            skills_df, create_skills_bar_chart, create_contract_type_chart, 
            create_top_companies_chart, create_job_source_chart
        ), *active_states

    # Identify which tab link triggered the callback
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "tab-overview-link":
        active_states[0] = True
        content = render_overview_tab(
            df, top_city, top_city_count, top_skill, top_job, 
            skills_df, create_skills_bar_chart, create_contract_type_chart, 
            create_top_companies_chart, create_job_source_chart
        )
    elif button_id == "tab-geo-link":
        active_states[1] = True
        content = render_geographic_tab(df)
    elif button_id == "tab-skills-link":
        active_states[2] = True
        content = render_skills_tab(df)
    elif button_id == "tab-jobs-link":
        active_states[3] = True
        content = render_job_distribution_tab(df)
    elif button_id == "tab-career-link":
        active_states[4] = True
        content = render_career_tab(df)
    elif button_id == "tab-temporal-link":
        active_states[5] = True
        content = render_temporal_analysis_tab(df)
    elif button_id == "tab-conclusions-link":
        active_states[6] = True
        content = render_conclusions_tab(len(df), top_city, top_city_count, top_skill)
    else:
        active_states[0] = True
        content = html.Div("Tab not found.")

    return content, *active_states

# Callback to toggle the hamburger menu collapse on mobile screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

server = app.server # Necesar pentru gunicorn pe Render
register_job_callbacks(app, df)
register_geographic_callbacks(app, df)
register_skills_callbacks(app, df)
register_career_callbacks(app, df)
register_temporal_callbacks(app, df)

if __name__ == '__main__':
    app.run(debug=True, dev_tools_ui=False, dev_tools_props_check=False)