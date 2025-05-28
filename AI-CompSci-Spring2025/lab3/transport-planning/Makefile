# Makefile for PDDL Package Transport Planning Project

.PHONY: all validate test clean install-ff install-optic help demo

# Default target
all: validate test

# Validate PDDL syntax
validate:
	@echo "=== Validating PDDL Syntax ==="
	@./validate_syntax.sh

# Run comprehensive project test
test:
	@echo "=== Running Project Tests ==="
	@./test_project.sh

# Clean generated files
clean:
	@echo "=== Cleaning Generated Files ==="
	@rm -rf results/
	@rm -f *.out *.log *.tmp
	@echo "Cleanup complete"

# Create results directory
results:
	@mkdir -p results

# Run planner (requires planner installation)
plan: results
	@echo "=== Running Planner ==="
	@./run_planner.sh

# Install FF planner (Ubuntu/Debian)
install-ff:
	@echo "=== Installing FF Planner ==="
	@sudo apt-get update
	@sudo apt-get install -y ff

# Install OPTIC planner (requires manual compilation)
install-optic:
	@echo "=== OPTIC Installation Instructions ==="
	@echo "1. Download from: https://nms.kcl.ac.uk/planning/software/optic.html"
	@echo "2. Extract and compile according to documentation"
	@echo "3. Add to PATH or copy binary to project directory"

# Show project statistics
stats:
	@echo "=== Project Statistics ==="
	@echo "Domain file size: $$(wc -l domain.pddl | cut -d' ' -f1) lines"
	@echo "Problem files: $$(ls problem*.pddl | wc -l)"
	@echo "Total actions: $$(grep -c ':action\|:durative-action' domain.pddl)"
	@echo "Total predicates: $$(grep -c '^[[:space:]]*(' domain.pddl | grep -v 'define\|domain\|requirements')"

# Demonstrate specific PDDL features
demo:
	@echo "=== PDDL Features Demonstration ==="
	@echo ""
	@echo "1. Object Typing:"
	@grep -A 10 ":types" domain.pddl
	@echo ""
	@echo "2. Negative Preconditions:"
	@grep -n "not (" domain.pddl | head -3
	@echo ""
	@echo "3. Conditional Effects:"
	@grep -A 3 "when\|forall" domain.pddl | head -6
	@echo ""
	@echo "4. Cost Functions:"
	@grep -A 3 "increase.*total-cost" domain.pddl | head -3

# Show help
help:
	@echo "PDDL Package Transport Planning Project"
	@echo "======================================="
	@echo ""
	@echo "Available targets:"
	@echo "  all          - Run validation and tests (default)"
	@echo "  validate     - Validate PDDL syntax"
	@echo "  test         - Run comprehensive project tests"
	@echo "  plan         - Run planner on all problems"
	@echo "  stats        - Show project statistics"
	@echo "  demo         - Demonstrate PDDL features"
	@echo "  clean        - Remove generated files"
	@echo "  install-ff   - Install FF planner (Ubuntu/Debian)"
	@echo "  install-optic- Show OPTIC installation instructions"
	@echo "  help         - Show this help message"
	@echo ""
	@echo "Files:"
	@echo "  domain.pddl  - Main domain definition"
	@echo "  problem*.pddl- Problem instances"
	@echo "  analysis.md  - Detailed project analysis"
	@echo "  README.md    - Project documentation"

# Quick verification that all required files exist
check-files:
	@echo "=== Checking Required Files ==="
	@for file in domain.pddl problem1.pddl problem2.pddl problem3.pddl README.md analysis.md; do \
		if [ -f "$$file" ]; then \
			echo "✓ $$file"; \
		else \
			echo "✗ Missing: $$file"; \
		fi; \
	done
