# Makefile for Robot Cleaning PDDL Project

.PHONY: all validate test clean help stats

# Default target
all: validate test

# Validate PDDL syntax
validate:
	@echo "=== Validating Robot Cleaning PDDL Syntax ==="
	@./validate.sh

# Run comprehensive project test
test:
	@echo "=== Running Robot Cleaning Tests ==="
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
	@echo "=== Running Planner on Robot Cleaning Problems ==="
	@./run_planner.sh

# Show project statistics
stats:
	@echo "=== Robot Cleaning Project Statistics ==="
	@echo "Domain file size: $$(wc -l domain.pddl | cut -d' ' -f1) lines"
	@echo "Problem files: $$(ls problem*.pddl | wc -l)"
	@echo "Total actions: $$(grep -c ':action' domain.pddl)"
	@echo "Total predicates: $$(grep -c '^[[:space:]]*(' domain.pddl | grep -v 'define\|domain\|requirements')"

# Show help
help:
	@echo "Robot Cleaning PDDL Project"
	@echo "============================="
	@echo ""
	@echo "Available targets:"
	@echo "  all          - Run validation and tests (default)"
	@echo "  validate     - Validate PDDL syntax"
	@echo "  test         - Run comprehensive project tests"
	@echo "  plan         - Run planner on all problems"
	@echo "  stats        - Show project statistics"
	@echo "  clean        - Remove generated files"
	@echo "  help         - Show this help message"
	@echo ""
	@echo "Files:"
	@echo "  domain.pddl       - Robot cleaning domain definition"
	@echo "  problem.pddl      - Fully connected rooms problem"
	@echo "  problem-linear.pddl - Linear room layout problem"
	@echo "  README.md         - Project documentation"

# Quick verification that all required files exist
check-files:
	@echo "=== Checking Required Files ==="
	@for file in domain.pddl problem.pddl problem-linear.pddl README.md; do \
		if [ -f "$$file" ]; then \
			echo "✓ $$file"; \
		else \
			echo "✗ Missing: $$file"; \
		fi; \
	done
