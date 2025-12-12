"""
Show current progress of experiments.
"""

import json
from pathlib import Path
from datetime import datetime


def show_progress(results_dir='./results'):
    """Display progress of experiments."""
    results_dir = Path(results_dir)

    if not results_dir.exists():
        print("No results directory found")
        return

    # Count completed experiments
    json_files = list(results_dir.glob('*.json'))
    json_files = [f for f in json_files if f.name != 'experiments_summary.json']

    print("="*80)
    print("Lab 7 - Experiment Progress")
    print("="*80)
    print(f"\nCompleted: {len(json_files)} / 30 experiments")

    if not json_files:
        print("\nNo experiments completed yet")
        return

    # Load and display results
    results = []
    for json_file in json_files:
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                results.append({
                    'name': json_file.stem,
                    'test_acc': data['test_accuracy'],
                    'val_acc': data['best_val_accuracy'],
                    'epochs': data['epochs_trained'],
                    'rnn_type': data['config']['rnn_type'],
                    'hidden_dim': data['config']['hidden_dim'],
                    'max_len': data['config'].get('max_len', 'full')
                })
        except Exception as e:
            print(f"Error loading {json_file}: {e}")

    if not results:
        return

    # Sort by test accuracy
    results.sort(key=lambda x: x['test_acc'], reverse=True)

    print("\n" + "="*80)
    print("Top 10 Results So Far:")
    print("="*80)
    print(f"{'Name':<25} {'RNN':<6} {'Hidden':<7} {'MaxLen':<7} {'Test Acc':<10} {'Val Acc':<10} {'Epochs':<7}")
    print("-"*80)

    for r in results[:10]:
        max_len_str = 'full' if r['max_len'] == 'full' else str(r['max_len'])
        print(f"{r['name']:<25} {r['rnn_type']:<6} {r['hidden_dim']:<7} {max_len_str:<7} "
              f"{r['test_acc']:<10.4f} {r['val_acc']:<10.4f} {r['epochs']:<7}")

    # Statistics
    test_accs = [r['test_acc'] for r in results]
    print("\n" + "="*80)
    print("Statistics:")
    print("="*80)
    print(f"Mean test accuracy: {sum(test_accs) / len(test_accs):.4f}")
    print(f"Best test accuracy: {max(test_accs):.4f}")
    print(f"Worst test accuracy: {min(test_accs):.4f}")

    # RNN type comparison
    rnn_results = [r for r in results if r['rnn_type'] == 'RNN']
    lstm_results = [r for r in results if r['rnn_type'] == 'LSTM']

    if rnn_results and lstm_results:
        rnn_mean = sum(r['test_acc'] for r in rnn_results) / len(rnn_results)
        lstm_mean = sum(r['test_acc'] for r in lstm_results) / len(lstm_results)

        print(f"\nRNN ({len(rnn_results)} exp): {rnn_mean:.4f}")
        print(f"LSTM ({len(lstm_results)} exp): {lstm_mean:.4f}")
        print(f"Difference: {lstm_mean - rnn_mean:.4f}")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Show experiment progress')
    parser.add_argument('--results', type=str, default='./results', help='Results directory')

    args = parser.parse_args()

    show_progress(args.results)
