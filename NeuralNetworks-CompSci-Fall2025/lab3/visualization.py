"""
Visualization utilities for neural network training analysis.

This module provides functions to generate various plots for analyzing
training progress, including learning curves, accuracy plots, confusion
matrices, and weight distributions.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for server environments
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.metrics import confusion_matrix


def plot_learning_curves(train_losses, val_losses=None, 
                         train_accs=None, val_accs=None,
                         save_path='learning_curves.png',
                         title='Learning Curves'):
    """Plot training and validation loss/accuracy curves.
    
    Args:
        train_losses: List of training losses per epoch
        val_losses: List of validation losses per epoch (optional)
        train_accs: List of training accuracies per epoch (optional)
        val_accs: List of validation accuracies per epoch (optional)
        save_path: Path to save the plot
        title: Title for the plot
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    epochs = range(1, len(train_losses) + 1)
    
    # Plot loss
    axes[0].plot(epochs, train_losses, 'b-', linewidth=2, label='Training Loss')
    if val_losses:
        axes[0].plot(epochs, val_losses, 'r-', linewidth=2, label='Validation Loss')
    axes[0].set_xlabel('Epoch', fontsize=12)
    axes[0].set_ylabel('Loss', fontsize=12)
    axes[0].set_title('Loss over Epochs', fontsize=14, fontweight='bold')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Plot accuracy
    if train_accs:
        axes[1].plot(epochs, train_accs, 'b-', linewidth=2, label='Training Accuracy')
    if val_accs:
        axes[1].plot(epochs, val_accs, 'r-', linewidth=2, label='Validation Accuracy')
    if train_accs or val_accs:
        axes[1].set_xlabel('Epoch', fontsize=12)
        axes[1].set_ylabel('Accuracy', fontsize=12)
        axes[1].set_title('Accuracy over Epochs', fontsize=14, fontweight='bold')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        axes[1].set_ylim([0, 1.05])
    
    plt.suptitle(title, fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ Learning curves saved to: {save_path}")


def plot_confusion_matrix(y_true, y_pred, class_names=None,
                          save_path='confusion_matrix.png',
                          title='Confusion Matrix'):
    """Plot confusion matrix.
    
    Args:
        y_true: True labels (1D array of class indices)
        y_pred: Predicted labels (1D array of class indices)
        class_names: List of class names (optional)
        save_path: Path to save the plot
        title: Title for the plot
    """
    cm = confusion_matrix(y_true, y_pred)
    n_classes = cm.shape[0]
    
    if class_names is None:
        class_names = [f'Class {i}' for i in range(n_classes)]
    
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax)
    
    ax.set(xticks=np.arange(n_classes),
           yticks=np.arange(n_classes),
           xticklabels=class_names,
           yticklabels=class_names,
           title=title,
           ylabel='True Label',
           xlabel='Predicted Label')
    
    # Rotate the tick labels
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    # Add text annotations
    thresh = cm.max() / 2.
    for i in range(n_classes):
        for j in range(n_classes):
            ax.text(j, i, format(cm[i, j], 'd'),
                   ha="center", va="center",
                   color="white" if cm[i, j] > thresh else "black",
                   fontsize=16, fontweight='bold')
    
    fig.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ Confusion matrix saved to: {save_path}")


