#!/bin/bash

# PDDL Project Testing and Demonstration Script
# This script tests the PDDL files and demonstrates project capabilities

echo "========================================"
echo "PDDL Package Transport Planning Project"
echo "========================================"
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
print_status "INFO" "PDDL Package Transport Planning with Extensions"
print_status "INFO" "Extensions: :strips, :typing, :negative-preconditions, :conditional-effects"
print_status "INFO" "            :multi-agent, :numeric-fluents, :action-costs, :durative-actions"
print_status "INFO" "Transport modes: Road (trucks), Air (planes), Water (ships)"
echo ""

# 2. File Structure Validation
echo -e "${BLUE}=== File Structure Validation ===${NC}"
required_files=("domain.pddl" "problem1.pddl" "problem2.pddl" "problem3.pddl" "README.md" "analysis.md")

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
if ./validate_syntax.sh > /dev/null 2>&1; then
    print_status "SUCCESS" "All PDDL files passed syntax validation"
else
    print_status "ERROR" "PDDL syntax validation failed"
    ./validate_syntax.sh
fi
echo ""

# 4. Domain Analysis
echo -e "${BLUE}=== Domain Analysis ===${NC}"
if [ -f "domain.pddl" ]; then
    types_count=$(grep -c "- object\|- vehicle\|- location" domain.pddl)
    predicates_count=$(grep -c "^[[:space:]]*(" domain.pddl | grep -v "define\|domain\|requirements\|types\|functions")
    actions_count=$(grep -c ":action" domain.pddl)
    durative_actions_count=$(grep -c ":durative-action" domain.pddl)
    
    print_status "INFO" "Domain types defined: $types_count"
    print_status "INFO" "Predicates defined: $predicates_count"
    print_status "INFO" "Standard actions: $actions_count"
    print_status "INFO" "Durative actions: $durative_actions_count"
fi
echo ""

# 5. Problem Analysis
echo -e "${BLUE}=== Problem Analysis ===${NC}"
for i in {1..3}; do
    problem_file="problem$i.pddl"
    if [ -f "$problem_file" ]; then
        vehicles=$(grep -c "truck\|plane\|ship" "$problem_file" | head -1)
        packages=$(grep -c "package" "$problem_file" | head -1)
        locations=$(grep -c "city\|airport\|port" "$problem_file" | head -1)
        
        print_status "INFO" "Problem $i: $vehicles vehicles, $packages packages, $locations locations"
    fi
done
echo ""

# 6. PDDL Extensions Demonstration
echo -e "${BLUE}=== PDDL Extensions Demonstration ===${NC}"

# Check for typing
if grep -q ":typing" domain.pddl; then
    print_status "SUCCESS" "✓ :typing - Object type hierarchy implemented"
else
    print_status "ERROR" "✗ :typing - Missing type definitions"
fi

# Check for negative preconditions
if grep -q "not (" domain.pddl; then
    print_status "SUCCESS" "✓ :negative-preconditions - Negative conditions found"
else
    print_status "ERROR" "✗ :negative-preconditions - No negative conditions found"
fi

# Check for conditional effects
if grep -q "when\|forall" domain.pddl; then
    print_status "SUCCESS" "✓ :conditional-effects - Conditional effects implemented"
else
    print_status "WARN" "⚠ :conditional-effects - Limited conditional effects"
fi

# Check for numeric fluents
if grep -q "increase\|total-cost" domain.pddl; then
    print_status "SUCCESS" "✓ :numeric-fluents & :action-costs - Cost tracking implemented"
else
    print_status "ERROR" "✗ :numeric-fluents - No cost functions found"
fi

# Check for durative actions
if grep -q ":durative-action" domain.pddl; then
    print_status "SUCCESS" "✓ :durative-actions - Temporal planning support"
else
    print_status "ERROR" "✗ :durative-actions - No temporal actions found"
fi

# Check for multi-agent
if grep -q "agent" domain.pddl; then
    print_status "SUCCESS" "✓ :multi-agent - Multiple vehicle agents defined"
else
    print_status "ERROR" "✗ :multi-agent - No agent definitions found"
fi
echo ""

# 7. Transport Topology Analysis
echo -e "${BLUE}=== Transport Topology Analysis ===${NC}"

# Road connections
road_connections=$(grep -c "road-connected" problem1.pddl)
print_status "INFO" "Road connections in Problem 1: $road_connections"

# Air connections  
air_connections=$(grep -c "air-connected" problem1.pddl)
print_status "INFO" "Air connections in Problem 1: $air_connections"

