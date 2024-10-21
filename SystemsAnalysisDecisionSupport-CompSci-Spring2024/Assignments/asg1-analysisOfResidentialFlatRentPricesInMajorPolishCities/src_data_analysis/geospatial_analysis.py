import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
import seaborn as sns
import numpy as np
from esda.moran import Moran
from libpysal.weights import Queen
import folium
from folium.plugins import HeatMap

# Directory containing the CSV files
data_dir = 'data_locations'
export_dir = 'exports'

# Ensure export directory exists
os.makedirs(export_dir, exist_ok=True)

# List of Polish cities with correct characters
cities = {
    'gdansk': 'Gdańsk',
    'krakow': 'Kraków',
    'lodz': 'Łódź',
    'poznan': 'Poznań',
    'warsaw': 'Warszawa',
    'wroclaw': 'Wrocław'
}

# Initialize a DataFrame to hold all the data
all_data = pd.DataFrame()

# Load data from all cities
for city_key, city_name in cities.items():
    file_path = os.path.join(data_dir, f'{city_key}_preprocessed_preprocessed_preprocessed.csv')
    if os.path.exists(file_path):
        data = pd.read_csv(file_path)
        data['city'] = city_name  # Add city name to data
        all_data = pd.concat([all_data, data], ignore_index=True)
    else:
        print(f'File for {city_name} not found: {file_path}')

# Create a GeoDataFrame
gdf = gpd.GeoDataFrame(all_data, geometry=gpd.points_from_xy(all_data.longitude, all_data.latitude))
gdf.crs = 'epsg:4326'

# Plot spatial distribution of flat prices
for city_key, city_name in cities.items():
    city_gdf = gdf[gdf['city'] == city_name]
    
    # Convert to Web Mercator for contextily basemap
    city_gdf = city_gdf.to_crs(epsg=3857)
    
    fig, ax = plt.subplots(figsize=(10, 10))
    city_gdf.plot(ax=ax, column='price', cmap='coolwarm', legend=True, markersize=15, alpha=0.8)
    ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron)
    ax.set_title(f'Spatial Distribution of Flat Prices in {city_name} [pln]')
    ax.set_axis_off()
    
    plt.savefig(os.path.join(export_dir, f'{city_key}_price_distribution.png'))
    plt.close()

# Calculate and print Moran's I for spatial autocorrelation
all_gdf = gdf.to_crs(epsg=3857)
weights = Queen.from_dataframe(all_gdf)
moran = Moran(all_gdf['price'], weights)
print(f"Moran's I: {moran.I}, p-value: {moran.p_sim}")

# Create heatmap for all cities
m = folium.Map(location=[52.2297, 21.0122], zoom_start=6)
heat_data = [[row['latitude'], row['longitude'], row['price']] for index, row in all_gdf.iterrows()]
HeatMap(heat_data).add_to(m)
m.save(os.path.join(export_dir, 'heatmap_all_cities.html'))

print("Geospatial analysis completed. Plots saved to 'exports/' directory.")
