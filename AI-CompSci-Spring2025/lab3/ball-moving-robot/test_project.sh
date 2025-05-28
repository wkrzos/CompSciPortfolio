#!/bin/bash

# Ball Moving Robot PDDL Project Test Script

echo "=== Ball Moving Robot PDDL Project ==="
echo ""

# Set up colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    if [ "$status" = "SUCCESS" ]; then
        echo -e "${GREEN}✓${NC} $message"
    elif [ "$status" = "ERROR" ]; then
        echo -e "${RED}✗${NC} $message"
    elif [ "$status" = "INFO" ]; then
        echo -e "${BLUE}ℹ${NC} $message"
    elif [ "$status" = "WARN" ]; then
        echo -e "${YELLOW}⚠${NC} $message"
    fi
}

# 1. Project Overview
echo -e "${BLUE}=== Project Overview ===${NC}"
print_status "INFO" "Ball Moving Robot PDDL Planning Domain"
print_status "INFO" "Requirements: :strips, :typing"
print_status "INFO" "Goal: Robot with dual arms moves 4 balls between rooms"
echo ""

# 2. File Structure Validation
echo -e "${BLUE}=== File Structure Validation ===${NC}"
required_files=("domain.pddl" "problem.pddl" "Makefile" "validate" "validate.sh")

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        print_status "SUCCESS" "Found: $file"
    else
        print_status "ERROR" "Missing: $file"
    fi
done
echo ""

# 3. PDDL Syntax Validation
echo -e "${BLUE}=== PDDL Syntax Validation ===${NC}"

# Check parentheses balance
files_to_check=("domain.pddl" "problem.pddl")
for file in "${files_to_check[@]}"; do
    if [ -f "$file" ]; then
        open_parens=$(grep -o '(' "$file" | wc -l)
        close_parens=$(grep -o ')' "$file" | wc -l)
        
        if [ "$open_parens" -eq "$close_parens" ]; then
            print_status "SUCCESS" "$file: Parentheses balanced ($open_parens pairs)"
        else
            print_status "ERROR" "$file: Unbalanced parentheses (open: $open_parens, close: $close_parens)"
        fi
    fi
done

# Check domain structure
if [ -f "domain.pddl" ]; then
    echo ""
    echo -e "${BLUE}=== Domain Analysis ===${NC}"
    
    if grep -q "ball-moving-robot" domain.pddl; then
        print_status "SUCCESS" "Domain name: ball-moving-robot"
    else
        print_status "ERROR" "Domain name not found or incorrect"
    fi
    
    # Check requirements
    if grep -q ":strips" domain.pddl && grep -q ":typing" domain.pddl; then
        print_status "SUCCESS" "Required PDDL features declared"
    else
        print_status "WARN" "Missing or incomplete requirements declaration"
    fi
    
    # Check types
    types_count=$(grep -A 5 ":types" domain.pddl | grep -o -E "(robot|room|ball|arm)" | sort -u | wc -l)
    if [ "$types_count" -ge 4 ]; then
        print_status "SUCCESS" "Required object types defined (robot, room, ball, arm)"
    else
        print_status "WARN" "Some object types may be missing"
    fi
    
    # Check predicates
    predicates=$(grep -A 10 ":predicates" domain.pddl | grep -c "at\|inroom\|holding\|arm-empty")
    if [ "$predicates" -ge 4 ]; then
        print_status "SUCCESS" "Core predicates defined (at, inroom, holding, arm-empty)"
    else
        print_status "WARN" "Some predicates may be missing"
    fi
    
    # Check actions
    actions=$(grep -c ":action" domain.pddl)
    print_status "INFO" "Actions defined: $actions"
    
    if grep -q "move" domain.pddl && grep -q "pick-up" domain.pddl && grep -q "put-down" domain.pddl; then
        print_status "SUCCESS" "Required actions present (move, pick-up, put-down)"
    else
        print_status "WARN" "Some required actions may be missing"
    fi
fi

# Check problem structure
if [ -f "problem.pddl" ]; then
    echo ""
    echo -e "${BLUE}=== Problem Analysis ===${NC}"
    
    if grep -q "move-balls" problem.pddl; then
        print_status "SUCCESS" "Problem name: move-balls"
    else
        print_status "ERROR" "Problem name not found or incorrect"
    fi
    
    # Check objects
    rooms=$(grep -A 10 ":objects" problem.pddl | grep -o "room[0-9]" | wc -l)
    robots=$(grep -A 10 ":objects" problem.pddl | grep -c "robot -")
    balls=$(grep -A 10 ":objects" problem.pddl | grep -o "ball[0-9]" | wc -l)
    arms=$(grep -A 10 ":objects" problem.pddl | grep -o "arm[0-9]" | wc -l)
    
    print_status "INFO" "Objects defined - Rooms: $rooms, Robots: $robots, Balls: $balls, Arms: $arms"
    
    if [ "$rooms" -ge 2 ] && [ "$robots" -ge 1 ] && [ "$balls" -ge 4 ] && [ "$arms" -ge 2 ]; then
        print_status "SUCCESS" "Sufficient objects for ball moving task"
    else
        print_status "WARN" "May not have enough objects for the task"
    fi
    
    # Check initial state
    if grep -A 20 ":init" problem.pddl | grep -q "at robot" && grep -q "inroom ball" && grep -q "arm-empty"; then
        print_status "SUCCESS" "Initial state properly defined"
    else
        print_status "WARN" "Initial state may be incomplete"
    fi
    
    # Check goal
    goal_balls=$(grep -A 10 ":goal" problem.pddl | grep -c "inroom ball")
    if [ "$goal_balls" -ge 4 ]; then
        print_status "SUCCESS" "Goal specifies moving all balls"
    else
        print_status "WARN" "Goal may not specify all ball movements"
    fi
fi

echo ""
echo -e "${BLUE}=== Theoretical Analysis ===${NC}"
print_status "INFO" "Problem Complexity:"
print_status "INFO" "  - State space: Exponential in number of balls and rooms"
print_status "INFO" "  - Optimal solution length: ~11 actions (with 2 arms)"
print_status "INFO" "  - Search difficulty: Easy (small state space)"
print_status "INFO" "  - Planning features: Basic STRIPS with typing"

echo ""
echo -e "${BLUE}=== Validation Summary ===${NC}"
if [ -f "domain.pddl" ] && [ -f "problem.pddl" ]; then
    print_status "SUCCESS" "Project structure complete"
    print_status "INFO" "Ready for planner execution"
    print_status "INFO" "Run './run_planner.sh' to solve the problem"
else
    print_status "ERROR" "Missing critical files - project incomplete"
fi

echo ""
print_status "INFO" "Test completed. Check output above for any issues."
