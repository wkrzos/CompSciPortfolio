"""
Compare and analyze results from all experiments.
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from tabulate import tabulate


def load_all_results(results_dir='./results'):
    """Load all experiment results."""
    results_dir = Path(results_dir)
    all_results = []

    for json_file in results_dir.glob('*.json'):
        if json_file.name == 'experiments_summary.json':
            continue

        try:
            with open(json_file, 'r') as f:
                raw = json.load(f)
                results = raw.get('results', {})
                history = results.get('history', {})

                entry = {
                    'filename': json_file.stem,
                    'config': raw.get('config', {}),
                    'test_accuracy': results.get('test_accuracy'),
                    'best_val_accuracy': results.get('best_val_accuracy'),
                    'final_train_accuracy': results.get('final_train_accuracy'),
                    'final_val_accuracy': results.get('final_val_accuracy'),
                    'epochs_trained': results.get('epochs_trained'),
                    'train_accuracies': history.get('train_accuracy', []),
                    'val_accuracies': history.get('val_accuracy', []),
                    'train_losses': history.get('train_loss', []),
                    'val_losses': history.get('val_loss', []),
                }
                all_results.append(entry)
        except Exception as e:
            print(f"Error loading {json_file}: {e}")

    return all_results


def create_summary_table(results, save_path=None):
    """Create summary table of all experiments."""
    data = []

    for r in results:
        config = r['config']
        max_len = config.get('max_len')
        max_len_str = 'full' if max_len is None else str(max_len)

        data.append({
            'RNN Type': config['rnn_type'],
            'Hidden Dim': config['hidden_dim'],
            'Max Length': max_len_str,
            'Parameters': config['num_parameters'],
            'Test Acc': r['test_accuracy'],
            'Best Val Acc': r['best_val_accuracy'],
            'Epochs': r['epochs_trained'],
            'Final Train Acc': r['train_accuracies'][-1] if r['train_accuracies'] else 0,
            'Final Val Loss': r['val_losses'][-1] if r['val_losses'] else 0
        })

    df = pd.DataFrame(data)
    df = df.sort_values('Test Acc', ascending=False)

    print("\n" + "="*100)
    print("EXPERIMENT SUMMARY - All Results (sorted by Test Accuracy)")
    print("="*100)
    print(tabulate(df, headers='keys', tablefmt='pipe', floatfmt='.4f', showindex=False))

    if save_path:
        df.to_csv(save_path, index=False)
        print(f"\nSaved to: {save_path}")

    return df


def analyze_rnn_type(results):
    """Analyze RNN vs LSTM performance."""
    data = []

    for r in results:
        config = r['config']
        data.append({
            'rnn_type': config['rnn_type'],
            'test_acc': r['test_accuracy'],
            'val_acc': r['best_val_accuracy'],
            'epochs': r['epochs_trained'],
            'params': config['num_parameters']
        })

    df = pd.DataFrame(data)

    print("\n" + "="*100)
    print("ANALYSIS: RNN vs LSTM")
    print("="*100)

    for rnn_type in ['RNN', 'LSTM']:
        subset = df[df['rnn_type'] == rnn_type]

        print(f"\n{rnn_type}:")
        print(f"  Experiments: {len(subset)}")
        print(f"  Test Accuracy: {subset['test_acc'].mean():.4f} ± {subset['test_acc'].std():.4f}")
        print(f"  Best: {subset['test_acc'].max():.4f}")
        print(f"  Worst: {subset['test_acc'].min():.4f}")
        print(f"  Mean epochs: {subset['epochs'].mean():.1f}")
        print(f"  Mean params: {subset['params'].mean():.0f}")

    # Statistical comparison
    rnn_acc = df[df['rnn_type'] == 'RNN']['test_acc']
    lstm_acc = df[df['rnn_type'] == 'LSTM']['test_acc']

    print(f"\nDifference (LSTM - RNN):")
    print(f"  Mean: {lstm_acc.mean() - rnn_acc.mean():.4f}")
    print(f"  Median: {lstm_acc.median() - rnn_acc.median():.4f}")

    return df


def analyze_hidden_dimension(results):
    """Analyze effect of hidden dimension."""
    data = []

    for r in results:
        config = r['config']
        data.append({
            'rnn_type': config['rnn_type'],
            'hidden_dim': config['hidden_dim'],
            'test_acc': r['test_accuracy'],
            'params': config['num_parameters']
        })

    df = pd.DataFrame(data)

    print("\n" + "="*100)
    print("ANALYSIS: Hidden Dimension Effect")
    print("="*100)

    summary_data = []

    for rnn_type in ['RNN', 'LSTM']:
        for hidden_dim in sorted(df['hidden_dim'].unique()):
            subset = df[(df['rnn_type'] == rnn_type) & (df['hidden_dim'] == hidden_dim)]

            summary_data.append({
                'RNN Type': rnn_type,
                'Hidden Dim': hidden_dim,
                'Count': len(subset),
                'Mean Acc': subset['test_acc'].mean(),
                'Std Acc': subset['test_acc'].std(),
                'Best Acc': subset['test_acc'].max(),
                'Mean Params': subset['params'].mean()
            })

    summary_df = pd.DataFrame(summary_data)
    print(tabulate(summary_df, headers='keys', tablefmt='pipe', floatfmt='.4f', showindex=False))

    return summary_df


def analyze_truncation(results):
    """Analyze effect of sequence truncation."""
    data = []

    for r in results:
        config = r['config']
        max_len = config.get('max_len')
        max_len_str = 'full' if max_len is None else str(max_len)
        max_len_val = max_len if max_len is not None else 999

        data.append({
            'rnn_type': config['rnn_type'],
            'hidden_dim': config['hidden_dim'],
            'max_len': max_len_str,
            'max_len_val': max_len_val,
            'test_acc': r['test_accuracy'],
            'epochs': r['epochs_trained']
        })

    df = pd.DataFrame(data)

    print("\n" + "="*100)
    print("ANALYSIS: Sequence Truncation Effect")
    print("="*100)

    summary_data = []

    for rnn_type in ['RNN', 'LSTM']:
        for max_len in sorted(df['max_len'].unique(), key=lambda x: (x == 'full', int(x) if x != 'full' else 0)):
            subset = df[(df['rnn_type'] == rnn_type) & (df['max_len'] == max_len)]

            summary_data.append({
                'RNN Type': rnn_type,
                'Max Length': max_len,
                'Count': len(subset),
                'Mean Acc': subset['test_acc'].mean(),
                'Std Acc': subset['test_acc'].std(),
                'Best Acc': subset['test_acc'].max(),
                'Mean Epochs': subset['epochs'].mean()
            })

    summary_df = pd.DataFrame(summary_data)
    print(tabulate(summary_df, headers='keys', tablefmt='pipe', floatfmt='.4f', showindex=False))

    return summary_df


def find_best_configurations(results, top_n=10):
    """Find and display best configurations."""
    data = []

    for r in results:
        config = r['config']
        max_len = config.get('max_len')
        max_len_str = 'full' if max_len is None else str(max_len)

        data.append({
            'RNN Type': config['rnn_type'],
            'Hidden Dim': config['hidden_dim'],
            'Max Length': max_len_str,
            'Test Acc': r['test_accuracy'],
            'Val Acc': r['best_val_accuracy'],
            'Epochs': r['epochs_trained'],
            'Parameters': config['num_parameters'],
            'Overfitting': r['train_accuracies'][-1] - r['best_val_accuracy'] if r['train_accuracies'] else 0
        })

    df = pd.DataFrame(data)
    df = df.sort_values('Test Acc', ascending=False).head(top_n)

    print("\n" + "="*100)
    print(f"TOP {top_n} CONFIGURATIONS")
    print("="*100)
    print(tabulate(df, headers='keys', tablefmt='pipe', floatfmt='.4f', showindex=False))

    return df


def create_detailed_analysis(results, output_dir='./results'):
    """Create detailed analysis report."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "="*100)
    print("DETAILED ANALYSIS OF RNN/LSTM EXPERIMENTS")
    print("="*100)

    # Summary table
    summary_df = create_summary_table(results, save_path=output_dir / 'summary.csv')

    # Analysis by factors
    analyze_rnn_type(results)
    analyze_hidden_dimension(results)
    analyze_truncation(results)

    # Best configurations
    find_best_configurations(results, top_n=10)

    # Additional statistics
    print("\n" + "="*100)
    print("OVERALL STATISTICS")
    print("="*100)

    test_accs = [r['test_accuracy'] for r in results]
    val_accs = [r['best_val_accuracy'] for r in results]
    epochs = [r['epochs_trained'] for r in results]
    params = [r['config']['num_parameters'] for r in results]

    stats = {
        'Metric': ['Test Accuracy', 'Val Accuracy', 'Epochs Trained', 'Parameters'],
        'Mean': [np.mean(test_accs), np.mean(val_accs), np.mean(epochs), np.mean(params)],
        'Std': [np.std(test_accs), np.std(val_accs), np.std(epochs), np.std(params)],
        'Min': [np.min(test_accs), np.min(val_accs), np.min(epochs), np.min(params)],
        'Max': [np.max(test_accs), np.max(val_accs), np.max(epochs), np.max(params)]
    }

    stats_df = pd.DataFrame(stats)
    print(tabulate(stats_df, headers='keys', tablefmt='pipe', floatfmt='.2f', showindex=False))

    print("\n" + "="*100)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Compare and analyze RNN/LSTM experiment results')
    parser.add_argument('--results', type=str, default='./results', help='Results directory')
    parser.add_argument('--output', type=str, default='./results', help='Output directory')

    args = parser.parse_args()

    print("Loading results...")
    results = load_all_results(args.results)

    if not results:
        print("No results found!")
    else:
        print(f"Found {len(results)} experiments")
        create_detailed_analysis(results, args.output)
