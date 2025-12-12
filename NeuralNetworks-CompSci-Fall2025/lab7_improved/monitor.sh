#!/bin/bash

# Monitor progress of experiments

echo "Monitoring Lab 7 experiments..."
echo "Press Ctrl+C to stop monitoring"
echo ""

while true; do
    clear
    echo "========================================"
    echo "Lab 7 - Experiment Progress"
    echo "========================================"
    echo ""

    # Count result files
    if [ -d "results" ]; then
        total_files=$(find results -name "*.json" ! -name "experiments_summary.json" | wc -l)
        echo "Completed experiments: $total_files / 30"
        echo ""

        # Show latest 5 results
        echo "Latest results:"
        echo "----------------------------------------"
        find results -name "*.json" ! -name "experiments_summary.json" -type f -printf '%T@ %p\n' | \
            sort -rn | head -5 | cut -d' ' -f2- | while read file; do
            name=$(basename "$file" .json)
            if [ -f "$file" ]; then
                acc=$(grep -o '"test_accuracy": [0-9.]*' "$file" | head -1 | cut -d' ' -f2)
                echo "  $name: ${acc:-N/A}"
            fi
        done
    else
        echo "No results directory found yet"
    fi

    echo ""
    echo "Refreshing in 10 seconds..."
    sleep 10
done
