package util.graph_by_matrix;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;
import java.util.Set;

public class DirectedGraphMatrix implements GraphMatrix {

    private static int ARR_SIZE = 10;

    private int[][] matrix = new int[ARR_SIZE][ARR_SIZE];

    public DirectedGraphMatrix() {
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
    public void addConnection(int from, int to) {
        matrix[from][to] = 1;
    }

    @Override
    public void addEdge(int from, int to) {
        matrix[from][to] = 1;
    }

    @Override
    public void print() {
        System.out.println();
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
        int vis; // current visited vertex

        boolean[] visited = new boolean[ARR_SIZE];
        for (int k = 0; k < ARR_SIZE; k++)
            visited[k] = false;

        visited[start] = true;

        // q is empty when all vertices are visited
        while (!q.isEmpty()) {

            vis = q.get(0);
            System.out.print(vis + " ");
            q.remove(q.get(0)); // removing visited element

            /*
             * A for loop is used to iterate through all the vertices in the graph,
             * represented by the variable i.
             * 
             * If there is an edge between the currently visited vertex vis and the vertex i
             * (as indicated by matrix[vis][i] == 1), and the vertex i has not been visited
             * before (!visited[i]), it is added to the queue q, and visited[i] is set to
             * true.
             * 
             * After the loop finishes, the process continues with the next vertex in the
             * queue until all vertices have been visited.
             * 
             * [1][2] 1 row, 2 column
             */
            for (int i = 0; i < ARR_SIZE; i++) {
                if (matrix[vis][i] == 1 && (!visited[i])) {
                    q.add(i);
                    visited[i] = true;
                }
            }
        }
    }
}
