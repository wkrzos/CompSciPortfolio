package util.graph_by_list;

import java.util.LinkedList;
import java.util.Queue;

public class DirectedGraphList implements GraphList {
    private int numVertices;
    private LinkedList<Integer>[] adjacencyList;

    public DirectedGraphList(int numVertices) {
        this.numVertices = numVertices;
        adjacencyList = new LinkedList[numVertices];

        for (int i = 0; i < numVertices; i++) {
            adjacencyList[i] = new LinkedList<>();
        }
    }

    public void addEdge(int source, int destination) {
        adjacencyList[source].add(destination);
    }

    public void printGraph() {
        for (int i = 0; i < numVertices; i++) {
            System.out.print(i + "->");
            for (int j : adjacencyList[i]) {
                System.out.print(j + " ");
            }
            System.out.println();
        }
    }

    public void dfs(int start) {
        boolean[] visited = new boolean[numVertices];
        dfsHelper(start, visited);
    }
    
    private void dfsHelper(int vertex, boolean[] visited) {
        visited[vertex] = true;
        System.out.print(vertex + " ");
    
        for (int neighbor : adjacencyList[vertex]) {
            if (!visited[neighbor]) {
                dfsHelper(neighbor, visited);
            }
        }
    }

    public void bfs(int start) {
        boolean[] visited = new boolean[numVertices];
        Queue<Integer> queue = new LinkedList<>();

        visited[start] = true;
        queue.add(start);

        while (!queue.isEmpty()) {
            int vertex = queue.poll();
            System.out.print(vertex + " ");

            for (int neighbor : adjacencyList[vertex]) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    queue.add(neighbor);
                }
            }
        }
    }
}