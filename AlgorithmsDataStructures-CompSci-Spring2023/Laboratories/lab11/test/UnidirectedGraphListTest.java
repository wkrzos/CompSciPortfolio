package test;

import util.graph_by_list.UnidirectedGraphList;

public class UnidirectedGraphListTest {
    public void run(){
        System.out.println("\nUnidirectedGraphListTest");
        UnidirectedGraphList graph = new UnidirectedGraphList(10);
        graph.printGraph();
        graph.addEdge(1, 2);
        graph.addEdge(2, 4);
        graph.addEdge(4, 2);
        graph.addEdge(1, 3);
        graph.addEdge(1, 5);
        graph.addEdge(6, 1);
        graph.printGraph();
        System.out.println("\ndfs");
        graph.dfs(1);
        System.out.println("\nbfs");
        graph.bfs(1);
    }
}
