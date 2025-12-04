#!/bin/bash

# Real-time progress monitor for experiments

RESULTS_DIR="./results"

echo "========================================="
echo "Lab 6 Experiments - Progress Monitor"
echo "========================================="
echo ""

while true; do
    # Count completed experiments
    COUNT=$(ls "$RESULTS_DIR"/*.json 2>/dev/null | grep -v summary | wc -l)
    TOTAL=45
    PERCENT=$((COUNT * 100 / TOTAL))

    # Show progress bar
    FILLED=$((PERCENT / 5))
    EMPTY=$((20 - FILLED))
    BAR=$(printf '█%.0s' $(seq 1 $FILLED))$(printf '░%.0s' $(seq 1 $EMPTY))

    # Get last experiment info
    LAST=$(tail -3 experiment_log.txt 2>/dev/null | grep "Experiment" || echo "Starting...")

    echo -ne "\r[$BAR] $COUNT/$TOTAL ($PERCENT%) - $LAST                    "

    # Check if done
    if [ $COUNT -ge $TOTAL ] && tail -1 experiment_log.txt 2>/dev/null | grep -q "All experiments completed"; then
        echo ""
        echo ""
        echo "✓ All experiments completed!"
        break
    fi

    sleep 5
done

echo ""
echo "Running analysis and visualization..."
source ../venv/bin/activate
python3 compare_results.py --results "$RESULTS_DIR"
python3 visualization.py --results "$RESULTS_DIR" --output "$RESULTS_DIR"
echo "Done!"
