"""
Utility functions for loading and preprocessing IMDB dataset.
"""

import torch
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence
import numpy as np
import pickle
import os
from collections import Counter


def load_imdb_data(data_dir='./data', max_words=10000, max_len=None):
    """
    Load IMDB dataset from Keras format.

    Args:
        data_dir: Directory to store/load data
        max_words: Maximum vocabulary size
        max_len: Maximum sequence length (None for no truncation)

    Returns:
        Tuple of (train_data, train_labels, test_data, test_labels, word_index)
    """
    # Try to load from disk first
    cache_file = os.path.join(data_dir, f'imdb_maxwords{max_words}_maxlen{max_len}.pkl')

    if os.path.exists(cache_file):
        print(f"Loading cached data from {cache_file}")
        with open(cache_file, 'rb') as f:
            data = pickle.load(f)
        return data['train_data'], data['train_labels'], data['test_data'], data['test_labels'], data['word_index']

    # Download from Keras
    print("Downloading IMDB dataset from Keras...")
    try:
        from tensorflow.keras.datasets import imdb
        from tensorflow.keras.preprocessing.sequence import pad_sequences

        # Load data
        (train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=max_words)

        # Get word index
        word_index = imdb.get_word_index()

        # Truncate sequences if max_len specified
        if max_len is not None:
            train_data = [seq[:max_len] for seq in train_data]
            test_data = [seq[:max_len] for seq in test_data]

        # Save to cache
        os.makedirs(data_dir, exist_ok=True)
        with open(cache_file, 'wb') as f:
            pickle.dump({
                'train_data': train_data,
                'train_labels': train_labels,
                'test_data': test_data,
                'test_labels': test_labels,
                'word_index': word_index
            }, f)

        print(f"Data cached to {cache_file}")
        return train_data, train_labels, test_data, test_labels, word_index

    except Exception as e:
        print(f"Error loading data: {e}")
        raise


def subsample_data(data, labels, fraction=1.0, seed=42):
    """
    Subsample dataset to a given fraction.

    Args:
        data: Input sequences
        labels: Labels
        fraction: Fraction of data to keep (0.0-1.0)
        seed: Random seed

    Returns:
        Tuple of (subsampled_data, subsampled_labels)
    """
    if fraction >= 1.0:
        return data, labels

    np.random.seed(seed)
    n_samples = len(data)
    n_subsample = int(n_samples * fraction)

    indices = np.random.choice(n_samples, n_subsample, replace=False)

    if isinstance(data, list):
        subsampled_data = [data[i] for i in indices]
    else:
        subsampled_data = data[indices]

    if isinstance(labels, list):
        subsampled_labels = [labels[i] for i in indices]
    else:
        subsampled_labels = labels[indices]

    return subsampled_data, subsampled_labels


class IMDBDataset(Dataset):
    """PyTorch Dataset for IMDB reviews."""

    def __init__(self, sequences, labels):
        """
        Initialize IMDB dataset.

        Args:
            sequences: List of word index sequences
            labels: List of labels (0 or 1)
        """
        self.sequences = sequences
        self.labels = labels

    def __len__(self):
        return len(self.sequences)

    def __getitem__(self, idx):
        return torch.LongTensor(self.sequences[idx]), torch.LongTensor([self.labels[idx]])


def collate_fn(batch):
    """
    Collate function for DataLoader - pads sequences to same length.

    Args:
        batch: List of (sequence, label) tuples

    Returns:
        Tuple of (padded_sequences, labels)
    """
    sequences, labels = zip(*batch)

    # Pad sequences to max length in batch
    padded_sequences = pad_sequence(sequences, batch_first=True, padding_value=0)
    labels = torch.cat(labels)

    return padded_sequences, labels


def prepare_dataloaders(train_data, train_labels, test_data, test_labels,
                       batch_size=32, val_split=0.2, subsample_fraction=1.0):
    """
    Prepare DataLoaders for training.

    Args:
        train_data: Training sequences
        train_labels: Training labels
        test_data: Test sequences
        test_labels: Test labels
        batch_size: Batch size
        val_split: Fraction of training data to use for validation
        subsample_fraction: Fraction of data to use

    Returns:
        Tuple of (train_loader, val_loader, test_loader)
    """
    # Subsample if needed
    if subsample_fraction < 1.0:
        train_data, train_labels = subsample_data(train_data, train_labels, subsample_fraction)
        test_data, test_labels = subsample_data(test_data, test_labels, subsample_fraction)

    # Split training into train/val
    n_train = len(train_data)
    n_val = int(n_train * val_split)
    n_train = n_train - n_val

    indices = np.random.permutation(len(train_data))
    train_indices = indices[:n_train]
    val_indices = indices[n_train:]

    if isinstance(train_data, list):
        train_data_split = [train_data[i] for i in train_indices]
        val_data_split = [train_data[i] for i in val_indices]
        train_labels_split = [train_labels[i] for i in train_indices]
        val_labels_split = [train_labels[i] for i in val_indices]
    else:
        train_data_split = train_data[train_indices]
        val_data_split = train_data[val_indices]
        train_labels_split = train_labels[train_indices]
        val_labels_split = train_labels[val_indices]

    # Create datasets
    train_dataset = IMDBDataset(train_data_split, train_labels_split)
    val_dataset = IMDBDataset(val_data_split, val_labels_split)
    test_dataset = IMDBDataset(test_data, test_labels)

    # Create dataloaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        collate_fn=collate_fn
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        collate_fn=collate_fn
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        collate_fn=collate_fn
    )

    return train_loader, val_loader, test_loader


def get_sequence_stats(sequences):
    """
    Get statistics about sequence lengths.

    Args:
        sequences: List of sequences

    Returns:
        Dictionary with statistics
    """
    lengths = [len(seq) for seq in sequences]

    return {
        'count': len(lengths),
        'min': min(lengths),
        'max': max(lengths),
        'mean': np.mean(lengths),
        'median': np.median(lengths),
        'std': np.std(lengths),
        'percentiles': {
            '25': np.percentile(lengths, 25),
            '50': np.percentile(lengths, 50),
            '75': np.percentile(lengths, 75),
            '90': np.percentile(lengths, 90),
            '95': np.percentile(lengths, 95),
            '99': np.percentile(lengths, 99)
        }
    }
