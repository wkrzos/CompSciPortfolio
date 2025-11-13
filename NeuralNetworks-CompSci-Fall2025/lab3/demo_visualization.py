#!/usr/bin/env python3
"""
Demo script showing visualization capabilities.

This script trains a simple network and generates all available plots.
"""

# THIS SCRIPT SHOULD NOT BE ATTACHED TO THE FINAL REPORT
# IT IS FOR TESTING PURPOSES ONLY AND WAS AUTO GENERATED

import numpy as np
from pathlib import Path

from layers import Linear, Activation
from activations import Softmax, ReLU
from network import NeuralNetwork
from data_utils import load_heart_disease_data
from visualization import (
    plot_learning_curves,
    plot_confusion_matrix,
    plot_weight_distribution,
    plot_training_summary
)


def main():
    print("=" * 70)
    print("Visualization Demo - Neural Network Training")
    print("=" * 70)
    
    # Set seed
    np.random.seed(42)
    
    # Load data
    print("\n[1] Loading data...")
    x_train, y_train, x_test, y_test, _ = load_heart_disease_data(
        normalize=True,
        random_state=42
    )
    
    input_dim = x_train.shape[1]
    n_classes = y_train.shape[1]
    
    # Build network
    print("[2] Building network: [13, 32, 16, 2]")
    layers = [
        Linear(input_dim, 32, weight_std=0.1),
        Activation(ReLU()),
        Linear(32, 16, weight_std=0.1),
        Activation(ReLU()),
        Linear(16, n_classes, weight_std=0.1),
        Activation(Softmax())
    ]
    network = NeuralNetwork(layers)
    
    # Train
    print("[3] Training for 150 epochs...")
    network.fit(
        x_train, y_train,
        x_val=x_test, y_val=y_test,
        epochs=150,
        learning_rate=0.1,
        batch_size=32,
        verbose=True
    )
    
    # Evaluate
    print("\n[4] Evaluating...")
    train_loss, train_acc = network.evaluate(x_train, y_train)
    test_loss, test_acc = network.evaluate(x_test, y_test)
    
    print(f"\nFinal Results:")
    print(f"  Training Accuracy: {train_acc:.4f} ({train_acc*100:.2f}%)")
    print(f"  Test Accuracy: {test_acc:.4f} ({test_acc*100:.2f}%)")
    
    # Generate all visualizations
    print("\n[5] Generating visualizations...")
    results_dir = Path('demo_results')
    results_dir.mkdir(exist_ok=True)
    
    # Get predictions
    train_pred = network.predict(x_train)
    test_pred = network.predict(x_test)
    
    y_train_true = np.argmax(y_train, axis=1)
    y_train_pred = np.argmax(train_pred, axis=1)
    y_test_true = np.argmax(y_test, axis=1)
    y_test_pred = np.argmax(test_pred, axis=1)
    
    # Generate comprehensive summary
    plot_training_summary(
        network=network,
        y_train_true=y_train_true,
        y_train_pred=y_train_pred,
        y_test_true=y_test_true,
        y_test_pred=y_test_pred,
        class_names=['Healthy (0)', 'Disease (1)'],
        save_dir=results_dir,
        prefix='demo'
    )
    
    print("\n" + "=" * 70)
    print(f"All plots saved to: {results_dir}/")
    print("=" * 70)
    print("\nGenerated files:")
    for file in sorted(results_dir.glob('*.png')):
        print(f"  - {file.name}")
    print()


if __name__ == '__main__':
    main()