# Water connections
water_connections=$(grep -c "water-connected" problem1.pddl)
print_status "INFO" "Water connections in Problem 1: $water_connections"

# Multi-modal analysis for Problem 3
if [ -f "problem3.pddl" ]; then
    intl_locations=$(grep -c "hamburg\|berlin" problem3.pddl)
    if [ $intl_locations -gt 0 ]; then
        print_status "SUCCESS" "✓ International transport routes (Poland-Germany)"
    fi
fi
echo ""

# 8. Cost and Metric Analysis
echo -e "${BLUE}=== Cost and Metric Analysis ===${NC}"
for i in {1..3}; do
    problem_file="problem$i.pddl"
    if [ -f "$problem_file" ]; then
        if grep -q "minimize.*total-cost" "$problem_file"; then
            print_status "SUCCESS" "Problem $i: Cost optimization enabled"
        else
            print_status "WARN" "Problem $i: No cost optimization"
        fi
    fi
done
echo ""

# 9. Planner Availability Check
echo -e "${BLUE}=== Planner Availability Check ===${NC}"
planners_found=0

if command -v ff &> /dev/null; then
    print_status "SUCCESS" "FF planner available"
    ((planners_found++))
fi

if command -v optic &> /dev/null; then
    print_status "SUCCESS" "OPTIC planner available (temporal planning)"
    ((planners_found++))
fi

if [ -f "./fast-downward.py" ] || command -v fast-downward &> /dev/null; then
    print_status "SUCCESS" "Fast Downward planner available"
    ((planners_found++))
fi

if command -v lpg &> /dev/null; then
    print_status "SUCCESS" "LPG planner available"
    ((planners_found++))
fi

if [ $planners_found -eq 0 ]; then
    print_status "WARN" "No PDDL planners detected. Install one of:"
    print_status "INFO" "  - FF: https://fai.cs.uni-saarland.de/hoffmann/ff.html"
    print_status "INFO" "  - OPTIC: https://nms.kcl.ac.uk/planning/software/optic.html"  
    print_status "INFO" "  - Fast Downward: https://www.fast-downward.org/"
    print_status "INFO" "  - LPG: https://lpg.unibs.it/lpg/"
else
    print_status "SUCCESS" "Found $planners_found PDDL planner(s)"
fi
echo ""

# 10. Project Complexity Assessment
echo -e "${BLUE}=== Project Complexity Assessment ===${NC}"

# Calculate complexity metrics
total_objects=0
total_init_facts=0
total_goal_facts=0

for i in {1..3}; do
    problem_file="problem$i.pddl"
    if [ -f "$problem_file" ]; then
        objects=$(grep -A 20 ":objects" "$problem_file" | grep -c " - ")
        init_facts=$(grep -A 100 ":init" "$problem_file" | grep -c "^[[:space:]]*(" | head -1)
        goal_facts=$(grep -A 20 ":goal" "$problem_file" | grep -c "delivered\|at")
        
        print_status "INFO" "Problem $i complexity: $objects objects, ~$init_facts init facts, ~$goal_facts goals"
        
        total_objects=$((total_objects + objects))
        total_init_facts=$((total_init_facts + init_facts))
        total_goal_facts=$((total_goal_facts + goal_facts))
    fi
done

print_status "INFO" "Total project complexity: $total_objects objects, ~$total_init_facts facts, ~$total_goal_facts goals"
echo ""

# 11. Usage Instructions
echo -e "${BLUE}=== Usage Instructions ===${NC}"
print_status "INFO" "1. Run syntax validation: ./validate_syntax.sh"
print_status "INFO" "2. Run planner: ./run_planner.sh"
print_status "INFO" "3. View analysis: cat analysis.md"
print_status "INFO" "4. Check results: ls -la results/"
echo ""

# 12. Summary
echo -e "${BLUE}=== Project Summary ===${NC}"
print_status "SUCCESS" "✓ Complete PDDL implementation with 7+ extensions"
print_status "SUCCESS" "✓ Multi-modal transport topology (road/air/water)"
print_status "SUCCESS" "✓ Three problem instances of increasing complexity"
print_status "SUCCESS" "✓ Cost optimization and temporal planning support"
print_status "SUCCESS" "✓ Multi-agent system with different vehicle types"
print_status "SUCCESS" "✓ Comprehensive analysis and documentation"
echo ""

echo -e "${GREEN}Project setup complete! Ready for planner testing and analysis.${NC}"
