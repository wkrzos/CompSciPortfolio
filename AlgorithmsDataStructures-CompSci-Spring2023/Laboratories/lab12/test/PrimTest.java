package test;

import java.util.ArrayList;
import java.util.List;

import util.algorithm.Prim;
import util.Edge;

public class PrimTest {

    public static void run() {

        Prim prim = new Prim();

        int numVertices = 4;
        List<Edge>[] adjacencyList = new List[numVertices];

        for (int i = 0; i < numVertices; i++) {
            adjacencyList[i] = new ArrayList<>();
        }

        adjacencyList[0].add(new Edge(0, 1, 2));
        adjacencyList[0].add(new Edge(0, 3, 6));
        adjacencyList[1].add(new Edge(1, 0, 2));
        adjacencyList[1].add(new Edge(1, 2, 3));
        adjacencyList[1].add(new Edge(1, 3, 8));
        adjacencyList[2].add(new Edge(2, 1, 3));
        adjacencyList[3].add(new Edge(3, 0, 6));
        adjacencyList[3].add(new Edge(3, 1, 8));


        List<Edge> minimumSpanningTree = prim.findMinimumSpanningTree(adjacencyList);

        System.out.println("Minimum Spanning Tree Edges:");
        for (Edge edge : minimumSpanningTree) {
            System.out.println(edge.from + " - " + edge.to + " : " + edge.weight);
        }
    }

}