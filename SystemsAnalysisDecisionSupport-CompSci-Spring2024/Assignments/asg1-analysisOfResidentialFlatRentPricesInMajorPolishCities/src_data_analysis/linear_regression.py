import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

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

# Function to plot and save the results
def plot_results(y_test, y_pred, title, file_path):
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.3)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], '--r', linewidth=2)
    plt.xlabel('Actual Price [zł]')
    plt.ylabel('Predicted Price [zł]')
    plt.title(title)
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()

# Process each city separately
for city_key, city_name in cities.items():
    file_path = os.path.join(data_dir, f'{city_key}_preprocessed_preprocessed_preprocessed.csv')
    
    if os.path.exists(file_path):
        # Load the CSV data
        data = pd.read_csv(file_path)
        all_data = pd.concat([all_data, data], ignore_index=True)
        
        # Drop unnecessary columns
        data = data.drop(columns=['id', 'latitude', 'longitude', 'address'])
        
        # Handle missing values (if any)
        data = data.dropna()
        
        # Convert categorical variables to numerical using one-hot encoding
        categorical_features = ['builttype']
        numerical_features = [col for col in data.columns if col not in categorical_features + ['price']]
        
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', 'passthrough', numerical_features),
                ('cat', OneHotEncoder(), categorical_features)
            ])
        
        # Linear model
        pipeline_linear = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('regressor', LinearRegression())
        ])
        
        # Split the data into training and test sets
        X = data.drop(columns=['price'])
        y = data['price']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train the linear model
        pipeline_linear.fit(X_train, y_train)
        
        # Predict on the test set with linear model
        y_pred_linear = pipeline_linear.predict(X_test)
        
        # Evaluate the linear model
        r2_linear = r2_score(y_test, y_pred_linear)
        mae_linear = mean_absolute_error(y_test, y_pred_linear)
        
        # Plot the results for linear model
        plot_results(y_test, y_pred_linear, f'Actual vs Predicted Price for {city_name} (Linear) (R²: {r2_linear:.2f}, MAE: {mae_linear:.2f}) [zł]', os.path.join(export_dir, f'{city_key}_price_prediction_linear.png'))
        
        # Random forest model
        pipeline_rf = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('regressor', RandomForestRegressor(random_state=42))
        ])
        
        # Train the random forest model
        pipeline_rf.fit(X_train, y_train)
        
        # Predict on the test set with random forest model
        y_pred_rf = pipeline_rf.predict(X_test)
        
        # Evaluate the random forest model
        r2_rf = r2_score(y_test, y_pred_rf)
        mae_rf = mean_absolute_error(y_test, y_pred_rf)
        
        # Plot the results for random forest model
        plot_results(y_test, y_pred_rf, f'Actual vs Predicted Price for {city_name} (Random Forest) (R²: {r2_rf:.2f}, MAE: {mae_rf:.2f}) [zł]', os.path.join(export_dir, f'{city_key}_price_prediction_rf.png'))
        
        # Logarithmic model
        y_log = np.log1p(y)  # Apply log transformation to the target variable
        pipeline_log = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('regressor', LinearRegression())
        ])
        
        # Split the data into training and test sets for logarithmic model
        X_train_log, X_test_log, y_train_log, y_test_log = train_test_split(X, y_log, test_size=0.2, random_state=42)
        
        # Train the logarithmic model
        pipeline_log.fit(X_train_log, y_train_log)
        
        # Predict on the test set with logarithmic model
        y_pred_log = pipeline_log.predict(X_test_log)
        
        # Convert predictions back to original scale
        y_pred_log_exp = np.expm1(y_pred_log)
        y_test_log_exp = np.expm1(y_test_log)
        
        # Evaluate the logarithmic model
        r2_log = r2_score(y_test_log_exp, y_pred_log_exp)
        mae_log = mean_absolute_error(y_test_log_exp, y_pred_log_exp)
        
        # Plot the results for logarithmic model
        plot_results(y_test_log_exp, y_pred_log_exp, f'Actual vs Predicted Price for {city_name} (Logarithmic) (R²: {r2_log:.2f}, MAE: {mae_log:.2f}) [zł]', os.path.join(export_dir, f'{city_key}_price_prediction_logarithmic.png'))
        
    else:
        print(f'File for {city_name} not found: {file_path}')

# Combined graph for all cities
# Drop unnecessary columns
all_data = all_data.drop(columns=['id', 'latitude', 'longitude', 'address'])

# Handle missing values (if any)
all_data = all_data.dropna()

# Convert categorical variables to numerical using one-hot encoding
categorical_features = ['builttype']
numerical_features = [col for col in all_data.columns if col not in categorical_features + ['price']]

preprocessor = ColumnTransformer(
    transformers=[
        ('num', 'passthrough', numerical_features),
        ('cat', OneHotEncoder(), categorical_features)
    ])

# Linear model
pipeline_linear = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

# Split the data into training and test sets
X = all_data.drop(columns=['price'])
y = all_data['price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the linear model
pipeline_linear.fit(X_train, y_train)

# Predict on the test set with linear model
y_pred_linear = pipeline_linear.predict(X_test)

# Evaluate the linear model
r2_linear = r2_score(y_test, y_pred_linear)
mae_linear = mean_absolute_error(y_test, y_pred_linear)

# Plot the results for linear model
plot_results(y_test, y_pred_linear, f'Actual vs Predicted Price for All Cities (Linear) (R²: {r2_linear:.2f}, MAE: {mae_linear:.2f}) [zł]', os.path.join(export_dir, 'all_cities_price_prediction_linear.png'))

# Random forest model
pipeline_rf = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(random_state=42))
])

# Train the random forest model
pipeline_rf.fit(X_train, y_train)

# Predict on the test set with random forest model
y_pred_rf = pipeline_rf.predict(X_test)

# Evaluate the random forest model
r2_rf = r2_score(y_test, y_pred_rf)
mae_rf = mean_absolute_error(y_test, y_pred_rf)

# Plot the results for random forest model
plot_results(y_test, y_pred_rf, f'Actual vs Predicted Price for All Cities (Random Forest) (R²: {r2_rf:.2f}, MAE: {mae_rf:.2f}) [zł]', os.path.join(export_dir, 'all_cities_price_prediction_rf.png'))

# Logarithmic model
y_log = np.log1p(y)  # Apply log transformation to the target variable
pipeline_log = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

# Split the data into training and test sets for logarithmic model
X_train_log, X_test_log, y_train_log, y_test_log = train_test_split(X, y_log, test_size=0.2, random_state=42)

# Train the logarithmic model
pipeline_log.fit(X_train_log, y_train_log)

# Predict on the test set with logarithmic model
y_pred_log = pipeline_log.predict(X_test_log)

# Convert predictions back to original scale
y_pred_log_exp = np.expm1(y_pred_log)
y_test_log_exp = np.expm1(y_test_log)

# Evaluate the logarithmic model
r2_log = r2_score(y_test_log_exp, y_pred_log_exp)
mae_log = mean_absolute_error(y_test_log_exp, y_pred_log_exp)

# Plot the results for logarithmic model
plot_results(y_test_log_exp, y_pred_log_exp, f'Actual vs Predicted Price for All Cities (Logarithmic) (R²: {r2_log:.2f}, MAE: {mae_log:.2f}) [zł]', os.path.join(export_dir, 'all_cities_price_prediction_logarithmic.png'))
