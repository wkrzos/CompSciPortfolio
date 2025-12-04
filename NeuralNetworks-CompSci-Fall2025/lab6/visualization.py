import json
import os
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import pandas as pd


def load_all_results(results_dir='./results'):
    """
    Load all experiment results from directory.

    Args:
        results_dir: Directory with JSON result files

    Returns:
        List of (filename, config, results) tuples
    """
    all_results = []

    for file in sorted(Path(results_dir).glob('*.json')):
        if 'summary' in file.name:
            continue

        try:
            with open(file, 'r') as f:
                data = json.load(f)
            all_results.append((file.name, data['config'], data['results']))
        except Exception as e:
            print(f"Error loading {file}: {e}")

    return all_results


def create_comparison_plots(results_dir='./results', output_dir='./results'):
    """
    Create comparison plots for different parameters.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Load summary
    summary_path = os.path.join(results_dir, 'experiments_summary.json')
    if not os.path.exists(summary_path):
        print(f"Summary file not found: {summary_path}")
        return

    with open(summary_path, 'r') as f:
        summary = json.load(f)

    # Create dataframe
    experiments = []
    for exp in summary['experiments']:
        if 'error' not in exp:
            exp_data = exp['config'].copy()
            exp_data['test_accuracy'] = exp['test_accuracy']
            exp_data['best_val_accuracy'] = exp['best_val_accuracy']
            experiments.append(exp_data)

    df = pd.DataFrame(experiments)

    if len(df) == 0:
        print("No valid experiments found")
        return

    # Plot 1: Effect of output channels
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    for idx, noise_type in enumerate(['baseline', 'noise_test_0.1', 'noise_both_0.1']):
        ax = axes[idx]
        data = df[df['noise_scenario'] == noise_type]

        for kernel in sorted(data['kernel_size'].unique()):
            subset = data[data['kernel_size'] == kernel].sort_values('out_channels')
            ax.plot(subset['out_channels'], subset['test_accuracy'],
                   marker='o', label=f'Kernel={kernel}')

        ax.set_xlabel('Output Channels')
        ax.set_ylabel('Test Accuracy')
        ax.set_title(f'Noise: {noise_type}')
        ax.legend()
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'effect_of_channels.png'), dpi=300, bbox_inches='tight')
    print(f"Saved: effect_of_channels.png")
    plt.close()

    # Plot 2: Effect of kernel size
    fig, ax = plt.subplots(figsize=(10, 6))

    for channels in sorted(df['out_channels'].unique()):
        data = df[df['out_channels'] == channels]

        for noise_type in sorted(data['noise_scenario'].unique()):
            subset = data[data['noise_scenario'] == noise_type].sort_values('kernel_size')
            ax.plot(subset['kernel_size'], subset['test_accuracy'],
                   marker='s', label=f'Ch={channels}, Noise={noise_type}')

    ax.set_xlabel('Kernel Size')
    ax.set_ylabel('Test Accuracy')
    ax.set_title('Effect of Kernel Size on Test Accuracy')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'effect_of_kernel_size.png'), dpi=300, bbox_inches='tight')
    print(f"Saved: effect_of_kernel_size.png")
    plt.close()

    # Plot 3: Effect of noise
    fig, ax = plt.subplots(figsize=(12, 6))

    baseline = df[df['noise_scenario'] == 'baseline'].groupby('out_channels')['test_accuracy'].mean()
    noise_test_01 = df[df['noise_scenario'] == 'noise_test_0.1'].groupby('out_channels')['test_accuracy'].mean()
    noise_test_02 = df[df['noise_scenario'] == 'noise_test_0.2'].groupby('out_channels')['test_accuracy'].mean()
    noise_both_01 = df[df['noise_scenario'] == 'noise_both_0.1'].groupby('out_channels')['test_accuracy'].mean()
    noise_both_02 = df[df['noise_scenario'] == 'noise_both_0.2'].groupby('out_channels')['test_accuracy'].mean()

    x = np.arange(len(baseline))
    width = 0.15

    ax.bar(x - 2*width, baseline, width, label='Baseline')
    ax.bar(x - width, noise_test_01, width, label='Noise Test (σ=0.1)')
    ax.bar(x, noise_test_02, width, label='Noise Test (σ=0.2)')
    ax.bar(x + width, noise_both_01, width, label='Noise Both (σ=0.1)')
    ax.bar(x + 2*width, noise_both_02, width, label='Noise Both (σ=0.2)')

    ax.set_xlabel('Output Channels')
    ax.set_ylabel('Average Test Accuracy')
    ax.set_title('Effect of Different Noise Scenarios')
    ax.set_xticks(x)
    ax.set_xticklabels(baseline.index)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'effect_of_noise.png'), dpi=300, bbox_inches='tight')
    print(f"Saved: effect_of_noise.png")
    plt.close()

    # Plot 4: Heatmap for channels vs kernel size (baseline)
    baseline_df = df[df['noise_scenario'] == 'baseline']
    pivot = baseline_df.pivot_table(
        values='test_accuracy',
        index='out_channels',
        columns='kernel_size',
        aggfunc='mean'
    )

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(pivot, cmap='viridis', aspect='auto')

    ax.set_xticks(np.arange(len(pivot.columns)))
    ax.set_yticks(np.arange(len(pivot.index)))
    ax.set_xticklabels(pivot.columns)
    ax.set_yticklabels(pivot.index)

    ax.set_xlabel('Kernel Size')
    ax.set_ylabel('Output Channels')
    ax.set_title('Test Accuracy: Channels vs Kernel Size (Baseline)')

    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            value = pivot.iloc[i, j]
            if not np.isnan(value):
                text = ax.text(j, i, f'{value:.3f}',
                             ha="center", va="center", color="w", fontsize=10)

    plt.colorbar(im, ax=ax)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'heatmap_channels_kernel.png'), dpi=300, bbox_inches='tight')
    print(f"Saved: heatmap_channels_kernel.png")
    plt.close()

    # Print statistics
    print("\n" + "="*80)
    print("EXPERIMENT STATISTICS")
    print("="*80)

    print("\nBest configurations by noise scenario:")
    for noise_type in sorted(df['noise_scenario'].unique()):
        best = df[df['noise_scenario'] == noise_type].nlargest(1, 'test_accuracy')
        if len(best) > 0:
            row = best.iloc[0]
            print(f"\n{noise_type}:")
            print(f"  Channels: {row['out_channels']}, Kernel: {row['kernel_size']}")
            print(f"  Test Accuracy: {row['test_accuracy']:.4f}")

    print("\n" + "="*80)


def plot_training_history(results_dir='./results', output_dir='./results'):
    """
    Plot training history for selected experiments.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Load results
    all_results = load_all_results(results_dir)

    if len(all_results) == 0:
        print("No results found")
        return

    # Plot first 4 experiments
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()

    for idx, (filename, config, results) in enumerate(all_results[:4]):
        ax = axes[idx]

        history = results['history']
        epochs = range(1, len(history['train_loss']) + 1)

        ax.plot(epochs, history['train_loss'], 'b-', label='Train Loss')
        ax.plot(epochs, history['val_loss'], 'r-', label='Val Loss')

        ax_twin = ax.twinx()
        ax_twin.plot(epochs, history['val_accuracy'], 'g-', label='Val Accuracy')

        title = f"Ch={config['out_channels']}, K={config['kernel_size']}, Noise={config['noise_scenario']}"
        ax.set_title(title)
        ax.set_xlabel('Epoch')
        ax.set_ylabel('Loss', color='b')
        ax_twin.set_ylabel('Accuracy', color='g')
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'training_history.png'), dpi=300, bbox_inches='tight')
    print(f"Saved: training_history.png")
    plt.close()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--results', type=str, default='./results', help='Results directory')
    parser.add_argument('--output', type=str, default='./results', help='Output directory for plots')

    args = parser.parse_args()

    create_comparison_plots(args.results, args.output)
    plot_training_history(args.results, args.output)
