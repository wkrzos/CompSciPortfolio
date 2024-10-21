package test;
import java.util.ArrayList;
import java.util.List;

import util.algorithm.Kruskal;
import util.Edge;

public class KruskalTest{
        public static void run()
    {
        List<Edge> edges = new ArrayList<>();
        
        edges.add(new Edge(0, 1, 2));
        edges.add(new Edge(1, 2, 3));
        edges.add(new Edge(0, 2, 1));
        edges.add(new Edge(1, 3, 4));
        edges.add(new Edge(2, 3, 5));

        Kruskal kruskal = new Kruskal();
        List<Edge> minimumSpanningTree = kruskal.findMinimumSpanningTree(edges, 4);

        System.out.println("Minimum Spanning Tree Edges:");
        for (Edge edge : minimumSpanningTree) {
            System.out.println(edge.from + " - " + edge.to + " : " + edge.weight);
        }
    }
}