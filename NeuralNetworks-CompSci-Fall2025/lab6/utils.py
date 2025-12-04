import torch
import numpy as np
from torch.utils.data import DataLoader, TensorDataset


def add_gaussian_noise(data, noise_std):
    """
    Add Gaussian noise to data.

    Args:
        data: Input tensor
        noise_std: Standard deviation of Gaussian noise

    Returns:
        Noisy tensor
    """
    if noise_std == 0:
        return data
    noise = torch.randn_like(data) * noise_std
    return data + noise


def prepare_dataloaders(train_data, train_labels, test_data, test_labels,
                       batch_size=32, noise_in_train=False, noise_in_test=False,
                       train_noise_std=0.0, test_noise_std=0.0):
    """
    Prepare data loaders with optional noise injection.

    Args:
        train_data: Training images (N, 1, H, W)
        train_labels: Training labels (N,)
        test_data: Test images (N, 1, H, W)
        test_labels: Test labels (N,)
        batch_size: Batch size for data loaders
        noise_in_train: Whether to add noise in training
        noise_in_test: Whether to add noise in testing
        train_noise_std: Standard deviation for training noise
        test_noise_std: Standard deviation for test noise

    Returns:
        Tuple of (train_loader, val_loader, test_loader)
    """
    # Convert to tensors if needed
    if not isinstance(train_data, torch.Tensor):
        train_data = torch.FloatTensor(train_data)
    if not isinstance(train_labels, torch.Tensor):
        train_labels = torch.LongTensor(train_labels)
    if not isinstance(test_data, torch.Tensor):
        test_data = torch.FloatTensor(test_data)
    if not isinstance(test_labels, torch.Tensor):
        test_labels = torch.LongTensor(test_labels)

    # Ensure 4D shape (batch, channels, height, width)
    if train_data.dim() == 3:
        train_data = train_data.unsqueeze(1)
    if test_data.dim() == 3:
        test_data = test_data.unsqueeze(1)

    # Add noise to training data if specified
    if noise_in_train and train_noise_std > 0:
        train_data = add_gaussian_noise(train_data, train_noise_std)

    # Add noise to test data if specified
    if noise_in_test and test_noise_std > 0:
        test_data = add_gaussian_noise(test_data, test_noise_std)

    # Split training into train/val (80/20)
    train_size = int(0.8 * len(train_data))
    val_size = len(train_data) - train_size

    train_subset, val_subset = torch.utils.data.random_split(
        TensorDataset(train_data, train_labels),
        [train_size, val_size]
    )

    train_loader = DataLoader(train_subset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_subset, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(
        TensorDataset(test_data, test_labels),
        batch_size=batch_size,
        shuffle=False
    )

    return train_loader, val_loader, test_loader


def load_fashion_mnist(data_path='./data', subsample_fraction=1.0):
    """
    Load Fashion-MNIST dataset.

    Args:
        data_path: Path to store/load data
        subsample_fraction: Fraction of data to use (for quick testing)

    Returns:
        Tuple of (train_data, train_labels, test_data, test_labels)
    """
    from torchvision import datasets, transforms

    transform = transforms.ToTensor()

    # Download/load training data
    train_dataset = datasets.FashionMNIST(
        root=data_path,
        train=True,
        download=True,
        transform=transform
    )

    # Download/load test data
    test_dataset = datasets.FashionMNIST(
        root=data_path,
        train=False,
        download=True,
        transform=transform
    )

    # Convert to numpy arrays
    train_data = train_dataset.data.float() / 255.0
    train_labels = train_dataset.targets
    test_data = test_dataset.data.float() / 255.0
    test_labels = test_dataset.targets

    # Subsample if needed
    if subsample_fraction < 1.0:
        n_train = int(len(train_data) * subsample_fraction)
        n_test = int(len(test_data) * subsample_fraction)
        train_data = train_data[:n_train]
        train_labels = train_labels[:n_train]
        test_data = test_data[:n_test]
        test_labels = test_labels[:n_test]

    # Ensure proper shape (N, 1, H, W)
    if train_data.dim() == 3:
        train_data = train_data.unsqueeze(1)
    if test_data.dim() == 3:
        test_data = test_data.unsqueeze(1)

    return train_data, train_labels, test_data, test_labels
