import pandas as pd
from time_utils import time_to_seconds

def load_transit_data(file_path):
    """Load transit data from CSV and preprocess it."""
    df = pd.read_csv(file_path, low_memory=False)
    # Convert times to seconds
    df['dep_sec'] = df['departure_time'].apply(time_to_seconds)
    df['arr_sec'] = df['arrival_time'].apply(time_to_seconds)
    return df

def extract_stops_coordinates(df):
    """Extract coordinates for all stops from the dataframe."""
    stops_coords = {}
    for _, row in df.iterrows():
        stops_coords[row['start_stop']] = (row['start_stop_lat'], row['start_stop_lon'])
        stops_coords[row['end_stop']] = (row['end_stop_lat'], row['end_stop_lon'])
    return stops_coords
