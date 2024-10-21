package utility;

public class Node {
    public int key;
    Node left, right;
    int subtreeHeight;
    int subtreeSize;

    public Node(int key) {
        this.key = key;
        this.subtreeHeight = 1;
        this.subtreeSize = 1;
    }
}
