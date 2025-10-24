#!/usr/bin/env python3
import sys
import time
import argparse
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # An amazing way to import modules from the parent directory, unfortunately proposed by Claude 3.7
from common.time_utils import time_to_seconds, seconds_to_time_str
from common.transit_graph import TransitGraph
from common.data_loader import load_transit_data

# Import all Tabu Search variants
from tabu_search_a import BasicTabuSearch
from tabu_search_b import DynamicTabuSearch
from tabu_search_c import AspirationTabuSearch

def main():
    parser = argparse.ArgumentParser(description="Wyszukiwanie trasy przy użyciu przeszukiwania Tabu")
    parser.add_argument('start_stop', help="Przystanek początkowy A")
    parser.add_argument('stops_to_visit', help="Lista przystanków do odwiedzenia (oddzielone średnikiem)")
    parser.add_argument('criterion', choices=['t', 'p'], help="Kryterium optymalizacyjne: t (czas) lub p (przesiadki)")
    parser.add_argument('start_time', help="Czas pojawienia się na przystanku początkowym (HH:MM:SS)")
    parser.add_argument('--algorithm', choices=['a', 'b', 'c'], default='a',
                        help="Wariant algorytmu: a - podstawowy, b - dynamiczny rozmiar listy tabu, c - z kryterium aspiracji")
    parser.add_argument('--rebuild', action='store_true', help="Wymuś przebudowanie grafu")
    args = parser.parse_args()

    # Load transit graph
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
    
    # Parse stops to visit
    stops_to_visit = args.stops_to_visit.split(';')
    
    # Create the appropriate Tabu Search solver based on the selected algorithm
    if args.algorithm == 'a':
        sys.stderr.write("Używanie podstawowego przeszukiwania Tabu...\n")
        tabu_solver = BasicTabuSearch(
            transit_graph, 
            args.start_stop, 
            stops_to_visit, 
            start_sec, 
            criterion=args.criterion
        )
    elif args.algorithm == 'b':
        sys.stderr.write("Używanie przeszukiwania Tabu z dynamicznym rozmiarem listy...\n")
        tabu_solver = DynamicTabuSearch(
            transit_graph, 
            args.start_stop, 
            stops_to_visit, 
            start_sec, 
            criterion=args.criterion
        )
    elif args.algorithm == 'c':
        sys.stderr.write("Używanie przeszukiwania Tabu z kryterium aspiracji...\n")
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
    if best_path:
        for segment in best_path:
            line, board_stop, dep, alight_stop, arr = segment
            dep_time = seconds_to_time_str(dep)
            arr_time = seconds_to_time_str(arr)
            print(f"Linia: {line}, Wsiadamy: {board_stop} o {dep_time}, Wysiadamy: {alight_stop} o {arr_time}")
    else:
        print("Nie znaleziono połączenia")

    sys.stderr.write(f"Wartość funkcji kosztu: {best_cost}\n")
    sys.stderr.write(f"Czas obliczeń: {execution_time} sekund\n")

if __name__ == '__main__':
    main()
