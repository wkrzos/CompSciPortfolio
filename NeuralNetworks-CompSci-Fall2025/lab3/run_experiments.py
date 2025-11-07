import numpy as np
import json
from pathlib import Path
from datetime import datetime

from layers import Linear, Activation
from activations import Softmax, ReLU, Sigmoid, Tanh
from network import NeuralNetwork
from data_utils import load_heart_disease_data


def get_activation(name):
    """Get activation function by name."""
    return {'relu': ReLU(), 'sigmoid': Sigmoid(), 'tanh': Tanh()}[name]


def build_network(input_dim, hidden_layers, n_classes, activation, weight_std):
    """Build neural network."""
    layers = []
    prev_size = input_dim
    
    for hidden_size in hidden_layers:
        layers.append(Linear(prev_size, hidden_size, weight_std=weight_std))
        layers.append(Activation(activation))
        prev_size = hidden_size
    
    layers.append(Linear(prev_size, n_classes, weight_std=weight_std))
    layers.append(Activation(Softmax()))
    
    return NeuralNetwork(layers)


def run_experiment(config, x_train, y_train, x_test, y_test, input_dim, n_classes):
    """Run a single training experiment with given configuration.
    
    Args:
        config: Dictionary with hyperparameters
        x_train, y_train: Training data
        x_test, y_test: Test data
        input_dim: Number of input features
        n_classes: Number of output classes
        
    Returns:
        Dictionary with results
    """
    print(f"\nRunning: {config['name']}")
    print(f"  Config: {config}")
    
    # Set seed for reproducibility
    np.random.seed(42)
    
    # Build network
    activation = get_activation(config.get('activation', 'relu'))
    network = build_network(
        input_dim=input_dim,
        hidden_layers=config['hidden_layers'],
        n_classes=n_classes,
        activation=activation,
        weight_std=config.get('weight_std', 0.01)
    )
    
    # Train
    network.fit(
        x_train, y_train,
        x_val=x_test, y_val=y_test,
        epochs=config.get('epochs', 100),
        learning_rate=config.get('learning_rate', 0.01),
        batch_size=config.get('batch_size', 32),
        verbose=False
    )
    
    # Evaluate
    train_loss, train_acc = network.evaluate(x_train, y_train)
    test_loss, test_acc = network.evaluate(x_test, y_test)
    
    results = {
        'config': config,
        'train_loss': float(train_loss),
        'train_accuracy': float(train_acc),
        'test_loss': float(test_loss),
        'test_accuracy': float(test_acc),
        'train_losses': [float(x) for x in network.train_losses],
        'test_losses': [float(x) for x in network.val_losses],
        'train_accuracies': [float(x) for x in network.train_accuracies],
        'test_accuracies': [float(x) for x in network.val_accuracies],
    }
    
    print(f"  Results: Train Acc={train_acc:.4f}, Test Acc={test_acc:.4f}")
    
    return results


