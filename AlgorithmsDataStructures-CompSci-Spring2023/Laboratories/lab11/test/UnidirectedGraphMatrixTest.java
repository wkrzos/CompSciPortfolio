package test;

import util.graph_by_matrix.UnidirectedGraphMatrix;

public class UnidirectedGraphMatrixTest {
    public void run(){
        System.out.println("\nUnidirectedGraphMatrixTest");
        UnidirectedGraphMatrix graph = new UnidirectedGraphMatrix();
        graph.print();
        graph.addEdge(1, 2);
        graph.addEdge(2, 4);
        graph.addEdge(4, 2);
        graph.addEdge(1, 3);
        graph.addEdge(1, 5);
        graph.addEdge(6, 1);
        graph.print();
        System.out.println("\ndfs");
        graph.dfs(1);
        System.out.println("\nbfs");
        graph.bfs(1);
        System.out.println("\naddVertex");
        graph.addVertex();
        graph.print();
    }
}
