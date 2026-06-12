# geographic_callbacks.py - Modular callback functions for Geographic Analysis tab
from dash import Output, Input
import plotly.express as px
import pandas as pd
import json
import os

def register_geographic_callbacks(app, df):
    """
    Registers callbacks for the Geographic Analysis tab,
    handling the region bar chart and the scatter mapbox bubble map.
    """
    
    # 1. Callback for Region Bar Chart
    @app.callback(
        [Output('choropleth-map', 'figure'),
         Output('region-chart-title', 'children')],
        [Input('exp-filter-map', 'value'),
         Input('contract-filter-map', 'value')]
    )
    def update_region_chart(exp_level, contract_type):
        filtered_df = df.copy()
        
        if exp_level and exp_level != 'all':
            filtered_df = filtered_df[filtered_df['Experience'] == exp_level]
        
        if contract_type and contract_type != 'all':
            filtered_df = filtered_df[filtered_df['JobType'] == contract_type]
        
        region_counts = filtered_df['region'].value_counts().head(15).reset_index()
        region_counts.columns = ['region', 'count']
        region_counts = region_counts.sort_values('count', ascending=True)
        
        num_regions = len(region_counts)
        if num_regions == 0:
            title_text = "📊 No Regions Found"
        elif num_regions == 1:
            title_text = f"📊 Job Distribution by Region ({num_regions} region)"
        else:
            title_text = f"📊 Job Distribution by Region ({num_regions} regions)"
        
        fig = px.bar(
            region_counts, x='count', y='region', orientation='h',
            color='count', color_continuous_scale='Blues', title='',
            labels={'count': 'Jobs', 'region': 'Region'}
        )
        
        fig.update_layout(
            height=400, title_x=0.5, xaxis_title="Jobs",
            yaxis_title="Region", showlegend=False
        )
        fig.update_coloraxes(showscale=False)
        
        return fig, title_text

    # 2. Callback for Scatter Mapbox (Bubble Map)
    @app.callback(
        [Output('bubble-map', 'figure'),
         Output('bubble-map-title', 'children')],
        [Input('exp-filter-map', 'value'),
         Input('contract-filter-map', 'value')]
    )
    def update_bubble_map(exp_level, contract_type):
        filtered_df = df.copy()
        
        if exp_level and exp_level != 'all':
            filtered_df = filtered_df[filtered_df['Experience'] == exp_level]
        
        if contract_type and contract_type != 'all':
            filtered_df = filtered_df[filtered_df['JobType'] == contract_type]
        
        # Safe path handling for coordinates JSON
        coords_path = os.path.join('data', 'city_coordinates.json')
        try:
            with open(coords_path, 'r', encoding='utf-8') as f:
                city_coords = json.load(f)
        except FileNotFoundError:
            print(f"ERROR: {coords_path} not found!")
            city_coords = {}
        
        city_counts = filtered_df['city'].value_counts().head(30).reset_index()
        city_counts.columns = ['city', 'count']
        city_counts = city_counts[city_counts['city'].isin(city_coords.keys())]
        
        city_counts['lat'] = city_counts['city'].apply(lambda x: city_coords.get(x, [51.1657, 10.4515])[0])
        city_counts['lon'] = city_counts['city'].apply(lambda x: city_coords.get(x, [51.1657, 10.4515])[1])
        
        num_cities = len(city_counts)
        if num_cities == 0:
            title_text = "📍 No E-Commerce Hubs Found"
        elif num_cities == 1:
            title_text = f"📍 {num_cities} E-Commerce Hub in Germany"
        else:
            title_text = f"📍 Top {num_cities} E-Commerce Hubs in Germany"
        
        fig = px.scatter_mapbox(
            city_counts, lat='lat', lon='lon', size='count', color='count',
            hover_name='city', title='', color_continuous_scale='Viridis',
            size_max=40, zoom=5, center={"lat": 51.1657, "lon": 10.4515},
            height=400, labels={'count': 'Jobs'}
        )
        
        fig.update_layout(
            mapbox_style="carto-positron", title_x=0.5,
            margin={"r": 0, "t": 0, "l": 0, "b": 0}
        )
        fig.update_coloraxes(colorbar_title_text="Jobs")
        
        return fig, title_text