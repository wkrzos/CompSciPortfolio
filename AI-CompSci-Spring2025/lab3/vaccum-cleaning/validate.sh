#!/bin/bash

# PDDL Robot Cleaning Validation Script

echo "=== Robot Cleaning PDDL Validation ==="

# Function to validate PDDL syntax
validate_file() {
    local file=$1
    local errors=0
    
    echo "Checking $file..."
    
    if [ ! -f "$file" ]; then
        echo "  ✗ File not found: $file"
        return 1
    fi
    
    # Check basic PDDL structure
    if ! grep -q "(define" "$file"; then
        echo "  ✗ Missing (define section"
        ((errors++))
    fi
    
    # Check parentheses balance
    open_parens=$(grep -o '(' "$file" | wc -l)
    close_parens=$(grep -o ')' "$file" | wc -l)
    
    if [ "$open_parens" -ne "$close_parens" ]; then
        echo "  ✗ Unbalanced parentheses: $open_parens open, $close_parens close"
        ((errors++))
    fi
    
    # Domain-specific checks
    if [[ "$file" == "domain.pddl" ]]; then
        if ! grep -q ":types" "$file"; then
            echo "  ✗ Missing :types section"
            ((errors++))
        fi
        
        if ! grep -q ":predicates" "$file"; then
            echo "  ✗ Missing :predicates section"
            ((errors++))
        fi
        
        if ! grep -q ":action" "$file"; then
            echo "  ✗ Missing :action definitions"
            ((errors++))
        fi
        
        # Check for required predicates
        required_predicates=("at" "dirty" "clean" "connected")
        for pred in "${required_predicates[@]}"; do
            if ! grep -q "($pred" "$file"; then
                echo "  ✗ Missing required predicate: $pred"
                ((errors++))
            fi
        done
        
        # Check for required actions
        required_actions=("move" "clean")
        for action in "${required_actions[@]}"; do
            if ! grep -q ":action $action" "$file"; then
                echo "  ✗ Missing required action: $action"
                ((errors++))
            fi
        done
    fi
    
    # Problem-specific checks
    if [[ "$file" == problem*.pddl ]]; then
        if ! grep -q ":objects" "$file"; then
            echo "  ✗ Missing :objects section"
            ((errors++))
        fi
        
        if ! grep -q ":init" "$file"; then
            echo "  ✗ Missing :init section"
            ((errors++))
        fi
        
        if ! grep -q ":goal" "$file"; then
            echo "  ✗ Missing :goal section"
            ((errors++))
        fi
        
        # Check for required objects
        if ! grep -q "robo.*robot" "$file"; then
            echo "  ✗ Missing robot object 'robo'"
            ((errors++))
        fi
        
        if ! grep -q "pokoj.*room" "$file"; then
            echo "  ✗ Missing room objects"
            ((errors++))
        fi
        
        # Check goal structure
        if ! grep -q "clean pokoj1.*clean pokoj2.*clean pokoj3" "$file"; then
            echo "  ✗ Goal should require all rooms to be clean"
            ((errors++))
        fi
    fi
    
    if [ $errors -eq 0 ]; then
        echo "  ✓ Validation passed"
        return 0
    else
        echo "  ✗ Found $errors issues"
        return 1
    fi
}

# Validate all files
total_errors=0

for file in domain.pddl problem.pddl problem-linear.pddl; do
    if [ -f "$file" ]; then
        if ! validate_file "$file"; then
            ((total_errors++))
        fi
        echo ""
    else
        echo "File not found: $file"
        ((total_errors++))
    fi
done

# Domain-Problem compatibility check
echo "=== Domain-Problem Compatibility Check ==="
if [ -f "domain.pddl" ] && [ -f "problem.pddl" ]; then
    domain_name=$(grep "define.*domain" domain.pddl | sed 's/.*domain \([^)]*\).*/\1/')
    problem_domain=$(grep ":domain" problem.pddl | sed 's/.*:domain \([^)]*\).*/\1/')
    
    if [ "$domain_name" = "$problem_domain" ]; then
        echo "  ✓ Domain names match: $domain_name"
    else
        echo "  ✗ Domain name mismatch: domain=$domain_name, problem=$problem_domain"
        ((total_errors++))
    fi
else
    echo "  ✗ Missing domain.pddl or problem.pddl"
    ((total_errors++))
fi

echo ""
echo "=== Validation Summary ==="
if [ $total_errors -eq 0 ]; then
    echo "✓ All validations passed!"
    echo "✓ Ready for planner execution"
else
    echo "✗ Found $total_errors validation issues"
    echo "✗ Please fix issues before running planner"
fi
