"""
Training and evaluation functions for recurrent networks.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm
import json
import os
from datetime import datetime


def train_epoch(model, train_loader, optimizer, criterion, device, grad_clip=None):
    """
    Train for one epoch with optional gradient clipping.

    Args:
        model: Neural network model
        train_loader: Training data loader
        optimizer: Optimizer
        criterion: Loss function
        device: Device (cuda or cpu)
        grad_clip: Gradient clipping threshold (None to disable)

    Returns:
        Average training loss and accuracy
    """
    model.train()
    total_loss = 0.0
    total_correct = 0
    total_samples = 0

    for sequences, labels in train_loader:
        sequences, labels = sequences.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(sequences)
        loss = criterion(outputs, labels)
        loss.backward()

        # Gradient clipping
        if grad_clip is not None:
            torch.nn.utils.clip_grad_norm_(model.parameters(), grad_clip)

        optimizer.step()
        total_loss += loss.item() * sequences.size(0)

        _, predicted = torch.max(outputs.data, 1)
        total_correct += (predicted == labels).sum().item()
        total_samples += sequences.size(0)

    avg_loss = total_loss / total_samples
    accuracy = total_correct / total_samples

    return avg_loss, accuracy


def validate(model, val_loader, criterion, device):
    """
    Validate on validation set.

    Args:
        model: Neural network model
        val_loader: Validation data loader
        criterion: Loss function
        device: Device (cuda or cpu)

    Returns:
        Tuple of (loss, accuracy)
    """
    model.eval()
    total_loss = 0.0
    total_correct = 0
    total_samples = 0

    with torch.no_grad():
        for sequences, labels in val_loader:
            sequences, labels = sequences.to(device), labels.to(device)

            outputs = model(sequences)
            loss = criterion(outputs, labels)

            total_loss += loss.item() * sequences.size(0)

            _, predicted = torch.max(outputs.data, 1)
            total_correct += (predicted == labels).sum().item()
            total_samples += sequences.size(0)

    avg_loss = total_loss / total_samples
    accuracy = total_correct / total_samples

    return avg_loss, accuracy


def test(model, test_loader, device):
    """
    Test on test set.

    Args:
        model: Neural network model
        test_loader: Test data loader
        device: Device (cuda or cpu)

    Returns:
        Test accuracy
    """
    model.eval()
    total_correct = 0
    total_samples = 0

    with torch.no_grad():
        for sequences, labels in test_loader:
            sequences, labels = sequences.to(device), labels.to(device)

            outputs = model(sequences)
            _, predicted = torch.max(outputs.data, 1)

            total_correct += (predicted == labels).sum().item()
            total_samples += sequences.size(0)

    accuracy = total_correct / total_samples
    return accuracy


def train_model(model, train_loader, val_loader, test_loader, device,
                epochs=20, learning_rate=0.001, weight_decay=1e-4, patience=5,
                grad_clip=1.0, use_scheduler=True):
    """
    Full training pipeline with early stopping, gradient clipping, and LR scheduling.

    Args:
        model: Neural network model
        train_loader: Training data loader
        val_loader: Validation data loader
        test_loader: Test data loader
        device: Device (cuda or cpu)
        epochs: Maximum number of epochs
        learning_rate: Learning rate
        weight_decay: Weight decay for optimizer (L2 regularization)
        patience: Early stopping patience
        grad_clip: Gradient clipping threshold (None to disable)
        use_scheduler: Whether to use learning rate scheduler

    Returns:
        Dictionary with training history and results
    """
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=weight_decay)

    # Learning rate scheduler: reduce on plateau
    scheduler = None
    if use_scheduler:
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, mode='max', factor=0.5, patience=3
        )

    history = {
        'train_loss': [],
        'train_accuracy': [],
        'val_loss': [],
        'val_accuracy': [],
    }

    best_val_acc = 0.0
    best_model_state = None
    patience_counter = 0

    model.to(device)

    print(f"Starting training on {device}...")
    for epoch in range(epochs):
        # Train with gradient clipping
        train_loss, train_acc = train_epoch(model, train_loader, optimizer, criterion, device, grad_clip)

        # Validate
        val_loss, val_acc = validate(model, val_loader, criterion, device)

        # Step scheduler
        if scheduler is not None:
            scheduler.step(val_acc)

        history['train_loss'].append(train_loss)
        history['train_accuracy'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_accuracy'].append(val_acc)

        print(f"Epoch {epoch+1}/{epochs} | "
              f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f} | "
              f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}")

        # Early stopping
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_model_state = model.state_dict().copy()
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print(f"Early stopping at epoch {epoch+1}")
                break

    # Load best model
    if best_model_state is not None:
        model.load_state_dict(best_model_state)

    # Test
    test_acc = test(model, test_loader, device)
    print(f"Test Accuracy: {test_acc:.4f}")

    results = {
        'test_accuracy': test_acc,
        'best_val_accuracy': best_val_acc,
        'final_train_accuracy': history['train_accuracy'][-1],
        'final_val_accuracy': history['val_accuracy'][-1],
        'history': history,
        'epochs_trained': len(history['train_loss'])
    }

    return results, model


def save_results(results, config, output_path):
    """
    Save experiment results to JSON file.

    Args:
        results: Results dictionary
        config: Configuration dictionary
        output_path: Path to save results
    """
    output_data = {
        'config': config,
        'results': results,
        'timestamp': datetime.now().isoformat()
    }

    # Convert numpy types to native Python types
    def convert_to_serializable(obj):
        import numpy as np
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj

    # Recursively convert
    def recursive_convert(obj):
        if isinstance(obj, dict):
            return {k: recursive_convert(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [recursive_convert(item) for item in obj]
        else:
            return convert_to_serializable(obj)

    output_data = recursive_convert(output_data)

    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=2)


def load_results(input_path):
    """
    Load experiment results from JSON file.

    Args:
        input_path: Path to load results from

    Returns:
        Tuple of (config, results)
    """
    with open(input_path, 'r') as f:
        data = json.load(f)

    return data['config'], data['results']
