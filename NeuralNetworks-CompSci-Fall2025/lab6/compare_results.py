import json
import pandas as pd
import os
from pathlib import Path


def compare_experiments(results_dir='./results'):
    """
    Create comprehensive comparison of all experiments.
    """
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

    # Print comprehensive statistics
    print("\n" + "="*100)
    print("COMPREHENSIVE EXPERIMENT RESULTS")
    print("="*100)

    # 1. Overall statistics
    print("\nOVERALL STATISTICS:")
    print(f"Total experiments: {len(df)}")
    print(f"Mean test accuracy: {df['test_accuracy'].mean():.4f} ± {df['test_accuracy'].std():.4f}")
    print(f"Min accuracy: {df['test_accuracy'].min():.4f}")
    print(f"Max accuracy: {df['test_accuracy'].max():.4f}")

    # 2. Best configurations
    print("\n" + "-"*100)
    print("BEST CONFIGURATIONS (by noise scenario):")
    print("-"*100)
    for noise_type in sorted(df['noise_scenario'].unique()):
        noise_df = df[df['noise_scenario'] == noise_type]
        best = noise_df.nlargest(3, 'test_accuracy')
        print(f"\n{noise_type}:")
        for idx, (_, row) in enumerate(best.iterrows(), 1):
            print(f"  {idx}. Ch={row['out_channels']:2d} K={row['kernel_size']} "
                  f"Acc={row['test_accuracy']:.4f} (Val: {row['best_val_accuracy']:.4f})")

    # 3. Effect of output channels
    print("\n" + "-"*100)
    print("EFFECT OF OUTPUT CHANNELS (averaged across kernel sizes):")
    print("-"*100)
    for noise_type in sorted(df['noise_scenario'].unique()):
        noise_df = df[df['noise_scenario'] == noise_type]
        ch_stats = noise_df.groupby('out_channels')['test_accuracy'].agg(['mean', 'std', 'min', 'max'])
        print(f"\n{noise_type}:")
        print(ch_stats.to_string())

    # 4. Effect of kernel size
    print("\n" + "-"*100)
    print("EFFECT OF KERNEL SIZE (averaged across channels):")
    print("-"*100)
    for noise_type in sorted(df['noise_scenario'].unique()):
        noise_df = df[df['noise_scenario'] == noise_type]
        k_stats = noise_df.groupby('kernel_size')['test_accuracy'].agg(['mean', 'std', 'min', 'max'])
        print(f"\n{noise_type}:")
        print(k_stats.to_string())

    # 5. Effect of noise
    print("\n" + "-"*100)
    print("EFFECT OF NOISE (averaged across all architectures):")
    print("-"*100)
    noise_stats = df.groupby('noise_scenario')['test_accuracy'].agg(['mean', 'std', 'min', 'max', 'count'])
    print(noise_stats.to_string())

    # 6. Top 10 configurations
    print("\n" + "-"*100)
    print("TOP 10 CONFIGURATIONS (overall):")
    print("-"*100)
    top_10 = df.nlargest(10, 'test_accuracy')[['out_channels', 'kernel_size', 'pool_size', 'noise_scenario', 'test_accuracy']]
    for idx, (_, row) in enumerate(top_10.iterrows(), 1):
        print(f"{idx:2d}. Ch={row['out_channels']:2d} K={row['kernel_size']} P={row['pool_size']} "
              f"Noise={row['noise_scenario']:20s} Acc={row['test_accuracy']:.4f}")

    # 7. Noise impact analysis
    print("\n" + "-"*100)
    print("NOISE IMPACT ANALYSIS:")
    print("-"*100)
    baseline_acc = df[df['noise_scenario'] == 'baseline']['test_accuracy'].mean()
    for noise_type in sorted(df['noise_scenario'].unique()):
        if noise_type != 'baseline':
            noise_acc = df[df['noise_scenario'] == noise_type]['test_accuracy'].mean()
            impact = (baseline_acc - noise_acc) / baseline_acc * 100
            print(f"{noise_type:20s}: {noise_acc:.4f} (Impact: {impact:+.2f}%)")

    # 8. Save detailed results to CSV
    csv_path = os.path.join(results_dir, 'detailed_results.csv')
    df_sorted = df.sort_values('test_accuracy', ascending=False)
    df_sorted.to_csv(csv_path, index=False)
    print(f"\nDetailed results saved to: {csv_path}")

    print("\n" + "="*100)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--results', type=str, default='./results', help='Results directory')
    args = parser.parse_args()

    compare_experiments(args.results)
