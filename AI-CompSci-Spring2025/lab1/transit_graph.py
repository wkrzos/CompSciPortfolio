from collections import defaultdict
import heapq
import pickle
from geo_utils import haversine

class TransitGraph:
    """A graph representation of a transit network."""
    
    def __init__(self):
        """Initialize an empty transit graph."""
        self.graph = defaultdict(list)
        self.stops_coords = {}
        self.direct_connections = set()  # Store direct connections for quick lookup
        
    def build_from_dataframe(self, df):
        """Build the graph from a pandas DataFrame of transit connections."""
        # Sort connections by departure time for better performance
        df = df.sort_values('dep_sec')
        
        # Build list of all stops for pre-filtering
        all_stops = set()
        
        for _, row in df.iterrows():
            start = row['start_stop']
            end = row['end_stop']
            all_stops.add(start)
            all_stops.add(end)
            
            # Record direct connection for rapid lookup
            self.direct_connections.add((start, end))
            
            edge = {
                'end_stop': end,
                'dep_sec': row['dep_sec'],
                'arr_sec': row['arr_sec'],
                'line': row['line'],
                'start_stop_lat': row['start_stop_lat'],
                'start_stop_lon': row['start_stop_lon'],
                'end_stop_lat': row['end_stop_lat'],
                'end_stop_lon': row['end_stop_lon']
            }
            self.graph[start].append(edge)
            
        # Extract coordinates
        for _, row in df.iterrows():
            self.stops_coords[row['start_stop']] = (row['start_stop_lat'], row['start_stop_lon'])
            self.stops_coords[row['end_stop']] = (row['end_stop_lat'], row['end_stop_lon'])
        
        # Pre-calculate reachability for stops
        self._precompute_reachability(all_stops)
        
        return self
    
    def _precompute_reachability(self, all_stops):
        """Build a reachability map to quickly determine if a path might exist."""
        self.reachable_from = defaultdict(set)
        
        # Initialize with direct connections
        for start, end in self.direct_connections:
            self.reachable_from[start].add(end)
        
        # Use Floyd-Warshall like approach to expand reachability
        for intermediate in all_stops:
            for start in all_stops:
                if intermediate in self.reachable_from[start]:
                    for end in self.reachable_from[intermediate]:
                        self.reachable_from[start].add(end)
    
    def is_potentially_reachable(self, start, target):
        """Check if target is potentially reachable from start based on precomputed data."""
        return target in self.reachable_from.get(start, set())
    
    def get_connections_from(self, stop):
        """Get all outgoing connections from a stop."""
        return self.graph.get(stop, [])
    
    def get_coordinates(self, stop):
        """Get coordinates of a stop."""
        return self.stops_coords.get(stop)
    
    def heuristic_time(self, current_stop, target_stop):
        """Heuristic function for travel time estimation."""
        MAX_SPEED_KM_S = 40/3600  # 40 km/h converted to km/s
        
        if current_stop not in self.stops_coords or target_stop not in self.stops_coords:
            return 0
            
        lat1, lon1 = self.stops_coords[current_stop]
        lat2, lon2 = self.stops_coords[target_stop]
        
        distance = haversine(lat1, lon1, lat2, lon2)
        return distance / MAX_SPEED_KM_S
    
    def heuristic_transfers(self, current_stop, target_stop):
        """Heuristic function for transfers minimization."""
        return 0
    
    def find_direct_connections(self, start, target, start_time):
        """Find direct connections between start and target after start_time."""
        direct_paths = []
        
        if not self.is_potentially_reachable(start, target):
            return None
            
        for edge in self.graph.get(start, []):
            if edge['end_stop'] == target and edge['dep_sec'] >= start_time:
                path = [(edge['line'], start, edge['dep_sec'], target, edge['arr_sec'])]
                cost = edge['arr_sec'] - start_time  # Total time including waiting
                direct_paths.append((path, cost))
                
        if direct_paths:
            # Return the direct path with minimum cost
            return min(direct_paths, key=lambda x: x[1])
        return None
    
    def find_path_a_star(self, start, target, start_time, cost_criterion='t'):
        """
        Find the optimal path using A* algorithm with optimizations.
        
        Args:
            start (str): Starting stop
            target (str): Target stop
            start_time (int): Starting time in seconds
            cost_criterion (str): 't' for time optimization, 'p' for transfers optimization
            
        Returns:
            tuple: (path, cost) where path is a list of segments and cost is the total cost
        """
        # Quick validation - check if target exists
        if target not in self.stops_coords:
            return None, float('inf')
            
        # Check if start and target are the same
        if start == target:
            return [], 0
            
        # Check if target is potentially reachable from start
        if not self.is_potentially_reachable(start, target):
            return None, float('inf')
        
        # Try to find direct connections first
        direct_result = self.find_direct_connections(start, target, start_time)
        if direct_result:
            return direct_result
        
        # If no direct path, use A* search with optimizations
        visited = set()
        costs = {start: start_time}
        
        # Calculate spatial bounds for pruning
        if start in self.stops_coords and target in self.stops_coords:
            start_lat, start_lon = self.stops_coords[start]
            target_lat, target_lon = self.stops_coords[target]
            max_distance = haversine(start_lat, start_lon, target_lat, target_lon) * 2.5  # Allow 2.5x the direct distance
        else:
            max_distance = float('inf')
        
        # Use priority queue for A* search
        pq = [(0, start_time, start, start_time, [], None)]
        nodes_explored = 0
        max_nodes = 10000  # Limit exploration to prevent excessive search
        
        while pq and nodes_explored < max_nodes:
            f, g, current, curr_time, path, current_line = heapq.heappop(pq)
            nodes_explored += 1
            
            # Skip if we've found a better path to this node
            if current in visited and costs[current] <= g:
                continue
                
            visited.add(current)
            costs[current] = g
            
            if current == target:
                return path, g
            
            # Dynamic bound adjustment - if we're exploring too widely, tighten the bound
            if nodes_explored > 5000:
                max_distance *= 0.8
            
            # Explore outgoing edges
            for edge in sorted(self.graph.get(current, []), key=lambda e: e['dep_sec']):  # Sort by departure time
                if edge['dep_sec'] >= curr_time:
                    next_stop = edge['end_stop']
                    
                    # Skip already visited stops with better costs
                    if next_stop in costs and costs[next_stop] <= g:
                        continue
                    
                    # Spatial pruning - skip stops too far from the general path direction
                    if next_stop in self.stops_coords and target in self.stops_coords:
                        if self._is_too_far_from_path(current, next_stop, target, max_distance):
                            continue
                    
                    # Calculate cost based on criterion
                    if cost_criterion == 't':
                        wait_time = edge['dep_sec'] - curr_time
                        ride_time = edge['arr_sec'] - edge['dep_sec']
                        step_cost = wait_time + ride_time
                    else:  # cost_criterion == 'p'
                        step_cost = 0 if (current_line == edge['line']) or (current_line is None) else 1
                    
                    new_g = g + step_cost
                    new_time = edge['arr_sec']
                    
                    # Skip if this makes the path too costly
                    if next_stop in costs and costs[next_stop] <= new_g:
                        continue
                    
                    # Calculate heuristic with adaptive weight
                    if cost_criterion == 't':
                        h = self.heuristic_time(next_stop, target) * 1.2  # Slightly more aggressive heuristic
                    else:
                        h = self.heuristic_transfers(next_stop, target)
                    
                    # Create path and add to queue
                    new_path = path + [(edge['line'], current, edge['dep_sec'], next_stop, edge['arr_sec'])]
                    heapq.heappush(pq, (new_g + h, new_g, next_stop, new_time, new_path, edge['line']))
        
        return None, float('inf')
    
    def _is_too_far_from_path(self, current, next_stop, target, max_distance):
        """Check if next_stop is too far from the general path direction."""
        current_lat, current_lon = self.stops_coords[current]
        next_lat, next_lon = self.stops_coords[next_stop]
        target_lat, target_lon = self.stops_coords[target]
        
        # Calculate current distance to target
        current_to_target = haversine(current_lat, current_lon, target_lat, target_lon)
        
        # Calculate next stop distance to target
        next_to_target = haversine(next_lat, next_lon, target_lat, target_lon)
        
        # If next stop takes us away from target by more than the threshold, skip it
        if next_to_target > current_to_target * 1.5 and next_to_target > max_distance:
            return True
            
        return False
    
    def save_to_file(self, filename):
        """
        Serialize the transit graph to a file.
        
        Args:
            filename (str): Path to the file where the graph will be saved
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(filename, 'wb') as f:
                pickle.dump({
                    'graph': self.graph,
                    'stops_coords': self.stops_coords,
                    'direct_connections': self.direct_connections,
                    'reachable_from': self.reachable_from
                }, f)
            return True
        except Exception as e:
            print(f"Error saving graph: {e}")
            return False
    
    @classmethod
    def load_from_file(cls, filename):
        """
        Load a transit graph from a serialized file.
        
        Args:
            filename (str): Path to the file containing the serialized graph
            
        Returns:
            TransitGraph: Loaded graph object or None if loading failed
        """
        try:
            graph = cls()
            with open(filename, 'rb') as f:
                data = pickle.load(f)
                graph.graph = data['graph']
                graph.stops_coords = data['stops_coords']
                graph.direct_connections = data['direct_connections']
                graph.reachable_from = data['reachable_from']
            return graph
        except Exception as e:
            print(f"Error loading graph: {e}")
            return None
