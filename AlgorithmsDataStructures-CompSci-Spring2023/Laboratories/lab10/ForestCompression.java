import java.util.ArrayList;

public class ForestCompression {
    private class Node {
        int val;
        Node parent;

        public Node(int val) {
            this.val = val;
            this.parent = null;
        }
    }

    private ArrayList<Node> list;

    public ForestCompression() {
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
     * the node with a null parent) and returns it. During the process, it performs
     * path compression by updating the parent references of the nodes encountered
     * along the path to directly point to the representative node, reducing the
     * length of the path for future findSet operations.
     */
    public Node findSet(int x) {
        Node curr;

        for (Node node : list) {
            curr = node;
            
            while (curr != null) {
                if (curr.val == x) {
                    while (curr.parent != null) {
                        curr = curr.parent;
                    }
                    return curr;
                }
                curr = curr.parent;
            }
        }

        return null;
    }

    /**
     * The compressNode(int x) method performs path compression for a specific node
     * x. It searches for the node x in the list and traverses the parent chain
     * until it finds the node x or reaches the end of the chain. It then retrieves
     * the representative node p by traversing the parent chain of the current node
     * curr. If the parent of curr is not null and is different from p, it means
     * that curr is not directly pointing to the representative node. In that case,
     * it adds the parent of curr to the list. Finally, it updates the parent
     * reference of curr to point to p, effectively compressing the path to the
     * representative node.
     */
    public void compressNode(int x) {
        Node curr = null;
        for (Node node : list) {
            curr = node;
            while (curr.parent != null && curr.val != x) {
                curr = curr.parent;
            }
            if (curr.val == x) {
                break;
            }
        }
        Node p = curr;
        while (p.parent != null) {
            p = p.parent;
        }
        if (curr.parent != null && curr.parent != p) {
            list.add(curr.parent);
        }
        if (curr.parent != null) {
            curr.parent = p;
        }
    }

    /**
     * The union(int x, int y) method performs the union operation between two sets
     * represented by elements x and y. It first applies path compression to both x
     * and y by calling the compressNode method. Then, it retrieves the
     * representative nodes nodex and nodey for x and y, respectively, using the
     * findSet method. It sets the parent of nodey to nodex, effectively merging the
     * sets. Finally, it removes the representative node nodex from the list since
     * it is no longer a representative node.
     */
    public void union(int x, int y) {
        compressNode(x);
        compressNode(y);
        Node nodex = findSet(x);
        Node nodey = findSet(y);
        nodey.parent = nodex;
        list.remove(nodex);
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
