package old;
// Creating a node for the red-black tree. A node has left and right child, element, and color of the node.

import java.util.LinkedList;
import java.util.Queue;

// Create class CreateRedBlackTree for creating a red-black tree.
class RedBlackTree {
    protected static Node nullNode; // Define null node.
    private Node current; // Define current node.
    private Node parent; // Define parent node.
    private Node header; // Define header node.
    private Node grand; // Define grand node.
    private Node great; // Define great node.

    // Create two variables, RED and BLACK, for color, and the values of these
    // variables are 0 and 1, respectively.
    static final int RED = 0;
    static final int BLACK = 1;

    // Using static initializer for initializing the null Node.
    static {
        nullNode = new Node(0);
        nullNode.leftChild = nullNode;
        nullNode.rightChild = nullNode;
    }

    // Constructor for creating the header node.
    public RedBlackTree(int header) {
        this.header = new Node(header);
        this.header.leftChild = nullNode;
        this.header.rightChild = nullNode;
    }

    // Create removeAll() to make the tree logically empty.
    public void removeAll() {
        header.rightChild = nullNode;
    }

    // Create checkEmpty() to check whether the tree is empty or not.
    public boolean isEmpty() {
        return header.rightChild == nullNode;
    }

    // TODO after inserting increasing values, the method deletes the smaller ones
    // Create insertNewNode() method for adding a new node in the red-black tree.
    public void insert(int newElement) {
        current = parent = grand = header; // Set header value to current, parent, and grand node.
        nullNode.element = newElement; // Set newElement to the element of the null node.

        // Repeat statements until the element of the current node is equal to the value
        // of the newElement.
        while (current.element != newElement) {
            great = grand;
            grand = parent;
            parent = current;

            // If the value of the newElement is lesser than the current node element,
            // the current node will point to the current left child, else point to the
            // current right child.
            current = newElement < current.element ? current.leftChild : current.rightChild;

            // Check whether both children are RED or NOT. If both children are RED, change
            // them using handleColors().
            if (current.leftChild.color == RED && current.rightChild.color == RED) {
                handleColors(newElement);
            }
        }

        // Insertion of the new node will fail if it is already present in the tree.
        if (current != nullNode) {
            return;
        }

        // Create a node with no left and right child and pass it to the current node.
        current = new Node(newElement, nullNode, nullNode);

        // Connect the current node with the parent.
        if (newElement < parent.element) {
            parent.leftChild = current;
        } else {
            parent.rightChild = current;
        }
        handleColors(newElement);
    }

    // Create handleColors() method to maintain the colors of Red-black tree nodes.
    private void handleColors(int newElement) {
        // Flip the colors of the node.
        current.color = RED; // Make current node RED.
        current.leftChild.color = BLACK; // Make leftChild BLACK.
        current.rightChild.color = BLACK; // Make rightChild BLACK.

        // Check the color of the parent node.
        if (parent.color == RED) {
            // Perform rotation when the color of parent node is RED.
            grand.color = RED;

            if (newElement < grand.element && grand.element != newElement && newElement < parent.element) {
                parent = performRotation(newElement, grand); // Start double rotation.
            }
            current = performRotation(newElement, great);
            current.color = BLACK;
        }

        // Change the color of the root node to BLACK.
        header.rightChild.color = BLACK;
    }

    // Create performRotation() method to perform double rotation.
    private Node performRotation(int newElement, Node parent) {
        // Check whether the value of the newElement is lesser than the element of the
        // parent node or not.
        if (newElement < parent.element) {
            // If true, perform the rotation with the left child and right child based on
            // the condition
            // and set the return value to the left child of the parent node.
            return parent.leftChild = newElement < parent.leftChild.element ? rotationWithLeftChild(parent.leftChild)
                    : rotationWithRightChild(parent.leftChild);
        } else {
            // If false, perform the rotation with the left child and right child based on
            // the condition
            // and set the return value to the right child of the parent node.
            return parent.rightChild = newElement < parent.rightChild.element ? rotationWithLeftChild(parent.rightChild)
                    : rotationWithRightChild(parent.rightChild);
        }
    }

    // Create rotationWithLeftChild() method for rotating a binary tree node with
    // the left child.
    private Node rotationWithLeftChild(Node node2) {
        Node node1 = node2.leftChild;
        node2.leftChild = node1.rightChild;
        node1.rightChild = node2;
        return node1;
    }

    // Create rotationWithRightChild() method for rotating a binary tree node with
    // the right child.
    private Node rotationWithRightChild(Node node1) {
        Node node2 = node1.rightChild;
        node1.rightChild = node2.leftChild;
        node2.leftChild = node1.leftChild;
        return node2;
    }

    // Create nodesInTree() method for getting the total number of nodes in a tree.
    public int nodesInTree() {
        return nodesInTree(header.rightChild);
    }

    private int nodesInTree(Node node) {
        if (node == nullNode) {
            return 0;
        } else {
            int size = 1;
            size += nodesInTree(node.leftChild);
            size += nodesInTree(node.rightChild);
            return size;
        }
    }

    // Create searchNode() method to get the desired node from the Red-Black tree.
    public boolean searchNode(int value) {
        return searchNode(header.rightChild, value);
    }

