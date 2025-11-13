import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import json
from pathlib import Path


def load_data(data_path, test_size=0.2, random_state=42):
    df = pd.read_csv(data_path)
    
    X = df.drop('target', axis=1).values
    y = df['target'].values
    
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    
    x_train, x_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    return x_train, y_train, x_test, y_test


def save_results(history, train_acc, test_acc, output_dir, config_name):
    results = {
        'history': history,
        'final_train_acc': float(train_acc),
        'final_test_acc': float(test_acc),
    }
    
    output_file = output_dir / f'{config_name}_results.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
