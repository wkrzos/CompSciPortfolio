package test;

import util.graph_by_matrix.DirectedGraphMatrix;

public class DirectedGraphMatrixTest {
    public void run(){
        System.out.println("\nDirectedGraphMatrixTest");
        DirectedGraphMatrix graph = new DirectedGraphMatrix();
        graph.print();
        graph.addEdge(1, 2);
        graph.addEdge(2, 4);
        graph.addEdge(4, 2);
        graph.addEdge(1, 3);
        graph.addEdge(1, 5);
        graph.addEdge(6, 1);
        graph.print();
        System.out.println("\nDFS");
        graph.dfs(1);
        System.out.println("\nBFS");
        graph.bfs(1);
        System.out.println("\naddVertex");
        graph.addVertex();
        graph.print();
    }
}