def main():
    """Run all experiments."""
    print("=" * 70)
    print("Neural Network Experiments - Heart Disease Dataset")
    print("=" * 70)
    
    # Load data (normalized version)
    print("\nLoading normalized data...")
    x_train_norm, y_train, x_test_norm, y_test, _ = load_heart_disease_data(
        normalize=True, random_state=42
    )
    
    # Load data (unnormalized version)
    print("\nLoading unnormalized data...")
    x_train_unnorm, _, x_test_unnorm, _, _ = load_heart_disease_data(
        normalize=False, random_state=42
    )
    
    input_dim = x_train_norm.shape[1]
    n_classes = y_train.shape[1]
    
    # Define experiments
    experiments = [
        # Baseline
        {
            'name': 'baseline',
            'hidden_layers': [32],
            'learning_rate': 0.01,
            'weight_std': 0.01,
            'activation': 'relu',
            'epochs': 100,
        },
        
        # Different hidden layer sizes
        {
            'name': 'hidden_8',
            'hidden_layers': [8],
            'learning_rate': 0.01,
            'weight_std': 0.01,
            'activation': 'relu',
            'epochs': 100,
        },
        {
            'name': 'hidden_64',
            'hidden_layers': [64],
            'learning_rate': 0.01,
            'weight_std': 0.01,
            'activation': 'relu',
            'epochs': 100,
        },
        {
            'name': 'hidden_128',
            'hidden_layers': [128],
            'learning_rate': 0.01,
            'weight_std': 0.01,
            'activation': 'relu',
            'epochs': 100,
        },
        
        # Different learning rates
        {
            'name': 'lr_0.001',
            'hidden_layers': [32],
            'learning_rate': 0.001,
            'weight_std': 0.01,
            'activation': 'relu',
            'epochs': 100,
        },
        {
            'name': 'lr_0.1',
            'hidden_layers': [32],
            'learning_rate': 0.1,
            'weight_std': 0.01,
            'activation': 'relu',
            'epochs': 100,
        },
        {
            'name': 'lr_0.5',
            'hidden_layers': [32],
            'learning_rate': 0.5,
            'weight_std': 0.01,
            'activation': 'relu',
            'epochs': 100,
        },
        
        # Different weight initializations
        {
            'name': 'weight_std_0.001',
            'hidden_layers': [32],
            'learning_rate': 0.01,
            'weight_std': 0.001,
            'activation': 'relu',
            'epochs': 100,
        },
        {
            'name': 'weight_std_0.1',
            'hidden_layers': [32],
            'learning_rate': 0.01,
            'weight_std': 0.1,
            'activation': 'relu',
            'epochs': 100,
        },
        {
            'name': 'weight_std_1.0',
            'hidden_layers': [32],
            'learning_rate': 0.01,
            'weight_std': 1.0,
            'activation': 'relu',
            'epochs': 100,
        },
        
        # Different number of layers
        {
            'name': 'layers_2',
            'hidden_layers': [32, 16],
            'learning_rate': 0.01,
            'weight_std': 0.01,
            'activation': 'relu',
            'epochs': 100,
        },
        {
            'name': 'layers_3',
            'hidden_layers': [64, 32, 16],
            'learning_rate': 0.01,
            'weight_std': 0.01,
            'activation': 'relu',
            'epochs': 100,
        },
    ]
    
    # Run experiments on normalized data
    print("\n" + "=" * 70)
    print("Running experiments with NORMALIZED data")
    print("=" * 70)
    
    results_normalized = []
    for config in experiments:
        result = run_experiment(
            config, x_train_norm, y_train, x_test_norm, y_test,
            input_dim, n_classes
        )
        results_normalized.append(result)
    
    # Run baseline on unnormalized data
    print("\n" + "=" * 70)
    print("Running experiment with UNNORMALIZED data")
    print("=" * 70)
    
    baseline_unnorm = {
        'name': 'baseline_unnormalized',
        'hidden_layers': [32],
        'learning_rate': 0.01,
        'weight_std': 0.01,
        'activation': 'relu',
        'epochs': 100,
    }
    
    result_unnorm = run_experiment(
        baseline_unnorm, x_train_unnorm, y_train, x_test_unnorm, y_test,
        input_dim, n_classes
    )
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = Path('results')
    results_dir.mkdir(exist_ok=True)
    
    output_file = results_dir / f'experiments_{timestamp}.json'
    
    all_results = {
        'normalized': results_normalized,
        'unnormalized': result_unnorm,
        'timestamp': timestamp,
    }
    
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n\nResults saved to: {output_file}")
    
    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY - Normalized Data")
    print("=" * 70)
    print(f"{'Experiment':<25} {'Train Acc':<12} {'Test Acc':<12} {'Gap':<8}")
    print("-" * 70)
    
    for result in results_normalized:
        name = result['config']['name']
        train_acc = result['train_accuracy']
        test_acc = result['test_accuracy']
        gap = train_acc - test_acc
        print(f"{name:<25} {train_acc:<12.4f} {test_acc:<12.4f} {gap:<8.4f}")
    
    print("\n" + "=" * 70)
    print("UNNORMALIZED vs NORMALIZED")
    print("=" * 70)
    
    baseline_norm = results_normalized[0]
    print(f"Normalized   - Test Acc: {baseline_norm['test_accuracy']:.4f}")
    print(f"Unnormalized - Test Acc: {result_unnorm['test_accuracy']:.4f}")
    
    print("\n" + "=" * 70)


if __name__ == '__main__':
    main()
