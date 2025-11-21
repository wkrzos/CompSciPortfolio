"""
Run experiments with different configurations for FashionMNIST classification.
Tests various combinations of:
- Model architecture (single/two-layer)
- Hidden layer sizes
- Batch sizes
- Training data sizes
- Gaussian noise (test only vs train+test)
"""

import torch
import json
import os
from datetime import datetime
import argparse

from model import create_model, count_parameters
from train import get_data_loaders, train_model


def run_experiment(config, verbose=True):
    """
    Run single experiment with given configuration.

    Args:
        config: Dictionary with experiment configuration
        verbose: Whether to print progress

    Returns:
        Results dictionary
    """
    if verbose:
        print(f"\n{'='*80}")
        print(f"Running experiment: {config['name']}")
        print(f"{'='*80}")
        print(f"Model: {config['model_type']}-layer")
        print(f"Hidden size: {config['hidden_size']}")
        if config['model_type'] == 'two':
            print(f"Hidden size 2: {config.get('hidden_size2', 64)}")
        print(f"Batch size: {config['batch_size']}")
        print(f"Data fraction: {config['data_fraction']*100}%")
        print(f"Noise std: {config['noise_std']}")
        print(f"Noise in training: {config['noise_train']}")

    # Set device: prefer CUDA, fallback to CPU if incompatible
    if torch.cuda.is_available():
        device = torch.device('cuda')
        try:
            # Test a trivial CUDA allocation to catch unsupported SM architectures early
            _ = torch.empty(1, device=device)
        except Exception as e:
            print(f"CUDA initialization failed ({e}); falling back to CPU.")
            device = torch.device('cpu')
    else:
        device = torch.device('cpu')


    # Create model
    if config['model_type'] == 'single':
        model = create_model('single', hidden_size=config['hidden_size'])
    else:
        model = create_model('two',
                           hidden_size=config['hidden_size'],
                           hidden_size2=config.get('hidden_size2', 64))

    num_params = count_parameters(model)
    if verbose:
        print(f"Model parameters: {num_params:,}")

    # Get data loaders
    train_loader, test_loader = get_data_loaders(
        batch_size=config['batch_size'],
        data_fraction=config['data_fraction'],
        noise_std=config['noise_std'],
        noise_train=config['noise_train']
    )

    # Train model
    history = train_model(
        model=model,
        train_loader=train_loader,
        test_loader=test_loader,
        num_epochs=config.get('num_epochs', 20),
        learning_rate=config.get('learning_rate', 0.001),
        device=device,
        noise_std=config['noise_std'],
        noise_train=config['noise_train'],
        verbose=verbose,
        early_stopping=config.get('early_stopping', True),
        patience=config.get('patience', 5),
        min_delta=config.get('min_delta', 0.001)
    )

    # Prepare results
    results = {
        'config': config,
        'history': history,
        'num_parameters': num_params,
        'final_train_acc': history['train_acc'][-1],
        'final_test_acc': history['test_acc'][-1],
        'best_test_acc': max(history['test_acc']),
        'device': str(device),
        'stopped_epoch': history.get('stopped_epoch'),
        'total_epochs': len(history['train_acc'])
    }

    if verbose:
        print(f"\nFinal Results:")
        print(f"Train Accuracy: {results['final_train_acc']:.2f}%")
        print(f"Test Accuracy: {results['final_test_acc']:.2f}%")
        print(f"Best Test Accuracy: {results['best_test_acc']:.2f}%")
        if results['stopped_epoch'] is not None:
            print(f"Early stopping at epoch {results['stopped_epoch']}/{config.get('num_epochs', 20)}")

    return results


