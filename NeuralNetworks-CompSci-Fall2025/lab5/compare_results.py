"""
Compare and analyze results from FashionMNIST experiments.
Generates summary statistics and comparison tables.
"""

import json
import os
import pandas as pd
import numpy as np
from tabulate import tabulate


def load_all_results(results_dir='results'):
    """
    Load all experiment results from directory.

    Args:
        results_dir: Directory containing result files

    Returns:
        List of result dictionaries
    """
    results = []

    for filename in os.listdir(results_dir):
        if filename.endswith('_results.json') and not filename.startswith('experiments_summary'):
            filepath = os.path.join(results_dir, filename)
            with open(filepath, 'r') as f:
                result = json.load(f)
                results.append(result)

    return results


def create_summary_table(results):
    """
    Create summary table of all experiments.

    Args:
        results: List of result dictionaries

    Returns:
        DataFrame with summary statistics
    """
    data = []

    for result in results:
        config = result['config']

        row = {
            'Experiment': config['name'],
            'Model Type': config['model_type'],
            'Hidden Size': config['hidden_size'],
            'Batch Size': config['batch_size'],
            'Data Fraction': f"{config['data_fraction']*100:.0f}%",
            'Noise Std': config['noise_std'],
            'Noise Train': config['noise_train'],
            'Parameters': result['num_parameters'],
            'Final Train Acc': f"{result['final_train_acc']:.2f}%",
            'Final Test Acc': f"{result['final_test_acc']:.2f}%",
            'Best Test Acc': f"{result['best_test_acc']:.2f}%",
            'Overfit Gap': f"{result['final_train_acc'] - result['final_test_acc']:.2f}%"
        }

        data.append(row)

    df = pd.DataFrame(data)
    return df


def compare_by_category(results, category):
    """
    Compare results within a specific category.

    Args:
        results: List of result dictionaries
        category: Category to compare (hidden_size, batch_size, data_size, noise)

    Returns:
        DataFrame with comparison statistics
    """
    if category == 'hidden_size':
        filtered = [r for r in results if '_h' in r['config']['name']]
        group_key = 'hidden_size'
    elif category == 'batch_size':
        filtered = [r for r in results if '_bs' in r['config']['name']]
        group_key = 'batch_size'
    elif category == 'data_size':
        filtered = [r for r in results if '_data' in r['config']['name']]
        group_key = 'data_fraction'
    elif category == 'noise':
        filtered = [r for r in results if '_noise' in r['config']['name']]
        group_key = 'noise_std'
    else:
        filtered = results
        group_key = 'name'

    data = []

    for result in filtered:
        config = result['config']

        row = {
            'Model Type': config['model_type'],
            group_key: config.get(group_key, config['name']),
            'Final Test Acc': result['final_test_acc'],
            'Best Test Acc': result['best_test_acc'],
            'Final Train Acc': result['final_train_acc'],
            'Overfit Gap': result['final_train_acc'] - result['final_test_acc']
        }

        if category == 'noise':
            row['Noise Train'] = config['noise_train']

        data.append(row)

    df = pd.DataFrame(data)
    return df.sort_values(by=['Model Type', group_key])


def find_best_configurations(results):
    """
    Find best performing configurations.

    Args:
        results: List of result dictionaries

    Returns:
        Dictionary with best configurations for different metrics
    """
    best = {
        'highest_test_acc': None,
        'lowest_overfit': None,
        'fastest_convergence': None,
        'most_parameters': None,
        'least_parameters': None
    }

    best_test_acc = -1
    lowest_overfit = float('inf')
    fastest_convergence = float('inf')
    most_params = -1
    least_params = float('inf')

    for result in results:
        # Highest test accuracy
        if result['final_test_acc'] > best_test_acc:
            best_test_acc = result['final_test_acc']
            best['highest_test_acc'] = result

        # Lowest overfitting
        overfit = result['final_train_acc'] - result['final_test_acc']
        if overfit < lowest_overfit:
            lowest_overfit = overfit
            best['lowest_overfit'] = result

        # Fastest convergence (epochs to reach 80% test accuracy)
        test_acc = result['history']['test_acc']
        epochs_to_80 = next((i for i, acc in enumerate(test_acc) if acc >= 80), len(test_acc))
        if epochs_to_80 < fastest_convergence:
            fastest_convergence = epochs_to_80
            best['fastest_convergence'] = result

        # Most parameters
        if result['num_parameters'] > most_params:
            most_params = result['num_parameters']
            best['most_parameters'] = result

        # Least parameters
        if result['num_parameters'] < least_params:
            least_params = result['num_parameters']
            best['least_parameters'] = result

    return best


