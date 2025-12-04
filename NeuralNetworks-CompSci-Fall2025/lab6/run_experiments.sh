#!/bin/bash

# Run CNN experiments script

echo "=================================="
echo "Lab 6: CNN Experiments"
echo "=================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 not found!"
    exit 1
fi

# Check if in lab6 directory
if [ ! -f "run_experiments.py" ]; then
    echo "ERROR: run_experiments.py not found!"
    echo "Please run this script from the lab6 directory"
    exit 1
fi

# Parse arguments
QUICK_MODE=false
OUTPUT_DIR="./results"

while [[ $# -gt 0 ]]; do
    case $1 in
        --quick)
            QUICK_MODE=true
            shift
            ;;
        --output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [--quick] [--output DIR]"
            echo ""
            echo "Options:"
            echo "  --quick         Run quick test (5 experiments, 5 epochs)"
            echo "  --output DIR    Output directory for results (default: ./results)"
            echo "  --help          Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Run experiments
if [ "$QUICK_MODE" = true ]; then
    echo "Running QUICK TEST mode..."
    python3 run_experiments.py --quick --output "$OUTPUT_DIR" --epochs 5
else
    echo "Running FULL experiments..."
    python3 run_experiments.py --output "$OUTPUT_DIR"
fi

# Check if experiments were successful
if [ $? -eq 0 ]; then
    echo ""
    echo "=================================="
    echo "Experiments completed successfully!"
    echo "Results saved to: $OUTPUT_DIR"
    echo "=================================="

    # Run analysis
    echo ""
    echo "Running analysis..."
    python3 compare_results.py --results "$OUTPUT_DIR"

    # Generate visualizations
    echo ""
    echo "Generating visualizations..."
    python3 visualization.py --results "$OUTPUT_DIR" --output "$OUTPUT_DIR"

    echo ""
    echo "All done! Check results in: $OUTPUT_DIR"
else
    echo ""
    echo "ERROR: Experiments failed!"
    exit 1
fi
