"""
Run systematic experiments with different hyperparameters for RNN/LSTM on IMDB.
"""

import os
import torch
import json
from datetime import datetime
from itertools import product
from pathlib import Path

from model import RecurrentNet, count_parameters
from train import train_model, save_results
from utils import load_imdb_data, prepare_dataloaders, get_sequence_stats


def run_experiments(output_dir='./results', subsample_fraction=0.2):
    """
    Run systematic experiments with different hyperparameters.

    Experiments cover:
    - RNN type: RNN vs LSTM
    - Hidden dimension: [64, 128, 256]
    - Sequence truncation: [None (full), 20, 50, 100, 200]

    Args:
        output_dir: Directory to save results
        subsample_fraction: Fraction of data to use (0.2 = 20% for faster experiments)
    """

    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Check device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    print(f"Data fraction: {subsample_fraction * 100}%")

    # Define parameter combinations
    rnn_types = ['RNN', 'LSTM']
    hidden_dims = [64, 128, 256]
    max_lengths = [None, 20, 50, 100, 200]  # None means full length

    # Fixed parameters
    vocab_size = 10000
    embedding_dim = 128
    batch_size = 64
    epochs = 20
    learning_rate = 0.001

    # Generate summary dictionary
    summary = {
        'timestamp': datetime.now().isoformat(),
        'device': str(device),
        'subsample_fraction': subsample_fraction,
        'experiments': []
    }

    experiment_num = 0
    total_experiments = len(rnn_types) * len(hidden_dims) * len(max_lengths)

    print(f"\nTotal experiments: {total_experiments}")
    print("="*80)

    for rnn_type, hidden_dim, max_len in product(rnn_types, hidden_dims, max_lengths):
        experiment_num += 1

        max_len_str = 'full' if max_len is None else str(max_len)

        config = {
            'rnn_type': rnn_type,
            'hidden_dim': hidden_dim,
            'max_len': max_len,
            'vocab_size': vocab_size,
            'embedding_dim': embedding_dim,
            'batch_size': batch_size,
            'epochs': epochs,
            'learning_rate': learning_rate,
            'subsample_fraction': subsample_fraction
        }

        print(f"\n{'='*80}")
        print(f"Experiment {experiment_num}/{total_experiments}")
        print(f"Config: {rnn_type}, hidden={hidden_dim}, max_len={max_len_str}")
        print(f"{'='*80}")

        try:
            # Load data with appropriate max_len
            print(f"Loading IMDB data (max_len={max_len_str})...")
            train_data, train_labels, test_data, test_labels, word_index = load_imdb_data(
                max_words=vocab_size,
                max_len=max_len
            )

            # Print sequence statistics
            if experiment_num == 1 or max_len is not None:
                train_stats = get_sequence_stats(train_data)
                print(f"Train sequence lengths: "
                      f"mean={train_stats['mean']:.1f}, "
                      f"median={train_stats['median']:.1f}, "
                      f"max={train_stats['max']}, "
                      f"95th percentile={train_stats['percentiles']['95']:.1f}")

            # Prepare data loaders
            train_loader, val_loader, test_loader = prepare_dataloaders(
                train_data, train_labels, test_data, test_labels,
                batch_size=batch_size,
                subsample_fraction=subsample_fraction
            )

            # Create model
            model = RecurrentNet(
                vocab_size=vocab_size,
                embedding_dim=embedding_dim,
                hidden_dim=hidden_dim,
                num_classes=2,
                rnn_type=rnn_type,
                num_layers=1,
                dropout=0.5
            )

            n_params = count_parameters(model)
            print(f"Model parameters: {n_params:,}")
            config['num_parameters'] = n_params

            # Train model
            results, trained_model = train_model(
                model, train_loader, val_loader, test_loader, device,
                epochs=epochs,
                learning_rate=learning_rate,
                patience=5
            )

            # Save results
            exp_name = f"{rnn_type.lower()}_h{hidden_dim}_len{max_len_str}"
            result_path = os.path.join(output_dir, f"{exp_name}.json")
            save_results(results, config, result_path)

            # Add to summary
            summary['experiments'].append({
                'name': exp_name,
                'config': config,
                'test_accuracy': results['test_accuracy'],
                'best_val_accuracy': results['best_val_accuracy'],
                'epochs_trained': results['epochs_trained']
            })

            print(f"\nTest Accuracy: {results['test_accuracy']:.4f}")
            print(f"Best Val Accuracy: {results['best_val_accuracy']:.4f}")
            print(f"Result saved to: {result_path}")

        except Exception as e:
            print(f"ERROR in experiment: {e}")
            import traceback
            traceback.print_exc()
            summary['experiments'].append({
                'name': f"{rnn_type.lower()}_h{hidden_dim}_len{max_len_str}",
                'config': config,
                'error': str(e)
            })

    # Save summary
    summary_path = os.path.join(output_dir, 'experiments_summary.json')
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\n{'='*80}")
    print("All experiments completed!")
    print(f"Summary saved to: {summary_path}")
    print(f"{'='*80}")

    return summary


def run_quick_test(max_epochs=3):
    """
    Quick test with minimal configuration.
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    # Load small subset
    print("Loading IMDB data (max_len=50, 5% of data)...")
    train_data, train_labels, test_data, test_labels, word_index = load_imdb_data(
        max_words=5000,
        max_len=50
    )

    # Get stats
    train_stats = get_sequence_stats(train_data)
    print(f"Train sequences: {len(train_data)}")
    print(f"Sequence lengths: mean={train_stats['mean']:.1f}, max={train_stats['max']}")

    # Prepare dataloaders
    train_loader, val_loader, test_loader = prepare_dataloaders(
        train_data, train_labels, test_data, test_labels,
        batch_size=32,
        subsample_fraction=0.05
    )

    # Create model
    model = RecurrentNet(
        vocab_size=5000,
        embedding_dim=64,
        hidden_dim=64,
        num_classes=2,
        rnn_type='LSTM',
        num_layers=1
    )

    print(f"Model parameters: {count_parameters(model):,}")

    # Train
    print(f"\nTraining for {max_epochs} epochs...")
    results, _ = train_model(
        model, train_loader, val_loader, test_loader, device,
        epochs=max_epochs,
        patience=10
    )

    print(f"\nQuick test completed!")
    print(f"Test Accuracy: {results['test_accuracy']:.4f}")

    return results


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Run RNN/LSTM experiments on IMDB')
    parser.add_argument('--quick', action='store_true', help='Run quick test')
    parser.add_argument('--output', type=str, default='./results', help='Output directory')
    parser.add_argument('--subsample', type=float, default=0.2,
                        help='Fraction of data to use (default: 0.2 = 20%)')
    parser.add_argument('--epochs', type=int, default=3, help='Epochs for quick test')

    args = parser.parse_args()

    if args.quick:
        run_quick_test(max_epochs=args.epochs)
    else:
        run_experiments(output_dir=args.output, subsample_fraction=args.subsample)
