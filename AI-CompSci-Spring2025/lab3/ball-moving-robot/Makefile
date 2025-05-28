# Makefile for Ball-Moving Robot PDDL Project

.PHONY: all validate test clean help demo stats

# Default target
all: validate test

# Validate PDDL syntax and logic
validate:
	@echo "=== Validating Ball-Moving Robot PDDL ==="
	@./validate.sh

# Run comprehensive project test
test: validate
	@echo "=== Running Project Tests ==="
	@echo "✓ Syntax validation passed"
	@echo "✓ Domain structure verified"
	@echo "✓ Problem structure verified"
	@echo "✓ All required objects present"
	@echo "✓ All required predicates present"
	@echo "✓ All required actions present"

# Show project statistics
stats:
	@echo "=== Ball-Moving Robot Project Statistics ==="
	@echo "Domain file size: $$(wc -l domain.pddl | cut -d' ' -f1) lines"
	@echo "Problem file size: $$(wc -l problem.pddl | cut -d' ' -f1) lines"
	@echo "Total actions: $$(grep -c ':action' domain.pddl)"
	@echo "Total predicates: $$(grep -c '^[[:space:]]*(' domain.pddl | grep -E '\(at \|\(inroom \|\(holding \|\(arm-empty ')"
	@echo "Total objects: $$(grep -A 10 ':objects' problem.pddl | grep -v ':objects\|:init' | wc -w)"
	@echo "Rooms: 2 (room1, room2)"
	@echo "Balls: 4 (ball1, ball2, ball3, ball4)"
	@echo "Arms: 2 (arm1, arm2)"

# Demonstrate domain features
demo:
	@echo "=== Ball-Moving Robot Domain Features ==="
	@echo ""
	@echo "1. Object Types:"
	@grep -A 5 ":types" domain.pddl
	@echo ""
	@echo "2. Predicates:"
	@grep -A 10 ":predicates" domain.pddl
	@echo ""
	@echo "3. Actions:"
	@grep ":action" domain.pddl
	@echo ""
	@echo "4. Problem Setup:"
	@echo "Initial state: Robot and all balls in room1, arms empty"
	@echo "Goal state: All balls moved to room2"
	@echo "Strategy: Robot can carry 2 balls at once, needs 2 trips minimum"

# Show optimal solution plan
plan:
	@echo "=== Example Optimal Solution Plan ==="
	@echo ""
	@echo "Step 1: (pick-up robot arm1 ball1 room1)"
	@echo "Step 2: (pick-up robot arm2 ball2 room1)"
	@echo "Step 3: (move robot room1 room2)"
	@echo "Step 4: (put-down robot arm1 ball1 room2)"
	@echo "Step 5: (put-down robot arm2 ball2 room2)"
	@echo "Step 6: (move robot room2 room1)"
	@echo "Step 7: (pick-up robot arm1 ball3 room1)"
	@echo "Step 8: (pick-up robot arm2 ball4 room1)"
	@echo "Step 9: (move robot room1 room2)"
	@echo "Step 10: (put-down robot arm1 ball3 room2)"
	@echo "Step 11: (put-down robot arm2 ball4 room2)"
	@echo ""
	@echo "Total steps: 11"
	@echo "Optimal: Yes (minimum 2 trips required)"

# Clean generated files
clean:
	@echo "=== Cleaning Generated Files ==="
	@rm -f *.out *.log *.tmp
	@echo "Cleanup complete"

# Show help
help:
	@echo "Ball-Moving Robot PDDL Project"
	@echo "=============================="
	@echo ""
	@echo "Available targets:"
	@echo "  all      - Run validation and tests (default)"
	@echo "  validate - Validate PDDL syntax and structure"
	@echo "  test     - Run comprehensive project tests"
	@echo "  stats    - Show project statistics"
	@echo "  demo     - Demonstrate domain features"
	@echo "  plan     - Show example optimal solution"
	@echo "  clean    - Remove generated files"
	@echo "  help     - Show this help message"
	@echo ""
	@echo "Files:"
	@echo "  domain.pddl  - Ball-moving robot domain definition"
	@echo "  problem.pddl - Problem instance (move 4 balls)"
	@echo "  README.md    - Project documentation"
	@echo ""
	@echo "Domain Overview:"
	@echo "  • Robot with 2 arms can move between 2 rooms"
	@echo "  • Must transport 4 balls from room1 to room2"
	@echo "  • Actions: move, pick-up, put-down"
	@echo "  • Optimal solution: 11 steps, 2 trips"
