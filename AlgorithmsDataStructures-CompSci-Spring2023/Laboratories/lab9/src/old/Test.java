package old;
import java.util.Scanner;

public class Test {
    public static void main(String[] args) {
        RedBlackTree tree = new RedBlackTree(-1);
        Scanner scanner = new Scanner(System.in);
        int choice;

        do {
            System.out.println("Red-Black Tree Menu:");
            System.out.println("1. Insert a node");
            System.out.println("2. Search for a node");
            System.out.println("3. Preorder traversal");
            System.out.println("4. Inorder traversal");
            System.out.println("5. Postorder traversal");
            System.out.println("6. Level order traversal");
            System.out.println("7. Get tree height");
            System.out.println("8. Get left subtree height");
            System.out.println("9. Get right subtree height");
            System.out.println("10. Get total number of nodes");
            System.out.println("11. Get number of nodes in left subtree");
            System.out.println("12. Get number of nodes in right subtree");
            System.out.println("13. Update subtree parameters");
            System.out.println("0. Exit");
            System.out.print("Enter your choice: ");
            choice = scanner.nextInt();

            switch (choice) {
                case 1:
                    System.out.print("Enter the value to insert: ");
                    int value = scanner.nextInt();
                    tree.insert(value);
                    System.out.println("Node inserted successfully!");
                    break;
                case 2:
                    System.out.print("Enter the value to search: ");
                    int searchValue = scanner.nextInt();
                    boolean found = tree.searchNode(searchValue);
                    if (found) {
                        System.out.println("Node found in the tree.");
                    } else {
                        System.out.println("Node not found in the tree.");
                    }
                    break;
                case 3:
                    System.out.println("Preorder Traversal:");
                    tree.preorderTraversal();
                    System.out.println();
                    break;
                case 4:
                    System.out.println("Inorder Traversal:");
                    tree.inorderTraversal();
                    System.out.println();
                    break;
                case 5:
                    System.out.println("Postorder Traversal:");
                    tree.postorderTraversal();
                    System.out.println();
                    break;
                case 6:
                    System.out.println("Level Order Traversal:");
                    tree.levelOrderTraversal();
                    break;
                case 7:
                    int height = tree.treeHeight();
                    System.out.println("Tree Height: " + height);
                    break;
                case 8:
                    int leftSubtreeHeight = tree.leftSubtreeHeight();
                    System.out.println("Left Subtree Height: " + leftSubtreeHeight);
                    break;
                case 9:
                    int rightSubtreeHeight = tree.rightSubtreeHeight();
                    System.out.println("Right Subtree Height: " + rightSubtreeHeight);
                    break;
                case 10:
                    int totalNodes = tree.countNodes();
                    System.out.println("Total Number of Nodes: " + totalNodes);
                    break;
                case 11:
                    int leftSubtreeNodes = tree.countNodesInLeftSubtree();
                    System.out.println("Number of Nodes in Left Subtree: " + leftSubtreeNodes);
                    break;
                case 12:
                    int rightSubtreeNodes = tree.countNodesInRightSubtree();
                    System.out.println("Number of Nodes in Right Subtree: " + rightSubtreeNodes);
                    break;
                case 13:
                    tree.updateSubtreeParameters();
                    System.out.println("Subtree parameters updated successfully!");
                    break;
                case 0:
                    System.out.println("Exiting...");
                    break;
                default:
                    System.out.println("Invalid choice. Please try again.");
                    break;
            }

            System.out.println();
        } while (choice != 0);

        scanner.close();
    }
}
