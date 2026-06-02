import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def create_choropleth_map(df, region_counts):
    """Creează un bar chart pentru regiuni (în loc de hartă coropletă)"""
    if df.empty or region_counts.empty:
        return go.Figure()
    
    # Sortare descrescătoare
    region_counts = region_counts.sort_values('count', ascending=True).head(15)
    
    fig = px.bar(
        region_counts,
        x='count',
        y='region',
        orientation='h',
        color='count',
        color_continuous_scale='Blues',
        title='Job Distribution by Region',
        labels={'count': 'Number of Jobs', 'region': 'Region'}
    )
    
    fig.update_layout(
        height=500,
        title_x=0.5,
        xaxis_title="Number of Jobs",
        yaxis_title="Region",
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig

def create_bubble_map(df, city_counts):
    """Creează o hartă cu bule pentru orașe"""
    if df.empty or city_counts.empty:
        return go.Figure()
    
    # Coordonate aproximative pentru orașele din Germania
    city_coords = {
        'Berlin': (52.5200, 13.4050),
        'Hamburg': (53.5511, 9.9937),
        'Munich': (48.1351, 11.5820),
        'Cologne': (50.9375, 6.9603),
        'Frankfurt': (50.1109, 8.6821),
        'Stuttgart': (48.7758, 9.1829),
        'Düsseldorf': (51.2277, 6.7735),
        'Leipzig': (51.3397, 12.3731),
        'Dortmund': (51.5136, 7.4653),
        'Essen': (51.4556, 7.0116),
        'Bremen': (53.0793, 8.8017),
        'Dresden': (51.0504, 13.7373),
        'Hannover': (52.3759, 9.7320),
        'Nuremberg': (49.4521, 11.0767),
        'Duisburg': (51.4344, 6.7623),
        'Bochum': (51.4818, 7.2165),
        'Wuppertal': (51.2562, 7.1508),
        'Bielefeld': (52.0302, 8.5325),
        'Bonn': (50.7374, 7.0982),
        'Mannheim': (49.4875, 8.4660)
    }
    
    # Adaugă coordonate pentru orașele din date
    city_counts['lat'] = city_counts['city'].apply(
        lambda x: city_coords.get(x, (51.1657, 10.4515))[0]
    )
    city_counts['lon'] = city_counts['city'].apply(
        lambda x: city_coords.get(x, (51.1657, 10.4515))[1]
    )
    
    # Scalează dimensiunea bulelor
    max_count = city_counts['count'].max()
    city_counts['scaled_size'] = 20 + (city_counts['count'] / max_count) * 80
    
    fig = px.scatter_mapbox(
        city_counts,
        lat='lat',
        lon='lon',
        size='scaled_size',
        color='count',
        hover_name='city',
        text='city',
        title='Top 20 E-Commerce Hubs in Germany',
        color_continuous_scale='Viridis',
        size_max=60,
        zoom=5,
        center={"lat": 51.1657, "lon": 10.4515},
        labels={'count': 'Number of Jobs', 'city': 'City'},
        height=600
    )
    
    fig.update_layout(
        mapbox_style="carto-positron",  # Stil mai stabil
        title_x=0.5,
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        autosize=True,
        dragmode='pan'  # Permite panning
    )
    
    fig.update_traces(
        textposition='top center',
        textfont=dict(size=11, color='black', family='Arial')
    )
    
    return fig