package main;

import java.util.Scanner;

import utility.ExpandedBST;
import utility.Node;

public class BSTMenu {

    private static ExpandedBST bst = new ExpandedBST();

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int choice;

        do {
            System.out.println("1. Insert a key");
            System.out.println("2. Inorder traversal");
            System.out.println("3. Preorder traversal");
            System.out.println("4. Postorder traversal");
            System.out.println("5. Search for a key");
            System.out.println("6. Find minimum key");
            System.out.println("7. Find maximum key");
            System.out.println("8. Get tree height");
            System.out.println("9. Get total number of nodes");
            System.out.println("10. Get total number of leaves");
            System.out.println("11. Display level order");
            System.out.println("12. Display keys by level");
            System.out.println("13. Find successor");
            System.out.println("14. Find predecessor");
            System.out.println("15. Delete a key");
            System.out.println("16. Display ASCII tree");
            System.out.println("0. Exit");
            System.out.print("Enter your choice: ");
            choice = scanner.nextInt();

            switch (choice) {
                case 1:
                    System.out.print("Enter the key to insert: ");
                    int key = scanner.nextInt();
                    bst.insert(key);
                    bst.insert(key);
                    System.out.println("Key inserted successfully.");
                    break;
                case 2:
                    System.out.print("Inorder traversal: ");
                    bst.inorderTraversal(bst.root);
                    System.out.println();
                    break;
                case 3:
                    System.out.print("Preorder traversal: ");
                    bst.preorderTraversal(bst.root);
                    System.out.println();
                    break;
                case 4:
                    System.out.print("Postorder traversal: ");
                    bst.postorderTraversal(bst.root);
                    System.out.println();
                    break;
                case 5:
                    System.out.print("Enter the key to search: ");
                    int searchKey = scanner.nextInt();
                    Node searchResult = bst.search(bst.root, searchKey);
                    if (searchResult != null) {
                        System.out.println("Key found in the tree.");
                    } else {
                        System.out.println("Key not found in the tree.");
                    }
                    break;
                case 6:
                    int min = bst.findMin(bst.root);
                    System.out.println("Minimum key: " + min);
                    break;
                case 7:
                    int max = bst.findMax(bst.root);
                    System.out.println("Maximum key: " + max);
                    break;
                case 8:
                    int height = bst.height(bst.root);
                    System.out.println("Tree height: " + height);
                    break;
                case 9:
                    int nodeCount = bst.countNodes(bst.root);
                    System.out.println("Total number of nodes: " + nodeCount);
                    break;
                case 10:
                    int leafCount = bst.countLeaves(bst.root);
                    System.out.println("Total number of leaves: " + leafCount);
                    break;
                case 11:
                    System.out.println("Level order traversal:");
                    bst.displayLevelOrder();
                    break;
                case 12:
                    System.out.println("Keys by level:");
                    bst.displayByLevel();
                    break;
                case 13:
                    System.out.print("Enter the key to find successor: ");
                    int successorKey = scanner.nextInt();
                    Node successor = bst.findSuccessor(successorKey);
                    if (successor != null) {
                        System.out.println("Successor of " + successorKey + ": " + successor.key);
                    } else {
                        System.out.println("No successor found for " + successorKey);
                    }
                    break;
                case 14:
                    System.out.print("Enter the key to find predecessor: ");
                    int predecessorKey = scanner.nextInt();
                    Node predecessor = bst.findPredecessor(predecessorKey);
                    if (predecessor != null) {
                        System.out.println("Predecessor of " + predecessorKey + ": " + predecessor.key);
                    } else {
                        System.out.println("No predecessor found for " + predecessorKey);
                    }
                    break;
                case 15:
                    System.out.print("Enter the key to delete: ");
                    int deleteKey = scanner.nextInt();
                    bst.delete(deleteKey);
                    bst.delete(deleteKey);
                    System.out.println("Key deleted successfully.");
                    break;
                case 16:
                    System.out.println("ASCII tree:");
                    bst.displayAsciiTree();
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
