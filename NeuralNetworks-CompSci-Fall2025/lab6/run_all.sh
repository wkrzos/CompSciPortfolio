#!/bin/bash

# Comprehensive script to run all experiments, analysis, and visualization

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "========================================="
echo "Lab 6: CNN Experiments - Full Pipeline"
echo "========================================="
echo ""
echo "Scripts: $SCRIPT_DIR"
echo ""

# Activate venv
echo "Activating virtual environment..."
source ../venv/bin/activate

# Run experiments
echo "Starting experiments (this may take 1-2 hours)..."
echo "Running on: $(python3 -c 'import torch; print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU")')"
echo ""

python3 run_experiments.py

# Run analysis
echo ""
echo "Analysis complete! Running detailed comparison..."
python3 compare_results.py --results ./results

# Generate visualizations
echo ""
echo "Generating visualizations..."
python3 visualization.py --results ./results --output ./results

echo ""
echo "========================================="
echo "All done! Results in ./results"
echo "========================================="
echo ""
echo "Generated files:"
ls -1 results/ | grep -E "\.(png|json|csv)$" | sed 's/^/  - /'
