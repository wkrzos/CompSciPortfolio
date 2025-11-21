"""
Training and evaluation functions for FashionMNIST classification.
Supports Gaussian noise injection for robustness testing.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Subset
import torchvision
import torchvision.transforms as transforms
import numpy as np
from tqdm import tqdm
import time


def get_data_loaders(batch_size=32, data_fraction=1.0, noise_std=0.0, noise_train=False):
    """
    Get FashionMNIST data loaders with optional data subsetting and noise.

    Args:
        batch_size: Batch size for training and testing
        data_fraction: Fraction of training data to use (0.01, 0.1, 1.0)
        noise_std: Standard deviation of Gaussian noise to add
        noise_train: If True, add noise to training data; if False, only to test data

    Returns:
        train_loader, test_loader
    """
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))  # Normalize to [-1, 1]
    ])

    # Download and load training data
    train_dataset = torchvision.datasets.FashionMNIST(
        root='./data',
        train=True,
        download=True,
        transform=transform
    )

    # Subset training data if needed
    if data_fraction < 1.0:
        num_samples = int(len(train_dataset) * data_fraction)
        indices = np.random.choice(len(train_dataset), num_samples, replace=False)
        train_dataset = Subset(train_dataset, indices)

    # Download and load test data
    test_dataset = torchvision.datasets.FashionMNIST(
        root='./data',
        train=False,
        download=True,
        transform=transform
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=2
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=2
    )

    return train_loader, test_loader


def add_gaussian_noise(images, noise_std):
    """
    Add Gaussian noise to images.

    Args:
        images: Input tensor of images
        noise_std: Standard deviation of Gaussian noise

    Returns:
        Noisy images
    """
    if noise_std > 0:
        noise = torch.randn_like(images) * noise_std
        return images + noise
    return images


def train_epoch(model, train_loader, criterion, optimizer, device, noise_std=0.0, noise_train=False):
    """
    Train model for one epoch.

    Args:
        model: Neural network model
        train_loader: Training data loader
        criterion: Loss function
        optimizer: Optimizer
        device: Device to train on (cpu/cuda)
        noise_std: Standard deviation of Gaussian noise
        noise_train: Whether to add noise during training

    Returns:
        Average training loss, training accuracy
    """
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)

        # Add noise to training data if specified
        if noise_train and noise_std > 0:
            images = add_gaussian_noise(images, noise_std)

        # Zero gradients
        optimizer.zero_grad()

        # Forward pass
        outputs = model(images)
        loss = criterion(outputs, labels)

        # Backward pass and optimization
        loss.backward()
        optimizer.step()

        # Statistics
        running_loss += loss.item() * images.size(0)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    epoch_loss = running_loss / total
    epoch_acc = 100 * correct / total

    return epoch_loss, epoch_acc


def evaluate(model, test_loader, criterion, device, noise_std=0.0):
    """
    Evaluate model on test data.

    Args:
        model: Neural network model
        test_loader: Test data loader
        criterion: Loss function
        device: Device to evaluate on (cpu/cuda)
        noise_std: Standard deviation of Gaussian noise to add to test data

    Returns:
        Average test loss, test accuracy
    """
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)

            # Add noise to test data
            if noise_std > 0:
                images = add_gaussian_noise(images, noise_std)

            # Forward pass
            outputs = model(images)
            loss = criterion(outputs, labels)

            # Statistics
            running_loss += loss.item() * images.size(0)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    epoch_loss = running_loss / total
    epoch_acc = 100 * correct / total

    return epoch_loss, epoch_acc


def train_model(model, train_loader, test_loader, num_epochs=20, learning_rate=0.001,
                device='cpu', noise_std=0.0, noise_train=False, verbose=True,
                early_stopping=True, patience=5, min_delta=0.001):
    """
    Train model for multiple epochs and track performance.

    Args:
        model: Neural network model
        train_loader: Training data loader
        test_loader: Test data loader
        num_epochs: Number of training epochs
        learning_rate: Learning rate for optimizer
        device: Device to train on (cpu/cuda)
        noise_std: Standard deviation of Gaussian noise
        noise_train: Whether to add noise during training
        verbose: Whether to print progress
        early_stopping: Whether to use early stopping
        patience: Number of epochs to wait for improvement before stopping
        min_delta: Minimum change in test loss to qualify as improvement

    Returns:
        Dictionary with training history and results
    """
    model = model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    history = {
        'train_loss': [],
        'train_acc': [],
        'test_loss': [],
        'test_acc': [],
        'epoch_times': [],
        'stopped_epoch': None
    }

    # Early stopping variables
    best_test_loss = float('inf')
    best_model_state = None
    epochs_without_improvement = 0

    if verbose:
        print(f"Training on {device}")
        if early_stopping:
            print(f"Early stopping enabled: patience={patience}, min_delta={min_delta}")
        pbar = tqdm(range(num_epochs), desc="Training")
    else:
        pbar = range(num_epochs)

    for epoch in pbar:
        epoch_start = time.time()

        # Train
        train_loss, train_acc = train_epoch(
            model, train_loader, criterion, optimizer, device, noise_std, noise_train
        )

        # Evaluate
        test_loss, test_acc = evaluate(model, test_loader, criterion, device, noise_std)

        epoch_time = time.time() - epoch_start

        # Record history
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['test_loss'].append(test_loss)
        history['test_acc'].append(test_acc)
        history['epoch_times'].append(epoch_time)

        # Early stopping check
        if early_stopping:
            if test_loss < best_test_loss - min_delta:
                best_test_loss = test_loss
                best_model_state = model.state_dict().copy()
                epochs_without_improvement = 0
            else:
                epochs_without_improvement += 1

            if epochs_without_improvement >= patience:
                if verbose:
                    print(f"\nEarly stopping triggered at epoch {epoch + 1}")
                    print(f"Best test loss: {best_test_loss:.4f}")
                history['stopped_epoch'] = epoch + 1
                # Restore best model
                if best_model_state is not None:
                    model.load_state_dict(best_model_state)
                break

        if verbose:
            postfix = {
                'train_loss': f'{train_loss:.4f}',
                'train_acc': f'{train_acc:.2f}%',
                'test_loss': f'{test_loss:.4f}',
                'test_acc': f'{test_acc:.2f}%'
            }
            if early_stopping:
                postfix['patience'] = f'{epochs_without_improvement}/{patience}'
            pbar.set_postfix(postfix)

    # If early stopping was used but not triggered, save the last state as best
    if early_stopping and history['stopped_epoch'] is None and best_model_state is not None:
        model.load_state_dict(best_model_state)

    return history
