package old;
class Node {
    Node leftChild, rightChild;
    int element;
    int color;
    int heightLeftSubtree;
    int heightRightSubtree;
    int nodesLeftSubtree;
    int nodesRightSubtree;

    // Constructor to set the value of a node having no left and right child.
    public Node(int element) {
        this(element, null, null);
    }

    // Constructor to set the value of element, leftChild, rightChild, and color.
    public Node(int element, Node leftChild, Node rightChild) {
        this.element = element;
        this.leftChild = leftChild;
        this.rightChild = rightChild;
        color = 1;
        heightLeftSubtree = 0;
        heightRightSubtree = 0;
        nodesLeftSubtree = 0;
        nodesRightSubtree = 0;
    }

    @Override
    public String toString() {
        return "RedBlackNode{" +
                "element=" + element +
                ", color=" + color +
                ", heightLeftSubtree=" + heightLeftSubtree +
                ", heightRightSubtree=" + heightRightSubtree +
                ", nodesLeftSubtree=" + nodesLeftSubtree +
                ", nodesRightSubtree=" + nodesRightSubtree +
                '}';
    }
}