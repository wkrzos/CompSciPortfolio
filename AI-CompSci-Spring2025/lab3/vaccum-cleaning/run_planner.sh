#!/bin/bash

# Robot Cleaning PDDL Planner Script

echo "=== Robot Cleaning PDDL Planner ==="
echo ""

# Check if planners are available
if command -v ff &> /dev/null; then
    echo "Using FF planner..."
    PLANNER="ff"
elif command -v ./fast-downward.py &> /dev/null; then
    echo "Using Fast Downward planner..."
    PLANNER="fast-downward"
elif command -v optic &> /dev/null; then
    echo "Using OPTIC planner..."
    PLANNER="optic"
else
    echo "No PDDL planner found. Please install one of:"
    echo "- FF: https://fai.cs.uni-saarland.de/hoffmann/ff.html"
    echo "- Fast Downward: https://www.fast-downward.org/"
    echo "- OPTIC: https://nms.kcl.ac.uk/planning/software/optic.html"
    exit 1
fi

# Create results directory
mkdir -p results

echo ""
echo "=== Problem 1: Fully Connected Rooms ==="
echo "Running: $PLANNER domain.pddl problem.pddl"

if [ "$PLANNER" = "ff" ]; then
    ff -o domain.pddl -f problem.pddl > results/fully_connected_result.txt 2>&1
elif [ "$PLANNER" = "fast-downward" ]; then
    ./fast-downward.py domain.pddl problem.pddl --search "astar(lmcut())" > results/fully_connected_result.txt 2>&1
elif [ "$PLANNER" = "optic" ]; then
    optic domain.pddl problem.pddl > results/fully_connected_result.txt 2>&1
fi

echo "Results saved to: results/fully_connected_result.txt"

# Check if solution was found
if grep -q "step\|action\|SOLUTION" results/fully_connected_result.txt; then
    echo "✓ Solution found!"
    echo "Plan preview:"
    grep -A 10 -B 2 "step\|action" results/fully_connected_result.txt | head -15
else
    echo "✗ No solution found or planning failed"
fi

echo ""
echo "=== Problem 2: Linear Room Layout ==="
echo "Running: $PLANNER domain.pddl problem-linear.pddl"

if [ "$PLANNER" = "ff" ]; then
    ff -o domain.pddl -f problem-linear.pddl > results/linear_result.txt 2>&1
elif [ "$PLANNER" = "fast-downward" ]; then
    ./fast-downward.py domain.pddl problem-linear.pddl --search "astar(lmcut())" > results/linear_result.txt 2>&1
elif [ "$PLANNER" = "optic" ]; then
    optic domain.pddl problem-linear.pddl > results/linear_result.txt 2>&1
fi

echo "Results saved to: results/linear_result.txt"

# Check if solution was found
if grep -q "step\|action\|SOLUTION" results/linear_result.txt; then
    echo "✓ Solution found!"
    echo "Plan preview:"
    grep -A 10 -B 2 "step\|action" results/linear_result.txt | head -15
else
    echo "✗ No solution found or planning failed"
fi

echo ""
echo "=== Analysis Summary ==="
echo "Check the results directory for detailed planner outputs:"
echo "- results/fully_connected_result.txt"
echo "- results/linear_result.txt"

echo ""
echo "=== Expected Solutions ==="
echo ""
echo "Fully Connected (optimal ~5 steps):"
echo "1. clean robo pokoj1"
echo "2. move robo pokoj1 pokoj2"
echo "3. clean robo pokoj2" 
echo "4. move robo pokoj2 pokoj3"
echo "5. clean robo pokoj3"
echo ""
echo "Linear Layout (same steps, but more constrained movement):"
echo "1. clean robo pokoj1"
echo "2. move robo pokoj1 pokoj2"
echo "3. clean robo pokoj2"
echo "4. move robo pokoj2 pokoj3" 
echo "5. clean robo pokoj3"

echo ""
echo "Planning completed!"
