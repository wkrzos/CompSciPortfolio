#!/bin/bash

# Simple Robot Cleaning PDDL Test Script

echo "=== Robot Cleaning PDDL Project ==="
echo ""

# Check file existence
echo "=== File Check ==="
files=("domain.pddl" "problem.pddl" "problem-linear.pddl")
all_files_exist=true

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file exists"
    else
        echo "✗ $file missing"
        all_files_exist=false
    fi
done

if [ "$all_files_exist" = true ]; then
    echo "✓ All required files present"
else
    echo "✗ Some files are missing"
    exit 1
fi

echo ""
echo "=== Basic Syntax Check ==="

# Check parentheses balance
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        open_parens=$(grep -o '(' "$file" | wc -l)
        close_parens=$(grep -o ')' "$file" | wc -l)
        
        if [ "$open_parens" -eq "$close_parens" ]; then
            echo "✓ $file: Parentheses balanced ($open_parens pairs)"
        else
            echo "✗ $file: Unbalanced parentheses (open: $open_parens, close: $close_parens)"
        fi
    fi
done

echo ""
echo "=== Domain Analysis ==="
if [ -f "domain.pddl" ]; then
    echo "Domain name: $(grep 'define.*domain' domain.pddl | sed 's/.*domain \([^)]*\).*/\1/')"
    echo "Types defined: $(grep -c '- object\|- robot\|- room' domain.pddl)"
    echo "Predicates: $(grep -c '^[[:space:]]*(' domain.pddl | grep -v 'define\|domain\|requirements')"
    echo "Actions: $(grep -c ':action' domain.pddl)"
    
    # Check required predicates
    required_preds=("at" "dirty" "clean" "connected")
    echo ""
    echo "Required predicates check:"
    for pred in "${required_preds[@]}"; do
        if grep -q "($pred" domain.pddl; then
            echo "  ✓ $pred"
        else
            echo "  ✗ $pred missing"
        fi
    done
    
    # Check required actions
    required_actions=("move" "clean")
    echo ""
    echo "Required actions check:"
    for action in "${required_actions[@]}"; do
        if grep -q ":action $action" domain.pddl; then
            echo "  ✓ $action"
        else
            echo "  ✗ $action missing"
        fi
    done
fi

echo ""
echo "=== Problem Analysis ==="
for problem_file in problem.pddl problem-linear.pddl; do
    if [ -f "$problem_file" ]; then
        echo ""
        echo "Analyzing $problem_file:"
        echo "  Problem name: $(grep 'define.*problem' "$problem_file" | sed 's/.*problem \([^)]*\).*/\1/')"
        echo "  Domain reference: $(grep ':domain' "$problem_file" | sed 's/.*:domain \([^)]*\).*/\1/')"
        
        # Check objects
        if grep -q "robo.*robot" "$problem_file"; then
            echo "  ✓ Robot object defined"
        else
            echo "  ✗ Robot object missing"
        fi
        
        if grep -q "pokoj.*room" "$problem_file"; then
            room_count=$(grep -o "pokoj[0-9]" "$problem_file" | sort -u | wc -l)
            echo "  ✓ Room objects defined ($room_count rooms)"
        else
            echo "  ✗ Room objects missing"
        fi
        
        # Check goal
        if grep -q "clean pokoj1.*clean pokoj2.*clean pokoj3" "$problem_file"; then
            echo "  ✓ Goal correctly specified (all rooms clean)"
        else
            echo "  ✗ Goal specification issue"
        fi
    fi
done

echo ""
echo "=== Expected Solution Preview ==="
echo "For both problems, optimal solution should be ~5 steps:"
echo "1. clean robo pokoj1"
echo "2. move robo pokoj1 pokoj2"
echo "3. clean robo pokoj2"
echo "4. move robo pokoj2 pokoj3"
echo "5. clean robo pokoj3"

echo ""
echo "=== Ready to Run Planner ==="
echo "Use: ./run_planner.sh"
echo ""
echo "Project validation complete! ✓"
