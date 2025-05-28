#!/bin/bash

# PDDL Planner Runner Script
# This script runs various PDDL planners on the package transport problems

echo "=== PDDL Package Transport Planning ==="
echo "Running planner on different problem instances..."

# Check if Fast Downward is available
if command -v ./fast-downward.py &> /dev/null; then
    echo "Using Fast Downward planner..."
    PLANNER="./fast-downward.py"
    SEARCH_ALGORITHM="--search astar(lmcut())"
elif command -v ff &> /dev/null; then
    echo "Using FF planner..."
    PLANNER="ff"
    SEARCH_ALGORITHM=""
elif command -v optic &> /dev/null; then
    echo "Using OPTIC planner (temporal planning)..."
    PLANNER="optic"
    SEARCH_ALGORITHM=""
else
    echo "No PDDL planner found. Please install one of:"
    echo "- Fast Downward: https://www.fast-downward.org/"
    echo "- FF: https://fai.cs.uni-saarland.de/hoffmann/ff.html"
    echo "- OPTIC: https://nms.kcl.ac.uk/planning/software/optic.html"
    exit 1
fi

# Create results directory
mkdir -p results

echo ""
echo "=== Problem 1: Simple Transport ==="
echo "Running: $PLANNER domain.pddl problem1.pddl $SEARCH_ALGORITHM"
if [ "$PLANNER" = "ff" ]; then
    $PLANNER -o domain.pddl -f problem1.pddl > results/problem1_result.txt 2>&1
elif [ "$PLANNER" = "optic" ]; then
    $PLANNER domain.pddl problem1.pddl > results/problem1_result.txt 2>&1
else
    $PLANNER domain.pddl problem1.pddl $SEARCH_ALGORITHM > results/problem1_result.txt 2>&1
fi

echo "Results saved to results/problem1_result.txt"

echo ""
echo "=== Problem 2: Complex Multi-Vehicle Transport ==="
echo "Running: $PLANNER domain.pddl problem2.pddl $SEARCH_ALGORITHM"
if [ "$PLANNER" = "ff" ]; then
    $PLANNER -o domain.pddl -f problem2.pddl > results/problem2_result.txt 2>&1
elif [ "$PLANNER" = "optic" ]; then
    $PLANNER domain.pddl problem2.pddl > results/problem2_result.txt 2>&1
else
    $PLANNER domain.pddl problem2.pddl $SEARCH_ALGORITHM > results/problem2_result.txt 2>&1
fi

echo "Results saved to results/problem2_result.txt"

echo ""
echo "=== Problem 3: Multi-Modal Transport ==="
echo "Running: $PLANNER domain.pddl problem3.pddl $SEARCH_ALGORITHM"
if [ "$PLANNER" = "ff" ]; then
    $PLANNER -o domain.pddl -f problem3.pddl > results/problem3_result.txt 2>&1
elif [ "$PLANNER" = "optic" ]; then
    $PLANNER domain.pddl problem3.pddl > results/problem3_result.txt 2>&1
else
    $PLANNER domain.pddl problem3.pddl $SEARCH_ALGORITHM > results/problem3_result.txt 2>&1
fi

echo "Results saved to results/problem3_result.txt"

echo ""
echo "=== Analysis Summary ==="
echo "Check the results directory for detailed planner outputs."
echo "Run 'cat results/problem*_result.txt' to view the solutions."

# Simple validation check
echo ""
echo "=== Basic Syntax Validation ==="
for problem in problem1.pddl problem2.pddl problem3.pddl; do
    if grep -q "define" "$problem" && grep -q "domain" "$problem" && grep -q "objects" "$problem"; then
        echo "✓ $problem - syntax looks correct"
    else
        echo "✗ $problem - potential syntax issues"
    fi
done

echo ""
echo "Planning completed! Check the results directory for detailed analysis."
