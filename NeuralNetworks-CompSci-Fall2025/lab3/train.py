"""
Command-line interface for training neural network on heart disease dataset.

This script allows configuring various hyperparameters and training a
multi-layer neural network using pure matrix operations and backpropagation.
"""

import argparse
import numpy as np
from pathlib import Path

from layers import Linear, Activation
from activations import Softmax, ReLU, Sigmoid, Tanh
from network import NeuralNetwork
from data_utils import load_heart_disease_data


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Train neural network on heart disease dataset'
    )
    
    # Data parameters
    parser.add_argument('--data', type=str, default='processed_heart_cleveland.csv',
                       help='Path to data file')
    parser.add_argument('--normalize', action='store_true', default=True,
                       help='Normalize input features (default: True)')
    parser.add_argument('--no-normalize', dest='normalize', action='store_false',
                       help='Do not normalize input features')
    
    # Network architecture
    parser.add_argument('--hidden-layers', type=int, nargs='+', default=[32],
                       help='Hidden layer sizes (e.g., 32 64 32)')
    parser.add_argument('--activation', type=str, default='relu',
                       choices=['relu', 'sigmoid', 'tanh'],
                       help='Activation function for hidden layers')
    
    # Training parameters
    parser.add_argument('--learning-rate', type=float, default=0.01,
                       help='Learning rate (default: 0.01)')
    parser.add_argument('--epochs', type=int, default=100,
                       help='Number of training epochs (default: 100)')
    parser.add_argument('--batch-size', type=int, default=32,
                       help='Batch size (default: 32)')
    parser.add_argument('--weight-std', type=float, default=0.01,
                       help='Standard deviation for weight initialization (default: 0.01)')
    
    # Other
    parser.add_argument('--seed', type=int, default=42,
                       help='Random seed (default: 42)')
    parser.add_argument('--quiet', action='store_true',
                       help='Suppress training output')
    
    return parser.parse_args()


def get_activation_function(name):
    """Get activation function object by name."""
    activations = {
        'relu': ReLU(),
        'sigmoid': Sigmoid(),
        'tanh': Tanh(),
    }
    return activations[name.lower()]


def build_network(input_dim, hidden_layers, n_classes, activation, weight_std):
    """Build neural network architecture.
    
    Args:
        input_dim: Number of input features
        hidden_layers: List of hidden layer sizes
        n_classes: Number of output classes
        activation: Activation function object for hidden layers
        weight_std: Standard deviation for weight initialization
        
    Returns:
        NeuralNetwork object
    """
    layers = []
    
    # Input layer to first hidden layer
    prev_size = input_dim
    for hidden_size in hidden_layers:
        layers.append(Linear(prev_size, hidden_size, weight_std=weight_std))
        layers.append(Activation(activation))
        prev_size = hidden_size
    
    # Last hidden layer to output
    layers.append(Linear(prev_size, n_classes, weight_std=weight_std))
    layers.append(Activation(Softmax()))
    
    return NeuralNetwork(layers)


def main():
    """Main training function."""
    args = parse_args()
    
    # Set random seed
    np.random.seed(args.seed)
    
    print("=" * 70)
    print("Neural Network Training - Heart Disease Classification")
    print("=" * 70)
    
    # Load data
    print("\n[1] Loading data...")
    x_train, y_train, x_test, y_test, feature_names = load_heart_disease_data(
        data_path=args.data,
        normalize=args.normalize,
        test_size=0.2,
        random_state=args.seed
    )
    
    input_dim = x_train.shape[1]
    n_classes = y_train.shape[1]
    
    # Build network
    print("\n[2] Building network...")
    activation = get_activation_function(args.activation)
    network = build_network(
        input_dim=input_dim,
        hidden_layers=args.hidden_layers,
        n_classes=n_classes,
        activation=activation,
        weight_std=args.weight_std
    )
    
    # Print architecture
    print(f"\nNetwork architecture:")
    print(f"  Input: {input_dim} features")
    for i, size in enumerate(args.hidden_layers, 1):
        print(f"  Hidden layer {i}: {size} neurons ({args.activation})")
    print(f"  Output: {n_classes} classes (softmax)")
    print(f"  Total parameters: {network.get_parameter_count()}")
    
    # Print hyperparameters
    print(f"\nHyperparameters:")
    print(f"  Learning rate: {args.learning_rate}")
    print(f"  Batch size: {args.batch_size}")
    print(f"  Epochs: {args.epochs}")
    print(f"  Weight init std: {args.weight_std}")
    print(f"  Normalization: {args.normalize}")
    
    # Train
    print("\n[3] Training...")
    print("-" * 70)
    
    network.fit(
        x_train, y_train,
        x_val=x_test, y_val=y_test,
        epochs=args.epochs,
        learning_rate=args.learning_rate,
        batch_size=args.batch_size,
        verbose=not args.quiet
    )
    
    # Final evaluation
    print("\n" + "=" * 70)
    print("[4] Final Results")
    print("=" * 70)
    
    train_loss, train_acc = network.evaluate(x_train, y_train)
    test_loss, test_acc = network.evaluate(x_test, y_test)
    
    print(f"\nTraining Set:")
    print(f"  Loss: {train_loss:.4f}")
    print(f"  Accuracy: {train_acc:.4f} ({train_acc*100:.2f}%)")
    
    print(f"\nTest Set:")
    print(f"  Loss: {test_loss:.4f}")
    print(f"  Accuracy: {test_acc:.4f} ({test_acc*100:.2f}%)")
    
    # Check for overfitting
    if train_acc - test_acc > 0.1:
        print("\n⚠ Warning: Significant gap between train and test accuracy.")
        print("  This might indicate overfitting.")
    
    print("\n" + "=" * 70)


if __name__ == '__main__':
    main()
