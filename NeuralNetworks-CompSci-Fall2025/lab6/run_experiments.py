import os
import torch
import json
from datetime import datetime
from itertools import product
from pathlib import Path

from model import CNNModel, CNNModelDeeper
from train import train_model, save_results
from utils import load_fashion_mnist, prepare_dataloaders


def run_experiments(output_dir='./results', num_workers=4):
    """
    Run systematic experiments with different hyperparameters.

    Experiments cover:
    - Number of output channels in conv layer: [16, 32, 64]
    - Kernel size: [3, 5, 7]
    - Pool size: [2]
    - Noise scenarios:
      * No noise (baseline)
      * Noise in test only (std=0.1, 0.2)
      * Noise in train and test (std=0.1, 0.2)
    """

    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Check device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    # Load data once
    print("Loading Fashion-MNIST dataset...")
    train_data, train_labels, test_data, test_labels = load_fashion_mnist('./data')
    print(f"Train: {train_data.shape}, Test: {test_data.shape}")

    # Define parameter combinations
    out_channels_list = [16, 32, 64]
    kernel_sizes = [3, 5, 7]
    pool_sizes = [2]
    noise_configs = [
        {'name': 'baseline', 'noise_in_train': False, 'noise_in_test': False, 'train_std': 0.0, 'test_std': 0.0},
        {'name': 'noise_test_0.1', 'noise_in_train': False, 'noise_in_test': True, 'train_std': 0.0, 'test_std': 0.1},
        {'name': 'noise_test_0.2', 'noise_in_train': False, 'noise_in_test': True, 'train_std': 0.0, 'test_std': 0.2},
        {'name': 'noise_both_0.1', 'noise_in_train': True, 'noise_in_test': True, 'train_std': 0.1, 'test_std': 0.1},
        {'name': 'noise_both_0.2', 'noise_in_train': True, 'noise_in_test': True, 'train_std': 0.2, 'test_std': 0.2},
    ]

    # Generate summary dictionary
    summary = {
        'timestamp': datetime.now().isoformat(),
        'device': str(device),
        'experiments': []
    }

    experiment_num = 0
    total_experiments = len(out_channels_list) * len(kernel_sizes) * len(pool_sizes) * len(noise_configs)

    for out_ch, kernel, pool, noise_cfg in product(out_channels_list, kernel_sizes, pool_sizes, noise_configs):
        experiment_num += 1

        config = {
            'model': 'CNNModel',
            'out_channels': out_ch,
            'kernel_size': kernel,
            'pool_size': pool,
            'noise_scenario': noise_cfg['name'],
            'train_noise_std': noise_cfg['train_std'],
            'test_noise_std': noise_cfg['test_std'],
            'batch_size': 32,
            'epochs': 30,
            'learning_rate': 0.001,
            'weight_decay': 1e-5,
        }

        print(f"\n{'='*80}")
        print(f"Experiment {experiment_num}/{total_experiments}")
        print(f"Config: out_ch={out_ch}, kernel={kernel}, pool={pool}, noise={noise_cfg['name']}")
        print(f"{'='*80}")

        try:
            # Prepare data loaders
            train_loader, val_loader, test_loader = prepare_dataloaders(
                train_data, train_labels, test_data, test_labels,
                batch_size=config['batch_size'],
                noise_in_train=noise_cfg['noise_in_train'],
                noise_in_test=noise_cfg['noise_in_test'],
                train_noise_std=noise_cfg['train_std'],
                test_noise_std=noise_cfg['test_std']
            )

            # Create model
            model = CNNModel(
                out_channels=out_ch,
                kernel_size=kernel,
                pool_size=pool,
                num_classes=10
            )

            # Train model
            results, trained_model = train_model(
                model, train_loader, val_loader, test_loader, device,
                epochs=config['epochs'],
                learning_rate=config['learning_rate'],
                weight_decay=config['weight_decay']
            )

            # Save results
            exp_name = f"cnn_ch{out_ch}_k{kernel}_p{pool}_{noise_cfg['name']}"
            result_path = os.path.join(output_dir, f"{exp_name}.json")
            save_results(results, config, result_path)

            # Add to summary
            summary['experiments'].append({
                'name': exp_name,
                'config': config,
                'test_accuracy': results['test_accuracy'],
                'best_val_accuracy': results['best_val_accuracy']
            })

            print(f"Test Accuracy: {results['test_accuracy']:.4f}")
            print(f"Result saved to: {result_path}")

        except Exception as e:
            print(f"ERROR in experiment: {e}")
            import traceback
            traceback.print_exc()
            summary['experiments'].append({
                'name': f"cnn_ch{out_ch}_k{kernel}_p{pool}_{noise_cfg['name']}",
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


def run_quick_test(num_epochs=5):
    """
    Quick test with minimal configuration.
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    print("Loading data...")
    train_data, train_labels, test_data, test_labels = load_fashion_mnist('./data')

    config = {
        'out_channels': 32,
        'kernel_size': 3,
        'pool_size': 2,
        'noise_scenario': 'baseline'
    }

    print("Preparing data loaders...")
    train_loader, val_loader, test_loader = prepare_dataloaders(
        train_data, train_labels, test_data, test_labels,
        batch_size=32
    )

    print("Creating model...")
    model = CNNModel(out_channels=32, kernel_size=3, pool_size=2)

    print(f"Training for {num_epochs} epochs...")
    results, _ = train_model(
        model, train_loader, val_loader, test_loader, device,
        epochs=num_epochs
    )

    print(f"Test Accuracy: {results['test_accuracy']:.4f}")
    return results


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Run CNN experiments')
    parser.add_argument('--quick', action='store_true', help='Run quick test')
    parser.add_argument('--output', type=str, default='./results', help='Output directory')
    parser.add_argument('--epochs', type=int, default=5, help='Epochs for quick test')

    args = parser.parse_args()

    if args.quick:
        run_quick_test(num_epochs=args.epochs)
    else:
        run_experiments(output_dir=args.output)