def plot_loss_comparison(results_dict, save_path='loss_comparison.png',
                        title='Loss Comparison Across Configurations'):
    """Plot loss curves for multiple configurations.
    
    Args:
        results_dict: Dictionary mapping config names to loss lists
        save_path: Path to save the plot
        title: Title for the plot
    """
    fig, ax = plt.subplots(figsize=(12, 7))
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(results_dict)))
    
    for (config_name, losses), color in zip(results_dict.items(), colors):
        epochs = range(1, len(losses) + 1)
        ax.plot(epochs, losses, linewidth=2, label=config_name, color=color)
    
    ax.set_xlabel('Epoch', fontsize=12)
    ax.set_ylabel('Loss', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ Loss comparison saved to: {save_path}")


def plot_accuracy_comparison(results_dict, save_path='accuracy_comparison.png',
                            title='Accuracy Comparison Across Configurations'):
    """Plot accuracy curves for multiple configurations.
    
    Args:
        results_dict: Dictionary mapping config names to accuracy lists
        save_path: Path to save the plot
        title: Title for the plot
    """
    fig, ax = plt.subplots(figsize=(12, 7))
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(results_dict)))
    
    for (config_name, accs), color in zip(results_dict.items(), colors):
        epochs = range(1, len(accs) + 1)
        ax.plot(epochs, accs, linewidth=2, label=config_name, color=color)
    
    ax.set_xlabel('Epoch', fontsize=12)
    ax.set_ylabel('Accuracy', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_ylim([0, 1.05])
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ Accuracy comparison saved to: {save_path}")


def plot_weight_distribution(network, save_path='weight_distribution.png',
                             title='Weight Distribution'):
    """Plot histogram of all weights in the network.
    
    Args:
        network: NeuralNetwork object
        save_path: Path to save the plot
        title: Title for the plot
    """
    all_weights = []
    layer_names = []
    
    for i, layer in enumerate(network.layers):
        if hasattr(layer, 'W'):
            all_weights.append(layer.W.flatten())
            layer_names.append(f'Layer {i//2 + 1}')
    
    fig, axes = plt.subplots(1, len(all_weights), figsize=(5*len(all_weights), 5))
    if len(all_weights) == 1:
        axes = [axes]
    
    for ax, weights, name in zip(axes, all_weights, layer_names):
        ax.hist(weights, bins=50, alpha=0.7, color='steelblue', edgecolor='black')
        ax.set_xlabel('Weight Value', fontsize=11)
        ax.set_ylabel('Frequency', fontsize=11)
        ax.set_title(f'{name}\n(μ={weights.mean():.4f}, σ={weights.std():.4f})',
                    fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
    
    plt.suptitle(title, fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ Weight distribution saved to: {save_path}")


def plot_gradient_flow(network, save_path='gradient_flow.png',
                      title='Gradient Flow Through Layers'):
    """Plot gradient magnitudes across layers.
    
    Args:
        network: NeuralNetwork object (after backward pass)
        save_path: Path to save the plot
        title: Title for the plot
    """
    layer_names = []
    grad_means = []
    grad_stds = []
    
    for i, layer in enumerate(network.layers):
        if hasattr(layer, 'grad_W') and layer.grad_W is not None:
            grad_flat = layer.grad_W.flatten()
            layer_names.append(f'Layer {i//2 + 1}')
            grad_means.append(np.abs(grad_flat).mean())
            grad_stds.append(np.abs(grad_flat).std())
    
    if not layer_names:
        print("⚠ No gradients available. Run training first.")
        return
    
    fig, ax = plt.subplots(figsize=(10, 6))
    x_pos = np.arange(len(layer_names))
    
    ax.bar(x_pos, grad_means, yerr=grad_stds, alpha=0.7, 
           color='steelblue', capsize=5, edgecolor='black')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(layer_names)
    ax.set_ylabel('Mean Absolute Gradient', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ Gradient flow saved to: {save_path}")


def plot_training_summary(network, y_train_true, y_train_pred,
                         y_test_true, y_test_pred,
                         class_names=None,
                         save_dir='results',
                         prefix='training'):
    """Generate a comprehensive set of plots for training analysis.
    
    Args:
        network: Trained NeuralNetwork object
        y_train_true: True training labels (class indices)
        y_train_pred: Predicted training labels (class indices)
        y_test_true: True test labels (class indices)
        y_test_pred: Predicted test labels (class indices)
        class_names: List of class names (optional)
        save_dir: Directory to save plots
        prefix: Prefix for saved files
    """
    # Create results directory
    save_dir = Path(save_dir)
    save_dir.mkdir(exist_ok=True)
    
    print("\n" + "="*70)
    print("Generating visualizations...")
    print("="*70)
    
    # 1. Learning curves
    if network.train_losses:
        plot_learning_curves(
            train_losses=network.train_losses,
            val_losses=network.val_losses if network.val_losses else None,
            train_accs=network.train_accuracies if network.train_accuracies else None,
            val_accs=network.val_accuracies if network.val_accuracies else None,
            save_path=save_dir / f'{prefix}_learning_curves.png',
            title='Neural Network Training Progress'
        )
    
    # 2. Confusion matrices
    if class_names is None:
        class_names = ['Healthy', 'Disease']
    
    plot_confusion_matrix(
        y_train_true, y_train_pred,
        class_names=class_names,
        save_path=save_dir / f'{prefix}_confusion_train.png',
        title='Confusion Matrix - Training Set'
    )
    
    plot_confusion_matrix(
        y_test_true, y_test_pred,
        class_names=class_names,
        save_path=save_dir / f'{prefix}_confusion_test.png',
        title='Confusion Matrix - Test Set'
    )
    
    # 3. Weight distribution
    plot_weight_distribution(
        network,
        save_path=save_dir / f'{prefix}_weight_distribution.png',
        title='Weight Distribution Across Layers'
    )
    
    print("="*70)
    print(f"All visualizations saved to: {save_dir}/")
    print("="*70)


def save_experiment_comparison(experiments, save_dir='results'):
    """Save comparison plots for multiple experiments.
    
    Args:
        experiments: List of dicts with keys 'name', 'train_losses', 'val_losses', 
                    'train_accs', 'val_accs'
        save_dir: Directory to save plots
    """
    save_dir = Path(save_dir)
    save_dir.mkdir(exist_ok=True)
    
    # Extract data
    train_losses = {exp['name']: exp['train_losses'] for exp in experiments}
    val_losses = {exp['name']: exp['val_losses'] for exp in experiments if exp['val_losses']}
    train_accs = {exp['name']: exp['train_accs'] for exp in experiments if exp['train_accs']}
    val_accs = {exp['name']: exp['val_accs'] for exp in experiments if exp['val_accs']}
    
    # Plot comparisons
    if train_losses:
        plot_loss_comparison(
            train_losses,
            save_path=save_dir / 'comparison_train_loss.png',
            title='Training Loss Comparison'
        )
    
    if val_losses:
        plot_loss_comparison(
            val_losses,
            save_path=save_dir / 'comparison_val_loss.png',
            title='Validation Loss Comparison'
        )
    
    if val_accs:
        plot_accuracy_comparison(
            val_accs,
            save_path=save_dir / 'comparison_val_accuracy.png',
            title='Validation Accuracy Comparison'
        )
