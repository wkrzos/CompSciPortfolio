#!/bin/bash

# PDDL Validation Script for Ball-Moving Robot Project
# Validates syntax and basic logical consistency

echo "=== PDDL Ball-Moving Robot Validation ==="
echo ""

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if files exist
echo "📁 Checking required files..."
if [ ! -f "domain.pddl" ]; then
    echo -e "${RED}✗ domain.pddl not found${NC}"
    exit 1
else
    echo -e "${GREEN}✓ domain.pddl found${NC}"
fi

if [ ! -f "problem.pddl" ]; then
    echo -e "${RED}✗ problem.pddl not found${NC}"
    exit 1
else
    echo -e "${GREEN}✓ problem.pddl found${NC}"
fi

echo ""

# Basic syntax validation
echo "🔍 Performing basic syntax checks..."

# Check domain file structure
echo "Checking domain.pddl structure..."
if grep -q "(define (domain" domain.pddl; then
    echo -e "${GREEN}✓ Domain definition found${NC}"
else
    echo -e "${RED}✗ Invalid domain definition${NC}"
    exit 1
fi

if grep -q ":requirements" domain.pddl; then
    echo -e "${GREEN}✓ Requirements section found${NC}"
else
    echo -e "${YELLOW}⚠ No requirements section${NC}"
fi

if grep -q ":types" domain.pddl; then
    echo -e "${GREEN}✓ Types section found${NC}"
else
    echo -e "${YELLOW}⚠ No types section${NC}"
fi

if grep -q ":predicates" domain.pddl; then
    echo -e "${GREEN}✓ Predicates section found${NC}"
else
    echo -e "${RED}✗ No predicates section${NC}"
    exit 1
fi

# Count actions
ACTION_COUNT=$(grep -c ":action" domain.pddl)
echo -e "${GREEN}✓ Found $ACTION_COUNT actions${NC}"

# Check problem file structure
echo ""
echo "Checking problem.pddl structure..."
if grep -q "(define (problem" problem.pddl; then
    echo -e "${GREEN}✓ Problem definition found${NC}"
else
    echo -e "${RED}✗ Invalid problem definition${NC}"
    exit 1
fi

if grep -q ":domain ball-moving-robot" problem.pddl; then
    echo -e "${GREEN}✓ Correct domain reference${NC}"
else
    echo -e "${RED}✗ Incorrect domain reference${NC}"
    exit 1
fi

if grep -q ":objects" problem.pddl; then
    echo -e "${GREEN}✓ Objects section found${NC}"
else
    echo -e "${RED}✗ No objects section${NC}"
    exit 1
fi

if grep -q ":init" problem.pddl; then
    echo -e "${GREEN}✓ Initial state found${NC}"
else
    echo -e "${RED}✗ No initial state${NC}"
    exit 1
fi

if grep -q ":goal" problem.pddl; then
    echo -e "${GREEN}✓ Goal state found${NC}"
else
    echo -e "${RED}✗ No goal state${NC}"
    exit 1
fi

echo ""

# Domain-specific validation
echo "🎯 Domain-specific validation..."

# Check required objects
echo "Checking required objects in problem..."
REQUIRED_OBJECTS=("robot" "room1" "room2" "ball1" "ball2" "ball3" "ball4" "arm1" "arm2")
for obj in "${REQUIRED_OBJECTS[@]}"; do
    if grep -q "$obj" problem.pddl; then
        echo -e "${GREEN}✓ Object $obj found${NC}"
    else
        echo -e "${RED}✗ Missing object: $obj${NC}"
    fi
done

# Check required predicates
echo ""
echo "Checking required predicates..."
REQUIRED_PREDICATES=("at" "inroom" "holding" "arm-empty")
for pred in "${REQUIRED_PREDICATES[@]}"; do
    if grep -q "$pred" domain.pddl; then
        echo -e "${GREEN}✓ Predicate $pred found${NC}"
    else
        echo -e "${RED}✗ Missing predicate: $pred${NC}"
    fi
done

# Check required actions
echo ""
echo "Checking required actions..."
REQUIRED_ACTIONS=("move" "pick-up" "put-down")
for action in "${REQUIRED_ACTIONS[@]}"; do
    if grep -q ":action $action" domain.pddl; then
        echo -e "${GREEN}✓ Action $action found${NC}"
    else
        echo -e "${RED}✗ Missing action: $action${NC}"
    fi
done

echo ""

# Try external validator if available
echo "🔧 Checking for external PDDL validators..."
if command -v validate &> /dev/null; then
    echo "Running VAL validator..."
    validate domain.pddl problem.pddl
elif command -v pddl-validator &> /dev/null; then
    echo "Running pddl-validator..."
    pddl-validator domain.pddl problem.pddl
else
    echo -e "${YELLOW}ℹ No external validator found. Install VAL or similar for complete validation.${NC}"
fi

echo ""
echo -e "${GREEN}=== Validation Complete ===${NC}"
echo "The ball-moving robot PDDL files appear to be syntactically correct!"
echo ""
echo "Next steps:"
echo "• Run with a PDDL planner to test functionality"
echo "• Verify that the solution plan makes logical sense"
echo "• Test with different problem instances"
