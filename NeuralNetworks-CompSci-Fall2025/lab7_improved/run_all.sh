#!/bin/bash

# Run all experiments for Lab 7

echo "========================================"
echo "Lab 7 - RNN/LSTM Experiments"
echo "========================================"

# Activate virtual environment
source ../venv/bin/activate

# Run experiments
echo ""
echo "Starting experiments..."
echo "This will run 30 experiments (2 RNN types × 3 hidden dims × 5 truncations)"
echo "Using 20% of data for efficiency"
echo ""

python run_experiments.py --subsample 0.2

echo ""
echo "========================================"
echo "Creating visualizations..."
echo "========================================"

python visualization.py

echo ""
echo "========================================"
echo "Comparing results..."
echo "========================================"

python compare_results.py

echo ""
echo "========================================"
echo "All done!"
echo "========================================"
