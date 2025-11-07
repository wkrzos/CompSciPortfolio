"""
Data loading and preprocessing utilities.
"""

import numpy as np
import pandas as pd
from pathlib import Path


def load_heart_disease_data(data_path='processed_heart_cleveland.csv', 
                            normalize=True, 
                            test_size=0.2, 
                            random_state=42):
    """Load and preprocess the heart disease dataset.
    
    Args:
        data_path: Path to the CSV file
        normalize: Whether to normalize features (z-score normalization)
        test_size: Fraction of data to use for testing
        random_state: Random seed for reproducibility
        
    Returns:
        Tuple of (x_train, y_train, x_test, y_test, feature_names)
        where y are one-hot encoded
    """
    # Try multiple possible paths
    possible_paths = [
        Path(data_path),
        Path('lab3') / data_path,
        Path('lab2') / data_path,
        Path('..') / 'lab2' / data_path,
    ]
    
    df = None
    for path in possible_paths:
        if path.exists():
            df = pd.read_csv(path)
            print(f"Loaded data from: {path}")
            break
    
    if df is None:
        raise FileNotFoundError(f"Could not find {data_path} in any expected location")
    
    # Separate features and target
    x = df.drop('target', axis=1).values
    y = df['target'].values
    feature_names = df.drop('target', axis=1).columns.tolist()
    
    # Convert to one-hot encoding
    n_classes = len(np.unique(y))
    y_onehot = np.zeros((len(y), n_classes))
    y_onehot[np.arange(len(y)), y] = 1
    
    # Train-test split
    np.random.seed(random_state)
    n_samples = len(x)
    n_test = int(n_samples * test_size)
    
    indices = np.random.permutation(n_samples)
    test_indices = indices[:n_test]
    train_indices = indices[n_test:]
    
    x_train, x_test = x[train_indices], x[test_indices]
    y_train, y_test = y_onehot[train_indices], y_onehot[test_indices]
    
    # Normalize if requested
    if normalize:
        mean = np.mean(x_train, axis=0)
        std = np.std(x_train, axis=0, dtype=np.float64)
        std = np.where(std == 0, 1.0, std)  # Avoid division by zero
        
        x_train = (x_train - mean) / std
        x_test = (x_test - mean) / std
    
    print(f"Dataset shape: {x.shape}")
    print(f"Train samples: {len(x_train)}, Test samples: {len(x_test)}")
    print(f"Number of classes: {n_classes}")
    print(f"Features normalized: {normalize}")
    
    return x_train, y_train, x_test, y_test, feature_names


def create_batches(x, y, batch_size):
    """Create mini-batches from data.
    
    Args:
        x: Input data (n_samples, input_dim)
        y: Labels (n_samples, output_dim)
        batch_size: Size of each batch
        
    Yields:
        Tuples of (x_batch, y_batch)
    """
    n_samples = x.shape[0]
    indices = np.random.permutation(n_samples)
    
    for start_idx in range(0, n_samples, batch_size):
        end_idx = min(start_idx + batch_size, n_samples)
        batch_indices = indices[start_idx:end_idx]
        yield x[batch_indices], y[batch_indices]
