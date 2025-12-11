"""
Visualization functions for RNN/LSTM experiments.
"""

import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path


def load_all_results(results_dir='./results'):
    """Load all experiment results from JSON files."""
    results_dir = Path(results_dir)
    all_results = []

    for json_file in results_dir.glob('*.json'):
        if json_file.name == 'experiments_summary.json':
            continue

        with open(json_file, 'r') as f:
            raw = json.load(f)
            results = raw.get('results', {})
            history = results.get('history', {})

            # Flatten for easier plotting
            entry = {
                'filename': json_file.name,
                'config': raw.get('config', {}),
                'test_accuracy': results.get('test_accuracy'),
                'best_val_accuracy': results.get('best_val_accuracy'),
                'epochs_trained': results.get('epochs_trained'),
                'train_losses': history.get('train_loss', []),
                'val_losses': history.get('val_loss', []),
                'train_accuracies': history.get('train_accuracy', []),
                'val_accuracies': history.get('val_accuracy', []),
            }
            all_results.append(entry)

    return all_results


def plot_training_curves(results, save_path=None):
    """
    Plot training and validation curves for selected experiments.
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Group by RNN type
    lstm_results = [r for r in results if r['config']['rnn_type'] == 'LSTM']
    rnn_results = [r for r in results if r['config']['rnn_type'] == 'RNN']

    # Plot LSTM - Loss
    ax = axes[0, 0]
    for r in lstm_results[:5]:  # Plot first 5
        config = r['config']
        label = f"h={config['hidden_dim']}, len={config.get('max_len', 'full')}"
        epochs = range(1, len(r['train_losses']) + 1)
        ax.plot(epochs, r['train_losses'], '--', alpha=0.7)
        ax.plot(epochs, r['val_losses'], '-', label=label)
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Loss')
    ax.set_title('LSTM - Training & Validation Loss')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Plot LSTM - Accuracy
    ax = axes[0, 1]
    for r in lstm_results[:5]:
        config = r['config']
        label = f"h={config['hidden_dim']}, len={config.get('max_len', 'full')}"
        epochs = range(1, len(r['train_accuracies']) + 1)
        ax.plot(epochs, r['train_accuracies'], '--', alpha=0.7)
        ax.plot(epochs, r['val_accuracies'], '-', label=label)
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Accuracy')
    ax.set_title('LSTM - Training & Validation Accuracy')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Plot RNN - Loss
    ax = axes[1, 0]
    for r in rnn_results[:5]:
        config = r['config']
        label = f"h={config['hidden_dim']}, len={config.get('max_len', 'full')}"
        epochs = range(1, len(r['train_losses']) + 1)
        ax.plot(epochs, r['train_losses'], '--', alpha=0.7)
        ax.plot(epochs, r['val_losses'], '-', label=label)
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Loss')
    ax.set_title('RNN - Training & Validation Loss')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Plot RNN - Accuracy
    ax = axes[1, 1]
    for r in rnn_results[:5]:
        config = r['config']
        label = f"h={config['hidden_dim']}, len={config.get('max_len', 'full')}"
        epochs = range(1, len(r['train_accuracies']) + 1)
        ax.plot(epochs, r['train_accuracies'], '--', alpha=0.7)
        ax.plot(epochs, r['val_accuracies'], '-', label=label)
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Accuracy')
    ax.set_title('RNN - Training & Validation Accuracy')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")

    plt.close()


def plot_rnn_type_comparison(results, save_path=None):
    """
    Compare RNN vs LSTM performance.
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Prepare data
    data = []
    for r in results:
        config = r['config']
        data.append({
            'rnn_type': config['rnn_type'],
            'hidden_dim': config['hidden_dim'],
            'max_len': config.get('max_len', 'full'),
            'test_acc': r['test_accuracy'],
            'val_acc': r['best_val_accuracy'],
            'num_params': config['num_parameters']
        })

    df = pd.DataFrame(data)

    # Plot 1: Test accuracy by RNN type
    ax = axes[0]
    for rnn_type in ['RNN', 'LSTM']:
        subset = df[df['rnn_type'] == rnn_type]
        ax.scatter(subset['num_params'], subset['test_acc'],
                  label=rnn_type, alpha=0.7, s=100)
    ax.set_xlabel('Number of Parameters')
    ax.set_ylabel('Test Accuracy')
    ax.set_title('RNN vs LSTM Performance')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 2: Accuracy by hidden dimension
    ax = axes[1]
    hidden_dims = sorted(df['hidden_dim'].unique())
    rnn_means = [df[(df['rnn_type'] == 'RNN') & (df['hidden_dim'] == h)]['test_acc'].mean()
                 for h in hidden_dims]
    lstm_means = [df[(df['rnn_type'] == 'LSTM') & (df['hidden_dim'] == h)]['test_acc'].mean()
                  for h in hidden_dims]

    x = np.arange(len(hidden_dims))
    width = 0.35
    ax.bar(x - width/2, rnn_means, width, label='RNN', alpha=0.8)
    ax.bar(x + width/2, lstm_means, width, label='LSTM', alpha=0.8)
    ax.set_xlabel('Hidden Dimension')
    ax.set_ylabel('Mean Test Accuracy')
    ax.set_title('Effect of Hidden Dimension')
    ax.set_xticks(x)
    ax.set_xticklabels(hidden_dims)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')

    # Plot 3: Box plot comparison
    ax = axes[2]
    rnn_accs = df[df['rnn_type'] == 'RNN']['test_acc'].values
    lstm_accs = df[df['rnn_type'] == 'LSTM']['test_acc'].values

    bp = ax.boxplot([rnn_accs, lstm_accs], labels=['RNN', 'LSTM'],
                     patch_artist=True, showmeans=True)

    for patch, color in zip(bp['boxes'], ['lightblue', 'lightgreen']):
        patch.set_facecolor(color)

    ax.set_ylabel('Test Accuracy')
    ax.set_title('Accuracy Distribution')
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")

    plt.close()


