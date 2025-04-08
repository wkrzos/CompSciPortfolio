import sys
import os
import time
import random
import argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # An amazing way to import modules from the parent directory, unfortunately proposed by Claude 3.7
from common.transit_graph import TransitGraph
from common.time_utils import time_to_seconds, seconds_to_time_str
from common.data_loader import load_transit_data
import os.path

class TabuRouting:
    """Base class for Tabu Search routing algorithms"""
    
    def __init__(self, transit_graph, start_stop, stops_to_visit, start_time, criterion='t', max_iterations=1000):
        """
        Initialize the Tabu Search routing solver.
        
        Args:
            transit_graph: The TransitGraph object containing transit network
            start_stop: The starting and ending stop
            stops_to_visit: List of stops that must be visited
            start_time: Starting time in seconds from midnight
            criterion: Optimization criterion - 't' for time or 'p' for transfers
            max_iterations: Maximum number of iterations for the algorithm
        """
        self.graph = transit_graph
        self.start_stop = start_stop
        self.stops_to_visit = stops_to_visit
        self.start_time = start_time
        self.criterion = criterion
        self.max_iterations = max_iterations
        self.tabu_list = []
        self.best_solution = None
        self.best_cost = float('inf')
        
    def generate_initial_solution(self):
        """Generate an initial solution (random permutation of stops)"""
        initial_solution = list(self.stops_to_visit)
        random.shuffle(initial_solution)
        return initial_solution
    
    def evaluate_solution(self, solution):
        """
        Evaluate the cost of a solution by finding paths between consecutive stops.
        
        Args:
            solution: A list of stops in the order they should be visited
            
        Returns:
            tuple: (complete_path, total_cost) where complete_path is a list of all path segments
                  and total_cost is the total cost of the solution
        """
        complete_path = []
        total_cost = 0
        current_time = self.start_time
        current_stop = self.start_stop
        
        # Visit all stops in the solution
        for next_stop in solution:
            # Find path from current stop to next stop
            path, cost = self.graph.find_path_a_star(
                current_stop, next_stop, current_time, cost_criterion=self.criterion
            )
            
            if path is None:
                # If no path found, return infinite cost
                return None, float('inf')
            
            complete_path.extend(path)
            total_cost += cost
            
            # Update current stop and time for next iteration
            current_stop = next_stop
            if path:
                current_time = path[-1][4]  # Arrival time at the last stop
        
        # Return to the starting stop
        path, cost = self.graph.find_path_a_star(
            current_stop, self.start_stop, current_time, cost_criterion=self.criterion
        )
        
        if path is None:
            return None, float('inf')
        
        complete_path.extend(path)
        total_cost += cost
        
        return complete_path, total_cost
    
    def get_neighbors(self, solution):
        """
        Generate neighbor solutions by swapping pairs of stops.
        
        Args:
            solution: The current solution
            
        Returns:
            list: A list of neighboring solutions
        """
        neighbors = []
        n = len(solution)
        
        for i in range(n):
            for j in range(i+1, n):
                neighbor = solution.copy()
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                neighbors.append(neighbor)
                
        return neighbors
    
    def is_tabu(self, solution):
        """
        Check if a solution is in the tabu list.
        
        Args:
            solution: The solution to check
            
        Returns:
            bool: True if the solution is tabu, False otherwise
        """
        return solution in self.tabu_list
    
    def run_tabu_search(self):
        """
        Run the basic Tabu Search algorithm.
        This method should be overridden by subclasses to implement specific variations.
        
        Returns:
            tuple: (best_path, best_cost) where best_path is the list of path segments for
                  the best solution found and best_cost is its cost
        """
        raise NotImplementedError("Subclasses must implement run_tabu_search()")
    
    def print_solution(self, path, cost, execution_time):
        """
        Print the solution in the required format.
        
        Args:
            path: List of path segments
            cost: Total cost of the solution
            execution_time: Execution time in seconds
        """
        if path:
            for segment in path:
                line, board_stop, dep, alight_stop, arr = segment
                dep_time = seconds_to_time_str(dep)
                arr_time = seconds_to_time_str(arr)
                print(f"Linia: {line}, Wsiadamy: {board_stop} o {dep_time}, Wysiadamy: {alight_stop} o {arr_time}")
        else:
            print("Nie znaleziono połączenia")

        sys.stderr.write(f"Wartość funkcji kosztu: {cost}\n")
        sys.stderr.write(f"Czas obliczeń: {execution_time} sekund\n")

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Wyszukiwanie trasy przez wiele przystanków przy użyciu przeszukiwania Tabu")
    parser.add_argument('start_stop', help="Przystanek początkowy A")
    parser.add_argument('stops_to_visit', help="Lista przystanków do odwiedzenia (oddzielone średnikiem)")
    parser.add_argument('criterion', choices=['t', 'p'], help="Kryterium optymalizacyjne: t (czas) lub p (przesiadki)")
    parser.add_argument('start_time', help="Czas pojawienia się na przystanku początkowym (HH:MM:SS)")
    parser.add_argument('--rebuild', action='store_true', help="Wymuś przebudowanie grafu")
    return parser.parse_args()

def load_transit_graph(args):
    """Load or build the transit graph"""
    graph_file = 'transit_graph.pkl'
    transit_graph = None
    
    # Try to load serialized graph if it exists and --rebuild flag is not set
    if not args.rebuild and os.path.exists(graph_file):
        sys.stderr.write("Ładowanie grafu z pliku...\n")
        transit_graph = TransitGraph.load_from_file(graph_file)
    
    # If loading failed or --rebuild flag is set, build the graph from data
    if transit_graph is None:
        sys.stderr.write("Budowanie grafu z danych CSV...\n")
        # Load data
        df = load_transit_data('connection_graph.csv')
        
        # Build transit graph from data
        transit_graph = TransitGraph()
        transit_graph.build_from_dataframe(df)
        
        # Save the graph for future use
        transit_graph.save_to_file(graph_file)
        sys.stderr.write("Graf zapisany do pliku.\n")
    
    return transit_graph
