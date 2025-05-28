#!/bin/bash

# Ball Moving Robot PDDL Planner Script

echo "=== Ball Moving Robot PDDL Planner ==="
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
echo "=== Ball Moving Problem ==="
echo "Running: $PLANNER domain.pddl problem.pddl"

if [ "$PLANNER" = "ff" ]; then
    ff -o domain.pddl -f problem.pddl > results/ball_moving_result.txt 2>&1
elif [ "$PLANNER" = "fast-downward" ]; then
    ./fast-downward.py domain.pddl problem.pddl --search "astar(lmcut())" > results/ball_moving_result.txt 2>&1
elif [ "$PLANNER" = "optic" ]; then
    optic domain.pddl problem.pddl > results/ball_moving_result.txt 2>&1
fi

echo "Results saved to: results/ball_moving_result.txt"

# Check if solution was found
if grep -q "step\|action\|SOLUTION" results/ball_moving_result.txt; then
    echo "✓ Solution found!"
    echo ""
    echo "Plan preview:"
    grep -A 15 -B 2 "step\|action\|ff: found legal plan" results/ball_moving_result.txt | head -20
else
    echo "✗ No solution found or planning failed"
    echo "Check results/ball_moving_result.txt for details"
fi

echo ""
echo "=== Problem Analysis ==="
echo "Domain: Ball Moving Robot"
echo "Objects: 1 robot, 2 arms, 4 balls, 2 rooms"
echo "Goal: Move all balls from room1 to room2"
echo ""
echo "Expected optimal solution steps:"
echo "1. Robot picks up ball1 with arm1"
echo "2. Robot picks up ball2 with arm2"
echo "3. Robot moves to room2"
echo "4. Robot puts down ball1"
echo "5. Robot puts down ball2"
echo "6. Robot moves back to room1"
echo "7. Robot picks up ball3 with arm1"
echo "8. Robot picks up ball4 with arm2"
echo "9. Robot moves to room2"
echo "10. Robot puts down ball3"
echo "11. Robot puts down ball4"
echo ""
echo "Total expected actions: 11"

# Basic validation
echo ""
echo "=== Basic Validation ==="
if [ -f "domain.pddl" ] && [ -f "problem.pddl" ]; then
    echo "✓ Required PDDL files present"
    
    # Check domain structure
    if grep -q "ball-moving-robot" domain.pddl && grep -q ":strips" domain.pddl; then
        echo "✓ Domain structure looks correct"
    else
        echo "✗ Domain structure issues detected"
    fi
    
    # Check problem structure
    if grep -q "move-balls" problem.pddl && grep -q "ball-moving-robot" problem.pddl; then
        echo "✓ Problem structure looks correct"
    else
        echo "✗ Problem structure issues detected"
    fi
else
    echo "✗ Missing required PDDL files"
fi

echo ""
echo "Planning completed! Check results/ball_moving_result.txt for detailed output."
