import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
import seaborn as sns

# Directory containing the CSV files
data_dir = 'data_locations'

# List of Polish cities
cities = ['gdansk', 'krakow', 'lodz', 'poznan', 'warsaw', 'wroclaw']

# Process each file in the directory
for city in cities:
    file_path = os.path.join(data_dir, f'{city}_preprocessed_preprocessed_preprocessed.csv')
    
    # Check if the file exists
    if os.path.exists(file_path):
        # Load the CSV data
        data = pd.read_csv(file_path)
        
        # Convert the DataFrame to a GeoDataFrame
        gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.longitude, data.latitude))
        
        # Set the coordinate reference system to WGS84
        gdf.crs = 'epsg:4326'
        
        # Convert to Web Mercator for contextily
        gdf = gdf.to_crs(epsg=3857)
        
        # Create a scatter plot
        fig, ax = plt.subplots(figsize=(10, 10))
        gdf.plot(ax=ax, markersize=10, color='red', alpha=0.0, edgecolor='k')
        
        # Add basemap
        ctx.add_basemap(ax, crs=gdf.crs.to_string(), source=ctx.providers.CartoDB.Positron)
        
        # Generate heatmap using seaborn
        kde = sns.kdeplot(x=gdf.geometry.x, y=gdf.geometry.y, ax=ax, cmap="Oranges", fill=True, alpha=0.5)
        
        # Set titles and labels
        ax.set_title(f'Heatmap of Flat Locations in {city.capitalize()}')
        ax.set_xlabel('Longitude [no unit]')
        ax.set_ylabel('Latitude [no unit]')
        
        # Save the plot as an image
        plt.savefig(f'exports/{city}_heatmap.png', dpi=300)
        
        # Show the plot
        plt.show()
    else:
        print(f'File for {city.capitalize()} not found: {file_path}')
