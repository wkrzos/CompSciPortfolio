package util.algorithm;

import java.util.ArrayList;
import java.util.List;
import java.util.PriorityQueue;

import util.Edge;

/**
 * This code implements Prim's algorithm for finding the minimum spanning tree
 * of a graph. Here's a breakdown of the code:
 * 
 * 1. The code is in the package `util.algorithm`.
 * 
 * 2. The necessary imports are included at the beginning of the code.
 * 
 * 3. The `Prim` class contains a single method `findMinimumSpanningTree`, which
 * takes an adjacency list (`List<Edge>[] adjacencyList`) as input and returns a
 * list of edges that form the minimum spanning tree.
 * 
 * 4. Inside the method, the number of vertices (`numVertices`) is determined by
 * the length of the adjacency list.
 * 
 * 5. Three arrays are created to store information about the vertices:
 * - `visited` is a boolean array to keep track of which vertices have been
 * visited.
 * - `parent` is an array to store the parent of each vertex in the minimum
 * spanning tree.
 * - `key` is an array to store the minimum weight of the edge connecting each
 * vertex to the minimum spanning tree.
 * 
 * 6. The `key` array is initialized with `Integer.MAX_VALUE` for all vertices,
 * except for the first vertex, which is set to 0. The `parent` of the first
 * vertex is set to -1.
 * 
 * 7. A `PriorityQueue` called `minHeap` is created to store the edges. The
 * edges are added to the `minHeap` with an initial edge `(0, 0, 0)`. The `Edge`
 * class is not shown in the code snippet, but it is assumed to have properties
 * `from`, `to`, and `weight` that represent the source vertex, destination
 * vertex, and weight of the edge, respectively.
 * 
 * 8. The algorithm enters a loop that continues until the `minHeap` is empty.
 * 
 * 9. In each iteration of the loop, the minimum-weight edge `currentEdge` is
 * removed from the `minHeap`.
 * 
 * 10. The destination vertex `u` of the `currentEdge` is checked to see if it
 * has already been visited. If it has, the iteration continues to the next
 * iteration.
 * 
 * 11. If `u` has not been visited, it is marked as visited by setting
 * `visited[u]` to `true`.
 * 
 * 12. The algorithm then iterates over the edges adjacent to vertex `u` in the
 * `adjacencyList`.
 * 
 * 13. For each adjacent edge, the destination vertex `v` and the weight of the
 * edge are retrieved.
 * 
 * 14. If vertex `v` has not been visited and the weight of the edge is smaller
 * than the current minimum weight `key[v]`, the `parent` of vertex `v` is
 * updated to `u`, the `key` of vertex `v` is updated to the weight of the edge,
 * and a new edge `(u, v, weight)` is added to the `minHeap`.
 * 
 * 15. After processing all adjacent edges of vertex `u`, the loop continues to
 * the next iteration.
 * 
 * 16. Once the loop finishes, the minimum spanning tree edges are extracted
 * from the `parent` and `key` arrays.
 * 
 * 17. The `minimumSpanningTree` list is created to store the edges of the
 * minimum spanning tree.
 * 
 * 18. A loop iterates over the `parent` and `key` arrays starting from index 1
 * (since the first vertex is already in the minimum spanning tree).
 * 
 * 19. For each vertex, the `from` vertex is set to the parent and the `to`
 * vertex is set to the current vertex. The weight is retrieved from the `key`
 * array.
 * 
 * 20. A new `Edge` object is created with the `from`, `to`, and `weight`, and
 * it is added to the `minimumSpanningTree` list.
 * 
 * 21. Finally, the `minimumSpanningTree` list, which contains the edges of the
 * minimum spanning tree, is
 * 
 * returned.
 * 
 * In summary, the code uses Prim's algorithm to find the minimum spanning tree
 * of a graph. It maintains a priority queue of edges, selects the
 * minimum-weight edge in each iteration, and updates the `key` and `parent`
 * arrays to gradually build the minimum spanning tree. The result is the
 * minimum spanning tree represented as a list of edges.
 */

public class Prim {

    public static List<Edge> findMinimumSpanningTree(List<Edge>[] adjacencyList) {
        int numVertices = adjacencyList.length;
        boolean[] visited = new boolean[numVertices];
        int[] parent = new int[numVertices];
        int[] key = new int[numVertices];

        for (int i = 0; i < numVertices; i++) {
            key[i] = Integer.MAX_VALUE;
        }

        key[0] = 0;
        parent[0] = -1;

        PriorityQueue<Edge> minHeap = new PriorityQueue<>();
        minHeap.offer(new Edge(0, 0, 0));

        while (!minHeap.isEmpty()) {
            Edge currentEdge = minHeap.poll();
            int u = currentEdge.to;

            if (visited[u]) {
                continue;
            }

            visited[u] = true;

            for (Edge edge : adjacencyList[u]) {
                int v = edge.to;
                int weight = edge.weight;

                if (!visited[v] && weight < key[v]) {
                    parent[v] = u;
                    key[v] = weight;
                    minHeap.offer(new Edge(u, v, weight));
                }
            }
        }

        List<Edge> minimumSpanningTree = new ArrayList<>();
        for (int i = 1; i < numVertices; i++) {
            int from = parent[i];
            int to = i;
            int weight = key[i];
            minimumSpanningTree.add(new Edge(from, to, weight));
        }

        return minimumSpanningTree;
    }
}
