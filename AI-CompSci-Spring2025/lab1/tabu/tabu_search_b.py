import sys
import os
import time
import math
from tabu_base import TabuRouting, parse_arguments, load_transit_graph
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # An amazing way to import modules from the parent directory, unfortunately proposed by Claude 3.7
from common.time_utils import time_to_seconds

class DynamicTabuSearch(TabuRouting):
    """
    Tabu Search implementation with dynamic tabu list size based on the number of stops to visit.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Calculate optimal tabu list size based on problem size
        self.tabu_list_size = self._calculate_tabu_list_size()
        self.tabu_list = []
        
    def _calculate_tabu_list_size(self):
        """
        Calculate optimal tabu list size based on the number of stops to visit.
        The size is adjusted dynamically to balance exploration and exploitation.
        
        Returns:
            int: The tabu list size
        """
        n = len(self.stops_to_visit)
        
        # Different strategies for tabu list size:
        # 1. Square root of problem size
        # 2. Log of problem size
        # 3. Proportion of neighborhood size
        
        # Using a combination of these strategies
        base_size = math.sqrt(n)
        neighborhood_size = n * (n - 1) // 2  # Size of neighborhood (all possible swaps)
        
        # Size that scales with problem size but ensures a reasonable proportion
        # of the neighborhood can be explored
        tabu_size = max(5, min(int(base_size + math.log2(n)), neighborhood_size // 3))
        
        sys.stderr.write(f"Dynamic tabu list size: {tabu_size} for {n} stops\n")
        return tabu_size
    
    def is_tabu(self, solution):
        """
        Check if a solution is in the tabu list.
        
        Args:
            solution: The solution to check
            
        Returns:
            bool: True if the solution is tabu, False otherwise
        """
        return solution in self.tabu_list
    
    def update_tabu_list(self, solution):
        """
        Add a solution to the tabu list and maintain its size.
        
        Args:
            solution: The solution to add to the tabu list
        """
        self.tabu_list.append(solution)
        
        # Keep tabu list size within limit
        if len(self.tabu_list) > self.tabu_list_size:
            self.tabu_list.pop(0)  # Remove oldest entry
    
    def run_tabu_search(self):
        """
        Run the Tabu Search algorithm with dynamic tabu list size.
        
        Returns:
            tuple: (best_path, best_cost) where best_path is the list of path segments
                  for the best solution found and best_cost is its cost
        """
        # Generate initial solution
        current_solution = self.generate_initial_solution()
        
        # Evaluate initial solution
        current_path, current_cost = self.evaluate_solution(current_solution)
        
        # Initialize best solution
        self.best_solution = current_solution
        self.best_cost = current_cost
        best_path = current_path
        
        # Main Tabu Search loop
        iterations_without_improvement = 0
        for iteration in range(self.max_iterations):
            # Generate neighbors
            neighbors = self.get_neighbors(current_solution)
            
            # Evaluate neighbors and choose the best non-tabu neighbor
            best_neighbor = None
            best_neighbor_cost = float('inf')
            best_neighbor_path = None
            
            for neighbor in neighbors:
                if not self.is_tabu(neighbor):
                    path, cost = self.evaluate_solution(neighbor)
                    if cost < best_neighbor_cost:
                        best_neighbor = neighbor
                        best_neighbor_cost = cost
                        best_neighbor_path = path
            
            # If no non-tabu neighbor was found, break
            if best_neighbor is None:
                break
            
            # Update current solution
            current_solution = best_neighbor
            current_cost = best_neighbor_cost
            current_path = best_neighbor_path
            
            # Add the neighbor to the tabu list
            self.update_tabu_list(best_neighbor)
            
            # Update best solution if necessary
            if current_cost < self.best_cost:
                self.best_solution = current_solution
                self.best_cost = current_cost
                best_path = current_path
                iterations_without_improvement = 0
            else:
                iterations_without_improvement += 1
            
            # Stop if no improvement for a while
            if iterations_without_improvement > 20:
                break
            
            # Periodically adjust tabu list size based on search performance
            if iteration > 0 and iteration % 10 == 0:
                # If we're improving, keep the current size
                # If we're not improving, try a different size
                if iterations_without_improvement > 5:
                    # Try a different tabu list size
                    if random.random() < 0.5:
                        self.tabu_list_size = max(2, int(self.tabu_list_size * 0.8))
                    else:
                        self.tabu_list_size = min(len(self.stops_to_visit) * 2, 
                                                  int(self.tabu_list_size * 1.2))
                    sys.stderr.write(f"Adjusted tabu list size to {self.tabu_list_size}\n")
            
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
    tabu_solver = DynamicTabuSearch(
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
