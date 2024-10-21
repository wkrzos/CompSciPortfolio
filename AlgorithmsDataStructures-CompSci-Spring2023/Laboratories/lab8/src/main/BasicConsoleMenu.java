package main;

import java.util.Scanner;

import utility.BST;
import utility.Node;

public class BasicConsoleMenu {

    public void run() {

        Scanner scanner = new Scanner(System.in);
        BST bst = new BST();

        int choice = 0;

        do {
            System.out.println("\nChoose an option:");
            System.out.println("1. Insert a node");
            System.out.println("2. Inorder traversal");
            System.out.println("3. Preorder traversal");
            System.out.println("4. Postorder traversal");
            System.out.println("5. Search for a node");
            System.out.println("6. Find the minimum value");
            System.out.println("7. Find the maximum value");
            System.out.println("8. Find the height of the tree");
            System.out.println("9. Count the number of nodes");
            System.out.println("10. Count the number of leaves");
            System.out.println("0. Exit");

            choice = scanner.nextInt();

            switch (choice) {
                case 1:
                    System.out.print("Enter the value to insert: ");
                    int value = scanner.nextInt();
                    bst.insert(value);
                    System.out.println("Value inserted successfully.");
                    break;
                case 2:
                    System.out.print("Inorder traversal: ");
                    bst.inorderTraversal(bst.root);
                    break;
                case 3:
                    System.out.print("Preorder traversal: ");
                    bst.preorderTraversal(bst.root);
                    break;
                case 4:
                    System.out.print("Postorder traversal: ");
                    bst.postorderTraversal(bst.root);
                    break;
                case 5:
                    System.out.print("Enter the value to search for: ");
                    int searchValue = scanner.nextInt();
                    Node result = bst.search(bst.root, searchValue);
                    if (result == null) {
                        System.out.println("Value not found.");
                    } else {
                        System.out.println("Value found.");
                    }
                    break;
                case 6:
                    int minValue = bst.findMin(bst.root);
                    System.out.println("Minimum value is " + minValue);
                    break;
                case 7:
                    int maxValue = bst.findMax(bst.root);
                    System.out.println("Maximum value is " + maxValue);
                    break;
                case 8:
                    int height = bst.height(bst.root);
                    System.out.println("Height of the tree is " + height);
                    break;
                case 9:
                    int numNodes = bst.countNodes(bst.root);
                    System.out.println("Number of nodes is " + numNodes);
                    break;
                case 10:
                    int numLeaves = bst.countLeaves(bst.root);
                    System.out.println("Number of leaves is " + numLeaves);
                    break;
                case 0:
                    System.out.println("Exiting program...");
                    break;
                default:
                    System.out.println("Invalid choice. Please try again.");
                    break;
            }

        } while (choice != 0);

        scanner.close();
    }
}