    private boolean searchNode(Node node, int value) {
        boolean check = false;
        while (node != nullNode && !check) {
            int nodeValue = node.element;
            if (value < nodeValue) {
                node = node.leftChild;
            } else if (value > nodeValue) {
                node = node.rightChild;
            } else {
                check = true;
                System.out.println(node.toString()); 
                break;
            }
            check = searchNode(node, value);
        }
        return check;
    }

    // Create preorderTraversal() method to perform preorder traversal.
    public void preorderTraversal() {
        preorderTraversal(header.rightChild);
    }

    private void preorderTraversal(Node node) {
        if (node != nullNode) {
            char c = 'R';
            if (node.color == BLACK) {
                c = 'B';
            }
            System.out.print(node.element + "" + c + " ");
            preorderTraversal(node.leftChild);
            preorderTraversal(node.rightChild);
        }
    }

    // Create inorderTraversal() method to perform inorder traversal.
    public void inorderTraversal() {
        inorderTraversal(header.rightChild);
    }

    private void inorderTraversal(Node node) {
        if (node != nullNode) {
            inorderTraversal(node.leftChild);
            char c = 'R';
            if (node.color == BLACK) {
                c = 'B';
            }
            System.out.print(node.element + "" + c + " ");
            inorderTraversal(node.rightChild);
        }
    }

    // Create postorderTraversal() method to perform postorder traversal.
    public void postorderTraversal() {
        postorderTraversal(header.rightChild);
    }

    private void postorderTraversal(Node node) {
        if (node != nullNode) {
            postorderTraversal(node.leftChild);
            postorderTraversal(node.rightChild);
            char c = 'R';
            if (node.color == BLACK) {
                c = 'B';
            }
            System.out.print(node.element + "" + c + " ");
        }
    }

    public void levelOrderTraversal() {
        if (header.rightChild == nullNode) {
            System.out.println("Tree is empty");
            return;
        }

        Queue<Node> queue = new LinkedList<>();
        queue.offer(header.rightChild);

        while (!queue.isEmpty()) {
            int levelSize = queue.size();

            for (int i = 0; i < levelSize; i++) {
                Node node = queue.poll();
                char c = 'R';
                if (node.color == BLACK) {
                    c = 'B';
                }
                System.out.print(node.element + "" + c + " ");

                if (node.leftChild != nullNode) {
                    queue.offer(node.leftChild);
                }
                if (node.rightChild != nullNode) {
                    queue.offer(node.rightChild);
                }
            }

            System.out.println();
        }
    }

    // Metoda do obliczania wysokości drzewa
    public int treeHeight() {
        return treeHeight(header);
    }

    private int treeHeight(Node node) {
        if (node == nullNode) {
            return -1;
        } else {
            int leftHeight = treeHeight(node.leftChild);
            int rightHeight = treeHeight(node.rightChild);
            return Math.max(leftHeight, rightHeight) + 1;
        }
    }

    // Metoda do obliczania wysokości lewego poddrzewa
    public int leftSubtreeHeight() {
        return leftSubtreeHeight(header.rightChild);
    }

    private int leftSubtreeHeight(Node node) {
        if (node == nullNode) {
            return -1;
        } else {
            return leftSubtreeHeight(node.leftChild) + 1;
        }
    }

    // Metoda do obliczania wysokości prawego poddrzewa
    public int rightSubtreeHeight() {
        return rightSubtreeHeight(header.rightChild);
    }

    private int rightSubtreeHeight(Node node) {
        if (node == nullNode) {
            return -1;
        } else {
            return rightSubtreeHeight(node.rightChild) + 1;
        }
    }

    // Metoda do obliczania liczby węzłów w drzewie
    public int countNodes() {
        return countNodes(header.rightChild);
    }

    private int countNodes(Node node) {
        if (node == nullNode) {
            return 0;
        } else {
            int leftCount = countNodes(node.leftChild);
            int rightCount = countNodes(node.rightChild);
            return leftCount + rightCount + 1;
        }
    }

    // Metoda do obliczania liczby węzłów w lewym poddrzewie
    public int countNodesInLeftSubtree() {
        return countNodes(header.rightChild.leftChild);
    }

    // Metoda do obliczania liczby węzłów w prawym poddrzewie
    public int countNodesInRightSubtree() {
        return countNodes(header.rightChild.rightChild);
    }

    // Metoda do aktualizacji parametrów poddrzewa dla każdego węzła
    public void updateSubtreeParameters() {
        updateSubtreeParameters(header.rightChild);
    }

    private void updateSubtreeParameters(Node node) {
        if (node != nullNode) {
            // Aktualizuj liczbę węzłów w lewym poddrzewie
            node.nodesLeftSubtree = countNodes(node.leftChild);

            // Aktualizuj liczbę węzłów w prawym poddrzewie
            node.nodesRightSubtree = countNodes(node.rightChild);

            // Aktualizuj wysokość lewego poddrzewa
            node.heightLeftSubtree = treeHeight(node.leftChild);

            // Aktualizuj wysokość prawego poddrzewa
            node.heightRightSubtree = treeHeight(node.rightChild);

            // Rekurencyjnie aktualizuj parametry poddrzewa dla lewego i prawego dziecka
            updateSubtreeParameters(node.leftChild);
            updateSubtreeParameters(node.rightChild);
        }
    }
}
