package utility;

import java.util.LinkedList;
import java.util.Queue;

public class ExpandedBST extends BST {

    public void displayLevelOrder() {
        int h = height(root);
        int i;
        for (i = 1; i <= h; i++) {
            printGivenLevel(root, i);
            System.out.println();
        }
    }

    void printGivenLevel(Node node, int level) {
        if (node == null)
            return;
        if (level == 1)
            System.out.print(node.key + " ");
        else if (level > 1) {
            printGivenLevel(node.left, level - 1);
            printGivenLevel(node.right, level - 1);
        }
    }

    // Method to display keys level by level
    public void displayByLevel() {
        if (root == null) {
            System.out.println("Tree is empty");
            return;
        }

        Queue<Node> queue = new LinkedList<>();
        queue.add(root);

        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            for (int i = 0; i < levelSize; i++) {
                Node current = queue.poll();
                System.out.print(current.key + " ");
                if (current.left != null)
                    queue.add(current.left);
                if (current.right != null)
                    queue.add(current.right);
            }
            System.out.println();
        }
    }

    // Method to find successor node of given key
    public Node findSuccessor(int key) {
        Node current = findNode(key);

        if (current == null)
            return null;

        if (current.right != null) {
            // Successor is the leftmost node in the right subtree
            current = current.right;
            while (current.left != null)
                current = current.left;
            return current;
        } else {
            // Successor is the closest ancestor whose left child is also an ancestor of the
            // current node
            Node ancestor = root;
            Node successor = null;
            while (ancestor != current) {
                if (current.key < ancestor.key) {
                    successor = ancestor;
                    ancestor = ancestor.left;
                } else {
                    ancestor = ancestor.right;
                }
            }
            return successor;
        }
    }

    // Method to find predecessor node of given key
    public Node findPredecessor(int key) {
        Node current = findNode(key);

        if (current == null)
            return null;

        if (current.left != null) {
            // Predecessor is the rightmost node in the left subtree
            current = current.left;
            while (current.right != null)
                current = current.right;
            return current;
        } else {
            // Predecessor is the closest ancestor whose right child is also an ancestor of
            // the current node
            Node ancestor = root;
            Node predecessor = null;
            while (ancestor != current) {
                if (current.key > ancestor.key) {
                    predecessor = ancestor;
                    ancestor = ancestor.right;
                } else {
                    ancestor = ancestor.left;
                }
            }
            return predecessor;
        }
    }

    // Method to find node with given key
    public Node findNode(int key) {
        Node current = root;

        while (current != null) {
            if (key == current.key) {
                return current;
            } else if (key < current.key) {
                current = current.left;
            } else {
                current = current.right;
            }
        }

        return null;
    }

    public void delete(int key) {
        root = deleteNode(root, key);
    }

    private Node deleteNode(Node current, int key) {
        if (current == null)
            return null;

        if (key < current.key) {
            current.left = deleteNode(current.left, key);
        } else if (key > current.key) {
            current.right = deleteNode(current.right, key);
        } else {
            // Node to be deleted has been found
            if (current.left == null && current.right == null) {
                // Case 1: Node to be deleted is a leaf node
                return null;
            } else if (current.left == null) {
                // Case 2: Node to be deleted has only right child
                return current.right;
            } else if (current.right == null) {
                // Case 2: Node to be deleted has only left child
                return current.left;
            } else {
                // Case 3: Node to be deleted has both left and right child
                // Find successor node and replace current node with it
                Node successor = findSuccessor(current.key);
                current.key = successor.key;
                current.right = deleteNode(current.right, successor.key);
            }
        }
        return current;
    }

    private void calculateSubtreeInfo(Node current) {
        if (current == null) {
            return;
        }

        int leftSubtreeHeight = height(current.left);
        int rightSubtreeHeight = height(current.right);
        int leftSubtreeSize = size(current.left);
        int rightSubtreeSize = size(current.right);

        current.subtreeHeight = Math.max(leftSubtreeHeight, rightSubtreeHeight) + 1;
        current.subtreeSize = leftSubtreeSize + rightSubtreeSize + 1;

        calculateSubtreeInfo(current.left);
        calculateSubtreeInfo(current.right);
    }

    // Method to calculate the size of the subtree rooted at the given node
    private int size(Node node) {
        if (node == null)
            return 0;
        else
            return 1 + size(node.left) + size(node.right);
    }

/*     public void displayAsciiTree() {
        System.out.println(getAsciiTree(root, ""));
    }

    private String getAsciiTree(Node node, String prefix) {
        StringBuilder builder = new StringBuilder();

        if (node == null) {
            return "";
        }

        String leftPrefix = prefix + "  ";
        String rightPrefix = prefix + "  ";
        builder.append(getAsciiTree(node.right, rightPrefix));

        builder.append(prefix);
        builder.append(node.key);
        builder.append("\n");

        builder.append(getAsciiTree(node.left, leftPrefix));

        return builder.toString();
    } */

/*     public void displayAsciiTree() {
        drawTree(root, "");
    }
    
    private void drawTree(Node node, String prefix) {
        if (node == null) {
            return;
        }
    
        String nodeString = "[" + node.key + "]";
        System.out.println(prefix + nodeString);
    
        String childPrefix = prefix + "├─ ";
        String emptyPrefix = prefix + "│  ";
    
        if (node.left != null && node.right != null) {
            drawTree(node.left, childPrefix);
            drawTree(node.right, emptyPrefix);
        } else if (node.left != null) {
            drawTree(node.left, childPrefix);
        } else if (node.right != null) {
            drawTree(node.right, childPrefix);
        }
    } */

    public void displayAsciiTree() {
        if (root == null) {
            System.out.println("Tree is empty.");
            return;
        }
    
        displayTreeHelper(root, 0);
    }
    
    private void displayTreeHelper(Node node, int level) {
        if (node == null) {
            return;
        }
    
        // Display right subtree
        displayTreeHelper(node.right, level + 1);
    
        // Indentation based on the level
        for (int i = 0; i < level; i++) {
            System.out.print("    ");
        }
    
        // Display current node
        System.out.println(node.key);
    
        // Display left subtree
        displayTreeHelper(node.left, level + 1);
    }
}
