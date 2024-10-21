package main;

import java.util.Scanner;

import utility.ExpandedBST;
import utility.Node;

public class ExpandedConsoleMenu {

    public void run() {
        Scanner input = new Scanner(System.in);
        ExpandedBST tree = new ExpandedBST();
        int choice;

        do {
            System.out.println("===== ExpandedBST Menu =====");
            System.out.println("1. Insert a node");
            System.out.println("2. Display tree by level");
            System.out.println("3. Display tree by depth");
            System.out.println("4. Find successor of a node");
            System.out.println("5. Find predecessor of a node");
            System.out.println("6. Delete a node");
            System.out.println("7. Exit");
            System.out.println("============================");

            System.out.print("Enter your choice: ");
            choice = input.nextInt();

            switch (choice) {
                case 1:
                    System.out.print("Enter the key of the node to insert: ");
                    int key = input.nextInt();
                    tree.insert(key);
                    System.out.println("Node with key " + key + " has been inserted");
                    break;
                case 2:
                    System.out.println("Tree displayed by level:");
                    tree.displayByLevel();
                    break;
                case 3:
                    System.out.println("Tree displayed by depth:");
                    tree.displayAsciiTree();
                    break;
                case 4:
                    System.out.print("Enter the key of the node to find the successor of: ");
                    int successorKey = input.nextInt();
                    Node successor = tree.findSuccessor(successorKey);
                    if (successor == null) {
                        System.out.println("No successor found");
                    } else {
                        System.out.println("The successor of node with key " + successorKey + " is node with key " + successor.key);
                    }
                    break;
                case 5:
                    System.out.print("Enter the key of the node to find the predecessor of: ");
                    int predecessorKey = input.nextInt();
                    Node predecessor = tree.findPredecessor(predecessorKey);
                    if (predecessor == null) {
                        System.out.println("No predecessor found");
                    } else {
                        System.out.println("The predecessor of node with key " + predecessorKey + " is node with key " + predecessor.key);
                    }
                    break;
                case 6:
                    System.out.print("Enter the key of the node to delete: ");
                    int deleteKey = input.nextInt();
                    tree.delete(deleteKey);
                    System.out.println("Node with key " + deleteKey + " has been deleted");
                    break;
                case 7:
                    System.out.println("Exiting program...");
                    break;
                default:
                    System.out.println("Invalid choice, please try again");
                    break;
            }
        } while (choice != 7);
    }
}