def generate_experiment_configs():
    """
    Generate all experiment configurations to test.

    Returns:
        List of configuration dictionaries
    """
    configs = []

    # Base configuration
    base_config = {
        'num_epochs': 20,
        'learning_rate': 0.001,
        'noise_std': 0.0,
        'noise_train': False,
        'batch_size': 32,
        'data_fraction': 1.0,
        'hidden_size': 128,
        'hidden_size2': 64
    }

    # 1. Compare single vs two-layer networks (baseline)
    for model_type in ['single', 'two']:
        config = base_config.copy()
        config['model_type'] = model_type
        config['name'] = f'baseline_{model_type}layer'
        configs.append(config)

    # 2. Test different hidden layer sizes
    for hidden_size in [64, 128, 256, 512]:
        for model_type in ['single', 'two']:
            config = base_config.copy()
            config['model_type'] = model_type
            config['hidden_size'] = hidden_size
            if model_type == 'two':
                config['hidden_size2'] = hidden_size // 2
            config['name'] = f'{model_type}layer_h{hidden_size}'
            configs.append(config)

    # 3. Test different batch sizes
    for batch_size in [16, 32, 64, 128]:
        for model_type in ['single', 'two']:
            config = base_config.copy()
            config['model_type'] = model_type
            config['batch_size'] = batch_size
            config['name'] = f'{model_type}layer_bs{batch_size}'
            configs.append(config)

    # 4. Test different training data sizes
    for data_fraction in [0.01, 0.1, 1.0]:
        for model_type in ['single', 'two']:
            config = base_config.copy()
            config['model_type'] = model_type
            config['data_fraction'] = data_fraction
            config['name'] = f'{model_type}layer_data{int(data_fraction*100)}pct'
            configs.append(config)

    # 5. Test Gaussian noise - test only
    for noise_std in [0.1, 0.3, 0.5]:
        for model_type in ['single', 'two']:
            config = base_config.copy()
            config['model_type'] = model_type
            config['noise_std'] = noise_std
            config['noise_train'] = False
            config['name'] = f'{model_type}layer_noise{noise_std}_testonly'
            configs.append(config)

    # 6. Test Gaussian noise - train and test
    for noise_std in [0.1, 0.3, 0.5]:
        for model_type in ['single', 'two']:
            config = base_config.copy()
            config['model_type'] = model_type
            config['noise_std'] = noise_std
            config['noise_train'] = True
            config['name'] = f'{model_type}layer_noise{noise_std}_traintest'
            configs.append(config)

    return configs


def main():
    """Main function to run all experiments."""
    parser = argparse.ArgumentParser(description='Run FashionMNIST experiments')
    parser.add_argument('--experiment', type=str, default='all',
                       help='Experiment to run (all, baseline, hidden_size, batch_size, data_size, noise)')
    parser.add_argument('--output-dir', type=str, default='results',
                       help='Directory to save results')

    args = parser.parse_args()

    # Generate all configurations
    all_configs = generate_experiment_configs()

    # Filter configurations based on experiment type
    if args.experiment == 'all':
        configs = all_configs
    elif args.experiment == 'baseline':
        configs = [c for c in all_configs if c['name'].startswith('baseline')]
    elif args.experiment == 'hidden_size':
        configs = [c for c in all_configs if '_h' in c['name']]
    elif args.experiment == 'batch_size':
        configs = [c for c in all_configs if '_bs' in c['name']]
    elif args.experiment == 'data_size':
        configs = [c for c in all_configs if '_data' in c['name']]
    elif args.experiment == 'noise':
        configs = [c for c in all_configs if '_noise' in c['name']]
    else:
        print(f"Unknown experiment type: {args.experiment}")
        return

    print(f"\n{'='*80}")
    print(f"Running {len(configs)} experiments")
    print(f"{'='*80}\n")

    # Run experiments
    all_results = []
    for i, config in enumerate(configs):
        print(f"\nExperiment {i+1}/{len(configs)}")

        try:
            results = run_experiment(config, verbose=True)
            all_results.append(results)

            # Save individual result
            os.makedirs(args.output_dir, exist_ok=True)
            result_file = os.path.join(args.output_dir, f"{config['name']}_results.json")
            with open(result_file, 'w') as f:
                json.dump(results, f, indent=2)

            print(f"Saved results to {result_file}")

        except Exception as e:
            print(f"Error in experiment {config['name']}: {str(e)}")
            continue

    # Save summary
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    summary_file = os.path.join(args.output_dir, f'experiments_summary_{timestamp}.json')
    with open(summary_file, 'w') as f:
        json.dump(all_results, f, indent=2)

    print(f"\n{'='*80}")
    print(f"All experiments completed!")
    print(f"Summary saved to {summary_file}")
    print(f"{'='*80}\n")


if __name__ == '__main__':
    main()
