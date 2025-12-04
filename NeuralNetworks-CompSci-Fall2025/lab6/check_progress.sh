#!/bin/bash

# Script to monitor experiment progress and run analysis/visualization when done

RESULTS_DIR="./results"
LOG_FILE="experiment_log.txt"

echo "Monitoring experiments..."
echo "Log file: $LOG_FILE"
echo "Results directory: $RESULTS_DIR"
echo ""

# Wait for experiments to complete
while true; do
    if tail -1 "$LOG_FILE" 2>/dev/null | grep -q "All experiments completed"; then
        echo "Experiments completed!"
        break
    fi

    # Count JSON files
    COUNT=$(ls "$RESULTS_DIR"/*.json 2>/dev/null | wc -l)
    echo "$(date '+%H:%M:%S') - Results files: $COUNT/45"

    sleep 60
done

echo ""
echo "Running analysis..."
source ../venv/bin/activate
python3 compare_results.py --results "$RESULTS_DIR"

echo ""
echo "Generating visualizations..."
python3 visualization.py --results "$RESULTS_DIR" --output "$RESULTS_DIR"

echo ""
echo "All done!"
