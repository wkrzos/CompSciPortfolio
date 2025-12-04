import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm
import json
import os
from datetime import datetime


def train_epoch(model, train_loader, optimizer, criterion, device):
    """
    Train for one epoch.

    Args:
        model: Neural network model
        train_loader: Training data loader
        optimizer: Optimizer
        criterion: Loss function
        device: Device (cuda or cpu)

    Returns:
        Average training loss
    """
    model.train()
    total_loss = 0.0
    total_samples = 0

    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item() * images.size(0)
        total_samples += images.size(0)

    return total_loss / total_samples


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
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)

            outputs = model(images)
            loss = criterion(outputs, labels)

            total_loss += loss.item() * images.size(0)

            _, predicted = torch.max(outputs.data, 1)
            total_correct += (predicted == labels).sum().item()
            total_samples += images.size(0)

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
        Tuple of (accuracy, per-class accuracies)
    """
    model.eval()
    total_correct = 0
    total_samples = 0
    class_correct = {}
    class_total = {}

    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)

            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)

            total_correct += (predicted == labels).sum().item()
            total_samples += images.size(0)

            # Track per-class accuracy
            for label, pred in zip(labels, predicted):
                label = label.item()
                if label not in class_total:
                    class_total[label] = 0
                    class_correct[label] = 0
                class_total[label] += 1
                if label == pred.item():
                    class_correct[label] += 1

    accuracy = total_correct / total_samples if total_samples > 0 else 0.0

    per_class_acc = {}
    for cls in class_total:
        per_class_acc[cls] = class_correct[cls] / class_total[cls]

    return accuracy, per_class_acc


def train_model(model, train_loader, val_loader, test_loader, device,
                epochs=20, learning_rate=0.001, weight_decay=1e-5):
    """
    Full training pipeline.

    Args:
        model: Neural network model
        train_loader: Training data loader
        val_loader: Validation data loader
        test_loader: Test data loader
        device: Device (cuda or cpu)
        epochs: Number of epochs
        learning_rate: Learning rate
        weight_decay: Weight decay for optimizer

    Returns:
        Dictionary with training history and results
    """
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=weight_decay)

    history = {
        'train_loss': [],
        'val_loss': [],
        'val_accuracy': [],
    }

    best_val_acc = 0.0
    best_model_state = None
    patience = 10
    patience_counter = 0

    model.to(device)

    for epoch in range(epochs):
        # Train
        train_loss = train_epoch(model, train_loader, optimizer, criterion, device)

        # Validate
        val_loss, val_acc = validate(model, val_loader, criterion, device)

        history['train_loss'].append(train_loss)
        history['val_loss'].append(val_loss)
        history['val_accuracy'].append(val_acc)

        print(f"Epoch {epoch+1}/{epochs} | "
              f"Train Loss: {train_loss:.4f} | "
              f"Val Loss: {val_loss:.4f} | "
              f"Val Acc: {val_acc:.4f}")

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
    test_acc, per_class_acc = test(model, test_loader, device)

    results = {
        'test_accuracy': test_acc,
        'per_class_accuracy': per_class_acc,
        'best_val_accuracy': best_val_acc,
        'history': history
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
        'results': results
    }

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
