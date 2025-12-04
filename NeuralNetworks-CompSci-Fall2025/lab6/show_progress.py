#!/usr/bin/env python3
"""
Quick stats viewer for running experiments
"""

import json
import os
import sys
from pathlib import Path
import pandas as pd

def get_results_stats(results_dir='./results'):
    """Get statistics from completed results"""

    completed = 0
    total = 45
    best_acc = 0
    best_config = None

    results = []

    for file in sorted(Path(results_dir).glob('*.json')):
        if 'summary' in file.name:
            continue

        try:
            with open(file, 'r') as f:
                data = json.load(f)

            config = data['config']
            test_acc = data['results']['test_accuracy']

            results.append({
                'name': file.stem,
                'channels': config['out_channels'],
                'kernel': config['kernel_size'],
                'noise': config['noise_scenario'],
                'accuracy': test_acc
            })

            completed += 1

            if test_acc > best_acc:
                best_acc = test_acc
                best_config = config

        except Exception as e:
            print(f"Error reading {file}: {e}", file=sys.stderr)

    return completed, total, best_acc, best_config, results

def print_stats():
    """Print current statistics"""

    try:
        completed, total, best_acc, best_config, results = get_results_stats()

        print("\n" + "="*60)
        print("Lab 6 - Experiment Progress")
        print("="*60)

        # Progress
        percent = (completed / total) * 100
        filled = int(percent / 5)
        bar = '█' * filled + '░' * (20 - filled)
        print(f"\nProgress: [{bar}] {completed}/{total} ({percent:.1f}%)")

        # Best result
        if best_config:
            print(f"\nBest Result So Far: {best_acc:.4f}")
            print(f"  Channels: {best_config['out_channels']}")
            print(f"  Kernel: {best_config['kernel_size']}")
            print(f"  Noise: {best_config['noise_scenario']}")

        # Statistics by parameter
        if results:
            df = pd.DataFrame(results)

            print(f"\n--- By Channels ---")
            for ch in sorted(df['channels'].unique()):
                subset = df[df['channels'] == ch]
                mean_acc = subset['accuracy'].mean()
                print(f"  {ch:2d} channels: {mean_acc:.4f} (n={len(subset)})")

            print(f"\n--- By Kernel Size ---")
            for k in sorted(df['kernel'].unique()):
                subset = df[df['kernel'] == k]
                mean_acc = subset['accuracy'].mean()
                print(f"  {k}×{k} kernel: {mean_acc:.4f} (n={len(subset)})")

            print(f"\n--- By Noise Type ---")
            for noise in sorted(df['noise'].unique()):
                subset = df[df['noise'] == noise]
                mean_acc = subset['accuracy'].mean()
                print(f"  {noise:20s}: {mean_acc:.4f} (n={len(subset)})")

            # Top 5
            print(f"\n--- Top 5 Results ---")
            top5 = df.nlargest(5, 'accuracy')
            for i, (_, row) in enumerate(top5.iterrows(), 1):
                print(f"  {i}. {row['accuracy']:.4f} | "
                      f"Ch={row['channels']:2d} K={row['kernel']} "
                      f"Noise={row['noise']}")

        print("\n" + "="*60 + "\n")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='View experiment progress')
    parser.add_argument('--results', type=str, default='./results',
                        help='Results directory')
    parser.add_argument('--watch', action='store_true',
                        help='Continuously update (every 30 seconds)')
    parser.add_argument('--interval', type=int, default=30,
                        help='Update interval in seconds (with --watch)')

    args = parser.parse_args()

    if args.watch:
        import time
        try:
            while True:
                os.system('clear' if os.name == 'posix' else 'cls')
                print_stats()
                print(f"Next update in {args.interval}s (press Ctrl+C to stop)")
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\nStopped.")
    else:
        print_stats()