def plot_truncation_effect(results, save_path=None):
    """
    Analyze effect of sequence truncation.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Prepare data
    data = []
    for r in results:
        config = r['config']
        max_len = config.get('max_len')
        max_len_str = 'full' if max_len is None else str(max_len)

        data.append({
            'rnn_type': config['rnn_type'],
            'hidden_dim': config['hidden_dim'],
            'max_len': max_len_str,
            'max_len_val': max_len if max_len is not None else 500,  # Use large value for full
            'test_acc': r['test_accuracy'],
            'epochs_trained': r['epochs_trained']
        })

    df = pd.DataFrame(data)

    # Plot 1: Accuracy vs sequence length
    ax = axes[0]
    for rnn_type in ['RNN', 'LSTM']:
        for hidden_dim in sorted(df['hidden_dim'].unique()):
            subset = df[(df['rnn_type'] == rnn_type) & (df['hidden_dim'] == hidden_dim)]
            subset = subset.sort_values('max_len_val')

            label = f"{rnn_type} (h={hidden_dim})"
            marker = 'o' if rnn_type == 'LSTM' else 's'
            ax.plot(subset['max_len'], subset['test_acc'],
                   marker=marker, label=label, linewidth=2, markersize=8)

    ax.set_xlabel('Maximum Sequence Length')
    ax.set_ylabel('Test Accuracy')
    ax.set_title('Effect of Sequence Truncation')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Plot 2: Training time (epochs) vs sequence length
    ax = axes[1]
    max_lens = sorted(df['max_len'].unique(), key=lambda x: (x == 'full', int(x) if x != 'full' else 0))

    rnn_epochs = [df[(df['rnn_type'] == 'RNN') & (df['max_len'] == ml)]['epochs_trained'].mean()
                  for ml in max_lens]
    lstm_epochs = [df[(df['rnn_type'] == 'LSTM') & (df['max_len'] == ml)]['epochs_trained'].mean()
                   for ml in max_lens]

    x = np.arange(len(max_lens))
    width = 0.35
    ax.bar(x - width/2, rnn_epochs, width, label='RNN', alpha=0.8)
    ax.bar(x + width/2, lstm_epochs, width, label='LSTM', alpha=0.8)
    ax.set_xlabel('Maximum Sequence Length')
    ax.set_ylabel('Average Epochs Trained')
    ax.set_title('Training Duration by Sequence Length')
    ax.set_xticks(x)
    ax.set_xticklabels(max_lens, rotation=45)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")

    plt.close()


def plot_hidden_dim_effect(results, save_path=None):
    """
    Analyze effect of hidden dimension.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Prepare data
    data = []
    for r in results:
        config = r['config']
        data.append({
            'rnn_type': config['rnn_type'],
            'hidden_dim': config['hidden_dim'],
            'test_acc': r['test_accuracy'],
            'num_params': config['num_parameters']
        })

    df = pd.DataFrame(data)

    # Plot 1: Accuracy vs hidden dimension
    ax = axes[0]
    hidden_dims = sorted(df['hidden_dim'].unique())

    for rnn_type in ['RNN', 'LSTM']:
        means = []
        stds = []
        for h in hidden_dims:
            subset = df[(df['rnn_type'] == rnn_type) & (df['hidden_dim'] == h)]['test_acc']
            means.append(subset.mean())
            stds.append(subset.std())

        ax.errorbar(hidden_dims, means, yerr=stds, marker='o',
                   label=rnn_type, linewidth=2, markersize=8, capsize=5)

    ax.set_xlabel('Hidden Dimension')
    ax.set_ylabel('Test Accuracy (mean ± std)')
    ax.set_title('Effect of Hidden Dimension')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 2: Accuracy vs parameters
    ax = axes[1]
    for rnn_type in ['RNN', 'LSTM']:
        subset = df[df['rnn_type'] == rnn_type]
        grouped = subset.groupby('hidden_dim')

        means = grouped['test_acc'].mean()
        params = grouped['num_params'].mean()

        ax.plot(params, means, marker='o', label=rnn_type,
               linewidth=2, markersize=8)

        # Add labels for hidden dimensions
        for h, p, a in zip(grouped.groups.keys(), params, means):
            ax.annotate(f'{h}', (p, a), textcoords="offset points",
                       xytext=(0,5), ha='center', fontsize=8)

    ax.set_xlabel('Number of Parameters')
    ax.set_ylabel('Test Accuracy')
    ax.set_title('Accuracy vs Model Size')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")

    plt.close()


def create_all_visualizations(results_dir='./results', output_dir='./results'):
    """
    Create all visualization plots.
    """
    print("Loading results...")
    results = load_all_results(results_dir)

    if not results:
        print("No results found!")
        return

    print(f"Found {len(results)} experiments")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\nCreating visualizations...")

    plot_training_curves(results, save_path=output_dir / 'training_curves.png')
    plot_rnn_type_comparison(results, save_path=output_dir / 'rnn_type_comparison.png')
    plot_truncation_effect(results, save_path=output_dir / 'truncation_effect.png')
    plot_hidden_dim_effect(results, save_path=output_dir / 'hidden_dim_effect.png')

    print("\nAll visualizations created!")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Create visualizations for RNN/LSTM experiments')
    parser.add_argument('--results', type=str, default='./results', help='Results directory')
    parser.add_argument('--output', type=str, default='./results', help='Output directory')

    args = parser.parse_args()

    create_all_visualizations(args.results, args.output)
