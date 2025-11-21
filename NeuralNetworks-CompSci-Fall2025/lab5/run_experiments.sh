#!/bin/bash

# Run FashionMNIST experiments script
# This script runs different sets of experiments for lab5

echo "======================================"
echo "FashionMNIST Experiments - Lab5"
echo "======================================"
echo ""

# Activate virtual environment if it exists
if [ -d "../venv" ]; then
    echo "Activating virtual environment..."
    source ../venv/bin/activate
fi

# Check if running all or specific experiments
EXPERIMENT_TYPE=${1:-"all"}

echo "Running experiment type: $EXPERIMENT_TYPE"
echo ""

# Run experiments based on type
case $EXPERIMENT_TYPE in
    baseline)
        echo "Running baseline experiments (single vs two-layer)..."
        python run_experiments.py --experiment baseline --output-dir results
        ;;
    hidden_size)
        echo "Running hidden size experiments..."
        python run_experiments.py --experiment hidden_size --output-dir results
        ;;
    batch_size)
        echo "Running batch size experiments..."
        python run_experiments.py --experiment batch_size --output-dir results
        ;;
    data_size)
        echo "Running data size experiments..."
        python run_experiments.py --experiment data_size --output-dir results
        ;;
    noise)
        echo "Running noise experiments..."
        python run_experiments.py --experiment noise --output-dir results
        ;;
    all)
        echo "Running ALL experiments (this will take a while)..."
        python run_experiments.py --experiment all --output-dir results
        ;;
    *)
        echo "Unknown experiment type: $EXPERIMENT_TYPE"
        echo "Available types: baseline, hidden_size, batch_size, data_size, noise, all"
        exit 1
        ;;
esac

# Check if experiments completed successfully
if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "Experiments completed successfully!"
    echo "======================================"
    echo ""

    # Generate visualizations
    echo "Generating visualizations..."
    python visualization.py --results-dir results --output-dir results/plots

    # Generate analysis summary
    echo ""
    echo "Generating analysis summary..."
    python compare_results.py --results-dir results --output-file results/analysis_summary.txt

    echo ""
    echo "======================================"
    echo "All tasks completed!"
    echo "Results saved in: results/"
    echo "Plots saved in: results/plots/"
    echo "Analysis summary: results/analysis_summary.txt"
    echo "======================================"
else
    echo ""
    echo "======================================"
    echo "Experiments failed!"
    echo "======================================"
    exit 1
fi
