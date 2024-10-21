import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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

# Building type translations
building_type_translations = {
    'blok': 'Block',
    'kamienica': 'Tenement',
    'loft': 'Loft',
    'pozostale': 'Other',
    'szeregowiec': 'Terraced',
    'wolnostojacy': 'Detached'
}

# Initialize a DataFrame to hold all the data
all_data = pd.DataFrame()

# Process each city
for city_key, city_name in cities.items():
    file_path = os.path.join(data_dir, f'{city_key}_preprocessed_preprocessed_preprocessed.csv')
    
    if os.path.exists(file_path):
        # Load the CSV data
        data = pd.read_csv(file_path)
        
        # Rename columns for clarity
        data.rename(columns={
            'floor_select': 'Floor',
            'furniture': 'Furniture',
            'price': 'Price (zł)',
            'builttype': 'Building Type',
            'm': 'Area (m²)',
            'rooms': 'Rooms',
            'rent': 'Rent (zł)'
        }, inplace=True)
        
        # Translate building types
        data['Building Type'] = data['Building Type'].map(building_type_translations)
        
        # Drop non-numeric columns for correlation matrix
        data = data.drop(columns=['id', 'latitude', 'longitude', 'address'])
        
        # Convert categorical columns to one-hot encoding with corrected labels
        data = pd.get_dummies(data, columns=['Building Type'], drop_first=True)
        
        # Adjust column names to remove underscores
        data.columns = [col.replace('_', ' ').title() for col in data.columns]
        
        # Append to the all_data DataFrame
        all_data = pd.concat([all_data, data], ignore_index=True)
        
        # Compute correlation matrix
        corr_matrix = data.corr()
        
        # Plot the heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
        plt.title(f'Correlation Heatmap for {city_name}')
        plt.tight_layout()
        
        # Save the heatmap
        plt.savefig(os.path.join(export_dir, f'{city_key}_correlation_heatmap.png'))
        plt.close()
        
    else:
        print(f'File for {city_name} not found: {file_path}')

# Generate a combined correlation heatmap for all cities
# Compute correlation matrix for all data
all_corr_matrix = all_data.corr()

# Plot the heatmap for all cities combined
plt.figure(figsize=(12, 10))
sns.heatmap(all_corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Combined Correlation Heatmap for All Cities')
plt.tight_layout()

# Save the combined heatmap
plt.savefig(os.path.join(export_dir, 'all_correlation_heatmap.png'))
plt.close()
