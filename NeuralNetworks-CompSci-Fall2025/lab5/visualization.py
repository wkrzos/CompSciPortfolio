"""
Visualization functions for FashionMNIST experiment results.
Creates plots for learning curves and performance comparisons.
"""

import matplotlib.pyplot as plt
import json
import os
import numpy as np
from matplotlib.gridspec import GridSpec


def plot_learning_curves(history, title='Learning Curves', save_path=None):
    """
    Plot training and test loss/accuracy curves.

    Args:
        history: Dictionary with training history
        title: Plot title
        save_path: Path to save figure (optional)
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    epochs = range(1, len(history['train_loss']) + 1)

    # Loss curves
    ax1.plot(epochs, history['train_loss'], 'b-', label='Train Loss', linewidth=2)
    ax1.plot(epochs, history['test_loss'], 'r-', label='Test Loss', linewidth=2)
    ax1.set_xlabel('Epoch', fontsize=12)
    ax1.set_ylabel('Loss', fontsize=12)
    ax1.set_title('Loss Curves', fontsize=14)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)

    # Accuracy curves
    ax2.plot(epochs, history['train_acc'], 'b-', label='Train Accuracy', linewidth=2)
    ax2.plot(epochs, history['test_acc'], 'r-', label='Test Accuracy', linewidth=2)
    ax2.set_xlabel('Epoch', fontsize=12)
    ax2.set_ylabel('Accuracy (%)', fontsize=12)
    ax2.set_title('Accuracy Curves', fontsize=14)
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)

    fig.suptitle(title, fontsize=16, fontweight='bold')
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved plot to {save_path}")
    else:
        plt.show()

    plt.close()


def plot_comparison(results_list, comparison_type='hidden_size', save_path=None):
    """
    Plot comparison of multiple experiments.

    Args:
        results_list: List of result dictionaries
        comparison_type: Type of comparison (hidden_size, batch_size, data_size, noise)
        save_path: Path to save figure (optional)
    """
    fig = plt.figure(figsize=(16, 10))
    gs = GridSpec(2, 2, figure=fig)

    ax1 = fig.add_subplot(gs[0, 0])  # Train accuracy curves
    ax2 = fig.add_subplot(gs[0, 1])  # Test accuracy curves
    ax3 = fig.add_subplot(gs[1, 0])  # Final accuracy comparison
    ax4 = fig.add_subplot(gs[1, 1])  # Loss curves

    # Filter results for single and two-layer networks
    single_layer_results = [r for r in results_list if r['config']['model_type'] == 'single']
    two_layer_results = [r for r in results_list if r['config']['model_type'] == 'two']

    # Plot train accuracy curves
    for result in single_layer_results:
        label = get_label(result['config'], comparison_type)
        ax1.plot(result['history']['train_acc'], label=f'Single: {label}', linewidth=2)
    for result in two_layer_results:
        label = get_label(result['config'], comparison_type)
        ax1.plot(result['history']['train_acc'], '--', label=f'Two: {label}', linewidth=2)

    ax1.set_xlabel('Epoch', fontsize=12)
    ax1.set_ylabel('Train Accuracy (%)', fontsize=12)
    ax1.set_title('Training Accuracy', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)

    # Plot test accuracy curves
    for result in single_layer_results:
        label = get_label(result['config'], comparison_type)
        ax2.plot(result['history']['test_acc'], label=f'Single: {label}', linewidth=2)
    for result in two_layer_results:
        label = get_label(result['config'], comparison_type)
        ax2.plot(result['history']['test_acc'], '--', label=f'Two: {label}', linewidth=2)

    ax2.set_xlabel('Epoch', fontsize=12)
    ax2.set_ylabel('Test Accuracy (%)', fontsize=12)
    ax2.set_title('Test Accuracy', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)

    # Bar plot of final accuracies
    labels = []
    single_accs = []
    two_accs = []

    for result in single_layer_results:
        labels.append(get_label(result['config'], comparison_type))
        single_accs.append(result['final_test_acc'])

    for result in two_layer_results:
        two_accs.append(result['final_test_acc'])

    x = np.arange(len(labels))
    width = 0.35

    ax3.bar(x - width/2, single_accs, width, label='Single Layer', alpha=0.8)
    ax3.bar(x + width/2, two_accs, width, label='Two Layer', alpha=0.8)

    ax3.set_xlabel(comparison_type.replace('_', ' ').title(), fontsize=12)
    ax3.set_ylabel('Final Test Accuracy (%)', fontsize=12)
    ax3.set_title('Final Test Accuracy Comparison', fontsize=14, fontweight='bold')
    ax3.set_xticks(x)
    ax3.set_xticklabels(labels, rotation=45, ha='right')
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3, axis='y')

    # Plot test loss curves
    for result in single_layer_results:
        label = get_label(result['config'], comparison_type)
        ax4.plot(result['history']['test_loss'], label=f'Single: {label}', linewidth=2)
    for result in two_layer_results:
        label = get_label(result['config'], comparison_type)
        ax4.plot(result['history']['test_loss'], '--', label=f'Two: {label}', linewidth=2)

    ax4.set_xlabel('Epoch', fontsize=12)
    ax4.set_ylabel('Test Loss', fontsize=12)
    ax4.set_title('Test Loss', fontsize=14, fontweight='bold')
    ax4.legend(fontsize=9)
    ax4.grid(True, alpha=0.3)

    title = f'Comparison: {comparison_type.replace("_", " ").title()}'
    fig.suptitle(title, fontsize=18, fontweight='bold')
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved comparison plot to {save_path}")
    else:
        plt.show()

    plt.close()


def get_label(config, comparison_type):
    """
    Generate label for plot based on comparison type.

    Args:
        config: Experiment configuration
        comparison_type: Type of comparison

    Returns:
        Label string
    """
    if comparison_type == 'hidden_size':
        return f"H={config['hidden_size']}"
    elif comparison_type == 'batch_size':
        return f"BS={config['batch_size']}"
    elif comparison_type == 'data_size':
        return f"{int(config['data_fraction']*100)}%"
    elif comparison_type == 'noise':
        noise_type = 'Train+Test' if config['noise_train'] else 'Test only'
        return f"σ={config['noise_std']} ({noise_type})"
    else:
        return config['name']


def load_results(results_dir, pattern=''):
    """
    Load all result files matching pattern.

    Args:
        results_dir: Directory containing result files
        pattern: Pattern to match in filenames

    Returns:
        List of result dictionaries
    """
    results = []

    for filename in os.listdir(results_dir):
        if filename.endswith('_results.json') and pattern in filename:
            filepath = os.path.join(results_dir, filename)
            with open(filepath, 'r') as f:
                result = json.load(f)
                results.append(result)

    return results


def create_all_visualizations(results_dir='results', output_dir='results/plots'):
    """
    Create all visualization plots from experiment results.

    Args:
        results_dir: Directory containing result files
        output_dir: Directory to save plots
    """
    os.makedirs(output_dir, exist_ok=True)

    print("Creating visualizations...")

    # 1. Individual learning curves for baseline
    print("\n1. Creating baseline learning curves...")
    baseline_results = load_results(results_dir, 'baseline')
    for result in baseline_results:
        name = result['config']['name']
        plot_learning_curves(
            result['history'],
            title=f"Learning Curves: {name}",
            save_path=os.path.join(output_dir, f'{name}_learning_curves.png')
        )

    # 2. Hidden size comparison
    print("\n2. Creating hidden size comparison...")
    hidden_size_results = load_results(results_dir, '_h')
    if hidden_size_results:
        plot_comparison(
            hidden_size_results,
            comparison_type='hidden_size',
            save_path=os.path.join(output_dir, 'hidden_size_comparison.png')
        )

    # 3. Batch size comparison
    print("\n3. Creating batch size comparison...")
    batch_size_results = load_results(results_dir, '_bs')
    if batch_size_results:
        plot_comparison(
            batch_size_results,
            comparison_type='batch_size',
            save_path=os.path.join(output_dir, 'batch_size_comparison.png')
        )

    # 4. Data size comparison
    print("\n4. Creating data size comparison...")
    data_size_results = load_results(results_dir, '_data')
    if data_size_results:
        plot_comparison(
            data_size_results,
            comparison_type='data_size',
            save_path=os.path.join(output_dir, 'data_size_comparison.png')
        )

    # 5. Noise comparison - test only
    print("\n5. Creating noise (test only) comparison...")
    noise_test_results = load_results(results_dir, '_testonly')
    if noise_test_results:
        plot_comparison(
            noise_test_results,
            comparison_type='noise',
            save_path=os.path.join(output_dir, 'noise_testonly_comparison.png')
        )

    # 6. Noise comparison - train and test
    print("\n6. Creating noise (train+test) comparison...")
    noise_train_results = load_results(results_dir, '_traintest')
    if noise_train_results:
        plot_comparison(
            noise_train_results,
            comparison_type='noise',
            save_path=os.path.join(output_dir, 'noise_traintest_comparison.png')
        )

    print(f"\nAll visualizations saved to {output_dir}")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Create visualizations from experiment results')
    parser.add_argument('--results-dir', type=str, default='results',
                       help='Directory containing result files')
    parser.add_argument('--output-dir', type=str, default='results/plots',
                       help='Directory to save plots')

    args = parser.parse_args()

    create_all_visualizations(args.results_dir, args.output_dir)
