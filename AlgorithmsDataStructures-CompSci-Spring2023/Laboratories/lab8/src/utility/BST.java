package utility;

public class BST {

    public Node root;

    public BST() {
        root = null;
    }

    public void insert(int key) {
        root = insertRec(root, key);
    }

    public Node insertRec(Node root, int key) {
        if (root == null) {
            root = new Node(key);
            return root;
        }

        if (key < root.key) {
            root.left = insertRec(root.left, key);
        } else if (key > root.key) {
            root.right = insertRec(root.right, key);
        }

        return root;
    }

    public void inorderTraversal(Node node) {
        if (node != null) {
            inorderTraversal(node.left);
            System.out.print(node.key + " ");
            inorderTraversal(node.right);
        }
    }

    public void preorderTraversal(Node node) {
        if (node != null) {
            System.out.print(node.key + " ");
            preorderTraversal(node.left);
            preorderTraversal(node.right);
        }
    }

    public void postorderTraversal(Node node) {
        if (node != null) {
            postorderTraversal(node.left);
            postorderTraversal(node.right);
            System.out.print(node.key + " ");
        }
    }

    public Node search(Node root, int key) {
        if (root == null || root.key == key) {
            return root;
        }

        if (key < root.key) {
            return search(root.left, key);
        } else {
            return search(root.right, key);
        }
    }

    public int findMin(Node root) {
        int min = root.key;

        while (root.left != null) {
            min = root.left.key;
            root = root.left;
        }

        return min;
    }

    public int findMax(Node root) {
        int max = root.key;

        while (root.right != null) {
            max = root.right.key;
            root = root.right;
        }

        return max;
    }

    public int height(Node node) {
        if (node == null) {
            return 0;
        } else {
            int leftHeight = height(node.left);
            int rightHeight = height(node.right);

            if (leftHeight > rightHeight) {
                return (leftHeight + 1);
            } else {
                return (rightHeight + 1);
            }
        }
    }

    public int countNodes(Node node) {
        if (node == null) {
            return 0;
        } else {
            int leftCount = countNodes(node.left);
            int rightCount = countNodes(node.right);

            return (leftCount + rightCount + 1);
        }
    }

    public int countLeaves(Node node) {
        if (node == null) {
            return 0;
        }

        if (node.left == null && node.right == null) {
            return 1;
        } else {
            int leftCount = countLeaves(node.left);
            int rightCount = countLeaves(node.right);

            return (leftCount + rightCount);
        }
    }
}