def print_analysis(results):
    """
    Print comprehensive analysis of all results.

    Args:
        results: List of result dictionaries
    """
    print("="*100)
    print("FASHIONMNIST EXPERIMENT ANALYSIS")
    print("="*100)

    # Overall summary
    print("\n1. OVERALL SUMMARY")
    print("-"*100)
    summary_df = create_summary_table(results)
    print(tabulate(summary_df, headers='keys', tablefmt='grid', showindex=False))

    # Best configurations
    print("\n2. BEST CONFIGURATIONS")
    print("-"*100)
    best = find_best_configurations(results)

    for metric, result in best.items():
        if result:
            print(f"\n{metric.replace('_', ' ').title()}:")
            print(f"  Experiment: {result['config']['name']}")
            print(f"  Model: {result['config']['model_type']}-layer")
            print(f"  Test Accuracy: {result['final_test_acc']:.2f}%")
            print(f"  Overfit Gap: {result['final_train_acc'] - result['final_test_acc']:.2f}%")
            print(f"  Parameters: {result['num_parameters']:,}")

    # Category comparisons
    categories = ['hidden_size', 'batch_size', 'data_size', 'noise']

    for category in categories:
        print(f"\n3. COMPARISON: {category.upper()}")
        print("-"*100)

        try:
            comp_df = compare_by_category(results, category)
            if not comp_df.empty:
                print(tabulate(comp_df, headers='keys', tablefmt='grid', showindex=False))
            else:
                print(f"No results found for {category}")
        except Exception as e:
            print(f"Error comparing {category}: {str(e)}")

    # Model architecture comparison
    print("\n4. SINGLE-LAYER VS TWO-LAYER COMPARISON")
    print("-"*100)

    single_layer = [r for r in results if r['config']['model_type'] == 'single']
    two_layer = [r for r in results if r['config']['model_type'] == 'two']

    if single_layer and two_layer:
        single_avg_acc = np.mean([r['final_test_acc'] for r in single_layer])
        two_avg_acc = np.mean([r['final_test_acc'] for r in two_layer])

        single_avg_overfit = np.mean([r['final_train_acc'] - r['final_test_acc'] for r in single_layer])
        two_avg_overfit = np.mean([r['final_train_acc'] - r['final_test_acc'] for r in two_layer])

        comparison_data = [
            ['Single-Layer', len(single_layer), f"{single_avg_acc:.2f}%", f"{single_avg_overfit:.2f}%"],
            ['Two-Layer', len(two_layer), f"{two_avg_acc:.2f}%", f"{two_avg_overfit:.2f}%"]
        ]

        print(tabulate(comparison_data,
                      headers=['Architecture', 'Experiments', 'Avg Test Acc', 'Avg Overfit Gap'],
                      tablefmt='grid'))

    print("\n" + "="*100)


def save_analysis_to_file(results, output_file='results/analysis_summary.txt'):
    """
    Save analysis to text file.

    Args:
        results: List of result dictionaries
        output_file: Path to output file
    """
    import sys
    from io import StringIO

    # Redirect stdout to capture print output
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    print_analysis(results)

    # Get captured output
    output = sys.stdout.getvalue()

    # Restore stdout
    sys.stdout = old_stdout

    # Save to file
    with open(output_file, 'w') as f:
        f.write(output)

    print(f"Analysis saved to {output_file}")

    # Also print to console
    print(output)


def main():
    """Main function to compare all results."""
    import argparse

    parser = argparse.ArgumentParser(description='Compare and analyze experiment results')
    parser.add_argument('--results-dir', type=str, default='results',
                       help='Directory containing result files')
    parser.add_argument('--output-file', type=str, default='results/analysis_summary.txt',
                       help='Output file for analysis')

    args = parser.parse_args()

    # Load all results
    results = load_all_results(args.results_dir)

    if not results:
        print(f"No results found in {args.results_dir}")
        return

    print(f"Loaded {len(results)} experiment results")

    # Print and save analysis
    save_analysis_to_file(results, args.output_file)


if __name__ == '__main__':
    main()
