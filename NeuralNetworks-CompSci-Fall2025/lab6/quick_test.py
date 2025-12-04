#!/usr/bin/env python3
"""
Quick test to verify the CNN setup works correctly.
"""

import torch
import torch.nn as nn
from model import CNNModel
from utils import load_fashion_mnist, prepare_dataloaders
from train import train_model

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Device: {device}")

# Load small subset
print("Loading data...")
train_data, train_labels, test_data, test_labels = load_fashion_mnist('./data', subsample_fraction=0.1)
print(f"Train: {train_data.shape}, Test: {test_data.shape}")

# Prepare loaders
print("Preparing data loaders...")
train_loader, val_loader, test_loader = prepare_dataloaders(
    train_data, train_labels, test_data, test_labels,
    batch_size=32
)

# Create model
print("Creating model...")
model = CNNModel(out_channels=32, kernel_size=3, pool_size=2)
print(f"Model: {model}")

# Check forward pass
print("\nTesting forward pass...")
for images, labels in train_loader:
    images = images.to(device)
    outputs = model.to(device)(images)
    print(f"Input shape: {images.shape}")
    print(f"Output shape: {outputs.shape}")
    print(f"Expected output shape: (batch_size, 10)")
    break

# Train for 2 epochs
print("\nTraining for 2 epochs...")
results, _ = train_model(
    model, train_loader, val_loader, test_loader, device,
    epochs=2
)

print(f"\nTest Accuracy: {results['test_accuracy']:.4f}")
print("Quick test completed successfully!")
