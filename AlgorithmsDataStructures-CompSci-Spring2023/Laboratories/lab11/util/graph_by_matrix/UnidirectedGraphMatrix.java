package util.graph_by_matrix;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class UnidirectedGraphMatrix implements GraphMatrix {

    private static int ARR_SIZE = 10;

    private static int[][] matrix = new int[ARR_SIZE][ARR_SIZE];

    public UnidirectedGraphMatrix() {
        for (int i = 0; i < ARR_SIZE; i++)
            for (int j = 0; j < ARR_SIZE; j++)
                matrix[i][j] = 0;
    }

    @Override
    public void addVertex() {
        int newMatrixSize = ARR_SIZE + 1;
        int[][] newMatrix = new int[newMatrixSize][newMatrixSize];

        // Copy existing values from the old matrix to the new matrix
        for (int i = 0; i < ARR_SIZE; i++) {
            System.arraycopy(matrix[i], 0, newMatrix[i], 0, ARR_SIZE);
        }

        // Update the class variables with the new matrix and size
        matrix = newMatrix;
        ARR_SIZE = newMatrixSize;
    }

    @Override
    /**
     * adds only one-way connection, condratictory to the graph type, can be used
     * for directed graph
     */
    public void addConnection(int from, int to) {
        matrix[from][to] = 1;
    }

    @Override
    public void addEdge(int from, int to) {
        matrix[from][to] = 1;
        matrix[to][from] = 1;
    }

    @Override
    public void print() {
        System.out.println("\n");
        for (int i = 0; i < ARR_SIZE; i++) {
            for (int j = 0; j < ARR_SIZE; j++)
                System.out.print(matrix[i][j] + " ");
            System.out.println();
        }
    }

    public void dfs(int start) {
        boolean[] visitedDFS = new boolean[ARR_SIZE];
        dfsHelper(start, visitedDFS);
    }

    public void dfsHelper(int start, boolean[] visitedDFS) {

        visitedDFS[start] = true;
        System.out.print(start + " ");

        for (int i = 0; i < matrix[start].length; i++) {

            // If the node is adjacent to the current node and wasn't visited yet
            if (matrix[start][i] == 1 && (!visitedDFS[i])) {
                dfsHelper(i, visitedDFS);
            }
        }
    }

    public void bfs(int start) {

        List<Integer> q = new ArrayList<>();
        q.add(start);
        int vis;

        boolean[] visited = new boolean[ARR_SIZE];
        for (int k = 0; k < ARR_SIZE; k++)
            visited[k] = false;

        visited[start] = true;
        
        while (!q.isEmpty()) {

            vis = q.get(0);
            System.out.print(vis + " ");
            q.remove(q.get(0));

            for (int i = 0; i < ARR_SIZE; i++) {
                if (matrix[vis][i] == 1 && (!visited[i])) {
                    q.add(i);
                    visited[i] = true;
                }
            }
        }
    }
}
