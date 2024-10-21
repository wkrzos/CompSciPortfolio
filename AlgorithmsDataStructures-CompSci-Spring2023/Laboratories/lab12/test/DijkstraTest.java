package test;

import util.algorithm.Dijkstra;

public class DijkstraTest {

    public static void run() {

        System.out.println("DijkstraTest");

        Dijkstra dijkstra = new Dijkstra();

    int[][] graph = {
        {0, 4, 0, 2},
        {4, 0, 3, 0},
        {0, 3, 0, 1},
        {2, 0, 1, 0}
    };

        int source = 0;
        int[] distances = dijkstra.dijkstra(graph, source);

        System.out.println("Shortest distances from source node " + source + ":");
        for (int i = 0; i < distances.length; i++) {
            System.out.println("Node " + i + ": " + distances[i]);
        }
    }
}