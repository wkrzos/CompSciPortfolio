"""
Model definitions for FashionMNIST classification.
Implements single-layer and two-layer neural networks.
"""

import torch
import torch.nn as nn


class SingleLayerNet(nn.Module):
    """Single-layer neural network for FashionMNIST classification."""

    def __init__(self, input_size=784, hidden_size=128, num_classes=10):
        """
        Initialize single-layer network.

        Args:
            input_size: Size of flattened input (28*28=784 for FashionMNIST)
            hidden_size: Number of neurons in hidden layer
            num_classes: Number of output classes (10 for FashionMNIST)
        """
        super(SingleLayerNet, self).__init__()
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        """Forward pass through the network."""
        x = self.flatten(x)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x


class TwoLayerNet(nn.Module):
    """Two-layer neural network for FashionMNIST classification."""

    def __init__(self, input_size=784, hidden_size1=128, hidden_size2=64, num_classes=10):
        """
        Initialize two-layer network.

        Args:
            input_size: Size of flattened input (28*28=784 for FashionMNIST)
            hidden_size1: Number of neurons in first hidden layer
            hidden_size2: Number of neurons in second hidden layer
            num_classes: Number of output classes (10 for FashionMNIST)
        """
        super(TwoLayerNet, self).__init__()
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(input_size, hidden_size1)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size1, hidden_size2)
        self.relu2 = nn.ReLU()
        self.fc3 = nn.Linear(hidden_size2, num_classes)

    def forward(self, x):
        """Forward pass through the network."""
        x = self.flatten(x)
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.fc2(x)
        x = self.relu2(x)
        x = self.fc3(x)
        return x


def create_model(model_type='single', hidden_size=128, hidden_size2=64):
    """
    Factory function to create models.

    Args:
        model_type: 'single' or 'two' layer network
        hidden_size: Size of (first) hidden layer
        hidden_size2: Size of second hidden layer (only for two-layer)

    Returns:
        Neural network model
    """
    if model_type == 'single':
        return SingleLayerNet(hidden_size=hidden_size)
    elif model_type == 'two':
        return TwoLayerNet(hidden_size1=hidden_size, hidden_size2=hidden_size2)
    else:
        raise ValueError(f"Unknown model_type: {model_type}")


def count_parameters(model):
    """Count trainable parameters in model."""
    return sum(p.numel() for p in model.parameters() if p.requires_grad)
