import os
import sys
import time
import random
from tabu_base import TabuRouting, parse_arguments, load_transit_graph
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # An amazing way to import modules from the parent directory, unfortunately proposed by Claude 3.7
from common.time_utils import time_to_seconds

class AspirationTabuSearch(TabuRouting):
    """
    Tabu Search implementation with aspiration criteria.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tabu_tenures = {}  # Dictionary to store tabu tenure for each move
        
    def is_tabu(self, solution):
        """
        Check if a solution is tabu.
        
        Args:
            solution: The solution to check
            
        Returns:
            bool: True if the solution is tabu, False otherwise
        """
        solution_key = tuple(solution)
        return solution_key in self.tabu_tenures and self.tabu_tenures[solution_key] > 0
    
    def aspiration_criteria_met(self, solution, cost):
        """
        Check if aspiration criteria are met (tabu but better than best solution).
        
        Args:
            solution: The solution to check
            cost: The cost of the solution
            
        Returns:
            bool: True if aspiration criteria are met, False otherwise
        """
        return cost < self.best_cost
    
    def update_tabu_list(self, solution, tenure=10):
        """
        Add a solution to the tabu list with a specified tenure.
        
        Args:
            solution: The solution to add to the tabu list
            tenure: The number of iterations the solution remains tabu
        """
        solution_key = tuple(solution)
        self.tabu_tenures[solution_key] = tenure
    
    def decrease_tabu_tenures(self):
        """Decrease the tabu tenure of all moves by 1"""
        for key in list(self.tabu_tenures.keys()):
            self.tabu_tenures[key] -= 1
            if self.tabu_tenures[key] <= 0:
                del self.tabu_tenures[key]
    
    def run_tabu_search(self):
        """
        Run the Tabu Search algorithm with aspiration criteria.
        
        Returns:
            tuple: (best_path, best_cost) where best_path is the list of path segments
                  for the best solution found and best_cost is its cost
        """
        # Generate initial solution
        current_solution = self.generate_initial_solution()
        
        # Evaluate initial solution
        current_path, current_cost = self.evaluate_solution(current_solution)
        
        # Initialize best solution
        self.best_solution = current_solution.copy()
        self.best_cost = current_cost
        best_path = current_path
        
        # For diversification
        diversification_trigger = 15  # Trigger diversification after X iterations without improvement
        iterations_without_improvement = 0
        
        # Main Tabu Search loop
        for iteration in range(self.max_iterations):
            # Generate neighbors
            neighbors = self.get_neighbors(current_solution)
            
            # Evaluate neighbors and choose the best neighbor
            best_neighbor = None
            best_neighbor_cost = float('inf')
            best_neighbor_path = None
            
            for neighbor in neighbors:
                path, cost = self.evaluate_solution(neighbor)
                
                # Check if the neighbor is tabu
                is_tabu = self.is_tabu(neighbor)
                
                # Apply aspiration criteria: accept tabu move if it's better than the best solution
                if (not is_tabu) or (is_tabu and self.aspiration_criteria_met(neighbor, cost)):
                    if cost < best_neighbor_cost:
                        best_neighbor = neighbor
                        best_neighbor_cost = cost
                        best_neighbor_path = path
            
            # If no neighbor was found, break
            if best_neighbor is None:
                break
            
            # Update current solution
            current_solution = best_neighbor.copy()
            current_cost = best_neighbor_cost
            current_path = best_neighbor_path
            
            # Add the move to the tabu list with a dynamic tenure
            # More impactful moves get longer tenure
            if current_cost < self.best_cost:
                # Better solution found, use shorter tenure to explore neighborhood more
                tenure = max(5, len(self.stops_to_visit) // 2)
            else:
                # No improvement, use longer tenure to force exploration
                tenure = max(7, len(self.stops_to_visit))
                
            self.update_tabu_list(best_neighbor, tenure)
            
            # Decrease tabu tenures for each iteration
            self.decrease_tabu_tenures()
            
            # Update best solution if necessary
            if current_cost < self.best_cost:
                self.best_solution = current_solution.copy()
                self.best_cost = current_cost
                best_path = current_path
                iterations_without_improvement = 0
            else:
                iterations_without_improvement += 1
            
            # Apply diversification strategy when stuck in local optima
            if iterations_without_improvement >= diversification_trigger:
                # Attempt to escape local optima by doing a random move
                sys.stderr.write("Applying diversification strategy...\n")
                # Perturb the current solution
                perturbed_solution = current_solution.copy()
                n = len(perturbed_solution)
                
                # Perform multiple swaps
                num_swaps = max(2, n // 3)
                for _ in range(num_swaps):
                    i, j = random.sample(range(n), 2)
                    perturbed_solution[i], perturbed_solution[j] = perturbed_solution[j], perturbed_solution[i]
                
                # Evaluate the perturbed solution
                perturbed_path, perturbed_cost = self.evaluate_solution(perturbed_solution)
                
                # Accept the perturbation regardless of cost
                current_solution = perturbed_solution
                current_cost = perturbed_cost
                current_path = perturbed_path
                
                # Reset counter
                iterations_without_improvement = 0
            
            sys.stderr.write(f"Iteration {iteration}: Best cost = {self.best_cost}\n")
        
        return best_path, self.best_cost

def main():
    # Parse command line arguments
    args = parse_arguments()
    
    # Load transit graph
    transit_graph = load_transit_graph(args)
    
    # Convert start time to seconds
    start_sec = time_to_seconds(args.start_time)
    
    # Parse stops to visit
    stops_to_visit = args.stops_to_visit.split(';')
    
    # Create and initialize the Tabu Search solver
    tabu_solver = AspirationTabuSearch(
        transit_graph, 
        args.start_stop, 
        stops_to_visit, 
        start_sec, 
        criterion=args.criterion
    )
    
    # Start timer before running the algorithm
    t0 = time.time()
    
    # Run Tabu Search
    best_path, best_cost = tabu_solver.run_tabu_search()
    
    # Calculate execution time
    execution_time = time.time() - t0
    
    # Print solution
    tabu_solver.print_solution(best_path, best_cost, execution_time)

if __name__ == '__main__':
    main()
