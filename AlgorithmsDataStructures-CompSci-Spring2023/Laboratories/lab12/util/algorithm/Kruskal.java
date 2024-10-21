package util.algorithm;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import util.DisjointSet;
import util.Edge;

/**
 * This code implements the Kruskal's algorithm for finding the minimum spanning
 * tree of a graph. Here's a breakdown of the code:
 * 
 * 1. The code is in the package `util.algorithm`.
 * 
 * 2. The necessary imports are included at the beginning of the code.
 * 
 * 3. The `Kruskal` class contains a single method `findMinimumSpanningTree`,
 * which takes a list of edges (`List<Edge> edges`) and the number of vertices
 * (`int numVertices`) as input and returns a list of edges that form the
 * minimum spanning tree.
 * 
 * 4. Inside the method, a new `ArrayList` called `minimumSpanningTree` is
 * created to store the edges of the minimum spanning tree.
 * 
 * 5. A `DisjointSet` object called `disjointSet` is created with the specified
 * `numVertices`. The `DisjointSet` class is not shown in the code snippet, but
 * it is a data structure that allows efficient union-find operations.
 * 
 * 6. The edges in the `edges` list are sorted in non-decreasing order of their
 * weights using the `Collections.sort` method. The lambda expression `(a, b) ->
 * a.weight - b.weight` is used as the comparator to compare two edges based on
 * their weights.
 * 
 * 7. The code then iterates over each edge in the sorted `edges` list.
 * 
 * 8. For each edge, it finds the root vertices of the sets that contain the
 * vertices of the edge using the `find` method of the `DisjointSet` object. The
 * `find` method returns the representative (root) element of the set that
 * contains the specified element.
 * 
 * 9. It checks if the root vertices of the two sets are different, which means
 * including this edge will not create a cycle in the minimum spanning tree.
 * 
 * 10. If the root vertices are different, the edge is added to the
 * `minimumSpanningTree` list, and the two sets are merged using the `union`
 * method of the `DisjointSet` object. The `union` method merges the sets that
 * contain the specified elements by making one element the representative of
 * the other element's set.
 * 
 * 11. After processing all the edges, the `minimumSpanningTree` list is
 * returned, which contains the edges of the minimum spanning tree.
 * 
 * In summary, the code sorts the edges based on their weights and then iterates
 * over them in the sorted order, adding edges to the minimum spanning tree as
 * long as they do not create cycles. The `DisjointSet` data structure is used
 * to efficiently check for cycles and merge sets. The result is the minimum
 * spanning tree of the given graph.
 */

public class Kruskal {

    public List<Edge> findMinimumSpanningTree(List<Edge> edges, int numVertices) {
        List<Edge> minimumSpanningTree = new ArrayList<>();
        DisjointSet disjointSet = new DisjointSet(numVertices);

        /**
         * Sort the edges in non-decreasing order of their weights
         * 
         * `(a, b) -> a.weight - b.weight` is a lambda expression used as a
         * comparator for sorting the edges in the `edges` list based on their weights.
         * 
         * Let's break it down:
         * 
         * - `(a, b)` indicates that the lambda expression takes two parameters `a` and
         * `b`. These parameters represent two edges that need to be compared.
         * - `a.weight` and `b.weight` access the `weight` property of the edges `a` and
         * `b`, respectively. This assumes that the `Edge` class has a `weight`
         * property.
         * - `a.weight - b.weight` subtracts the weight of edge `b` from the weight of
         * edge `a`. This expression represents the comparison logic. If the result is
         * negative, it means that `a` should come before `b` in the sorted order. If
         * the result is positive, it means that `b` should come before `a` in the
         * sorted order. If the result is zero, it means that the weights of `a` and `b`
         * are equal.
         * 
         * By using this lambda expression as the comparator, the `Collections.sort`
         * method arranges the edges in the `edges` list in non-decreasing order of
         * their weights.
         */
        Collections.sort(edges, (a, b) -> a.weight - b.weight);

        for (Edge edge : edges) {
            int root1 = disjointSet.find(edge.from);
            int root2 = disjointSet.find(edge.to);

            // Check if including this edge creates a cycle
            if (root1 != root2) {
                minimumSpanningTree.add(edge);
                disjointSet.union(root1, root2);
            }
        }

        return minimumSpanningTree;
    }
}