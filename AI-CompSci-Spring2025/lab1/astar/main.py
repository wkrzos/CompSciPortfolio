import sys
import time
import argparse
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # An amazing way to import modules from the parent directory, unfortunately proposed by Claude 3.7
from common.time_utils import time_to_seconds, seconds_to_time_str
from common.data_loader import load_transit_data
from common.transit_graph import TransitGraph

def main():
    parser = argparse.ArgumentParser(description="Wyszukiwanie najkrótszych połączeń")
    parser.add_argument('start_stop', help="Przystanek początkowy A")
    parser.add_argument('target_stop', help="Przystanek końcowy B")
    parser.add_argument('criterion', choices=['t', 'p'], help="Kryterium optymalizacyjne: t (czas) lub p (przesiadki)")
    parser.add_argument('start_time', help="Czas pojawienia się na przystanku A (HH:MM:SS)")
    parser.add_argument('--rebuild', action='store_true', help="Wymuś przebudowanie grafu")
    args = parser.parse_args()

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
    
    # Convert start time to seconds
    start_sec = time_to_seconds(args.start_time)
    
    # Start timer before running the algorithm
    t0 = time.time()
    
    # Find path using A* algorithm
    path, cost = transit_graph.find_path_a_star(
        args.start_stop, 
        args.target_stop, 
        start_sec, 
        cost_criterion=args.criterion
    )
    
    # Calculate execution time
    elapsed = time.time() - t0

    # Output results
    if path:
        for segment in path:
            line, board_stop, dep, alight_stop, arr = segment
            dep_time = seconds_to_time_str(dep)
            arr_time = seconds_to_time_str(arr)
            print(f"Linia: {line}, Wsiadamy: {board_stop} o {dep_time}, Wysiadamy: {alight_stop} o {arr_time}")
    else:
        print("Nie znaleziono połączenia")

    sys.stderr.write(f"Wartość funkcji kosztu: {cost}\n")
    sys.stderr.write(f"Czas obliczeń: {elapsed} sekund\n")

if __name__ == '__main__':
    main()
