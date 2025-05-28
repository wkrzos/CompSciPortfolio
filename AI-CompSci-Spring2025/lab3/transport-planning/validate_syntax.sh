#!/bin/bash

# PDDL Syntax Validation Script
# This script performs basic syntax validation on PDDL files

echo "=== PDDL Syntax Validation ==="

# Function to check basic PDDL syntax
validate_pddl() {
    local file=$1
    local errors=0
    
    echo "Checking $file..."
    
    # Check if file exists
    if [ ! -f "$file" ]; then
        echo "  ✗ File not found: $file"
        return 1
    fi
    
    # Check for required sections
    if ! grep -q "(define" "$file"; then
        echo "  ✗ Missing (define section"
        ((errors++))
    fi
    
    if ! grep -q ":requirements" "$file"; then
        echo "  ✗ Missing :requirements section"
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
    fi
    
    if [ $errors -eq 0 ]; then
        echo "  ✓ Syntax validation passed"
        return 0
    else
        echo "  ✗ Found $errors syntax issues"
        return 1
    fi
}

# Validate all PDDL files
total_errors=0

for file in domain.pddl problem1.pddl problem2.pddl problem3.pddl; do
    if ! validate_pddl "$file"; then
        ((total_errors++))
    fi
    echo ""
done

echo "=== Validation Summary ==="
if [ $total_errors -eq 0 ]; then
    echo "✓ All files passed validation"
    exit 0
else
    echo "✗ $total_errors files failed validation"
    exit 1
fi
