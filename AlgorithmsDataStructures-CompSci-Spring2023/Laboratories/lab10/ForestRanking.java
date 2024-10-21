import java.util.ArrayList;

public class ForestRanking {
    private class Node {
        int val;
        int rank;
        Node parent;

        public Node(int val) {
            this.val = val;
            this.parent = null;
            this.rank = 0;
        }
    }

    private ArrayList<Node> list;

    public ForestRanking() {
        this.list = new ArrayList<>();
    }

    /**
     * The makeSet(int x) method creates a new set with a single element x by adding
     * a new Node object with the value x to the list.
     */
    public void makeSet(int x) {
        list.add(new Node(x));
    }

    /**
     * The findSet(int x) method is used to find the representative node of the set
     * that contains element x. It iterates over each Node in the list and traverses
     * the parent chain until it finds a Node with a matching value x. Once found,
     * it further traverses the parent chain to reach the representative node (i.e.,
     * the node with a null parent) and returns it.
     */
    public Node findSet(int x) {
        for (Node node : list) {
            while (node != null) {
                if (node.val == x) {
                    while (node.parent != null) {
                        node = node.parent;
                    }
                    return node;
                }
                node = node.parent;
            }
        }
        return null;
    }

    /**
     * The union(int x, int y) method performs the union operation between two sets
     * represented by elements x and y. It first finds the representative nodes for
     * x and y using the findSet method.
     * 
     * If the rank of nodex is greater than the rank of nodey, it means the set
     * represented by nodey should be merged into the set represented by nodex. The
     * parent of nodey is updated to nodex, and nodex is removed from the list since
     * it is no longer a representative node.
     * 
     * Otherwise, if the rank of nodex is less than or equal to the rank of nodey,
     * it means the set represented by nodex should be merged into the set
     * represented by nodey. The parent of nodex is updated to nodey, and if both
     * ranks are equal, the rank of nodey is incremented to maintain the tree
     * balance. Finally, nodey is removed from the list.
     */
    public void union(int x, int y) {
        Node nodeX = findSet(x);
        Node nodeY = findSet(y);
        if (nodeX.rank > nodeY.rank) {
            nodeY.parent = nodeX;
            list.remove(nodeX);
        } else {
            nodeX.parent = nodeY;
            if (nodeX.rank == nodeY.rank) {
                nodeY.rank++;
            }
            list.remove(nodeY);
        }
    }

    public void print() {
        System.out.println("Printing");
        for (Node curr : list) {
            while (curr != null) {
                System.out.print(curr.val + " ");
                curr = curr.parent;
            }
            System.out.println();
        }
    }
}
