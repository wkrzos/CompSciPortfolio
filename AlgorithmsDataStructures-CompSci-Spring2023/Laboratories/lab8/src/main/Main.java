package main;

import java.util.Scanner;

import utility.ExpandedBST;

public class Main {
    public static void main(String[] args) {
        //expandedBSTTest();
        chooseMenu();
    }

    private static void chooseMenu(){

        Scanner input = new Scanner(System.in);
        int choice;

        do {
            System.out.println("===== Menu =====");
            System.out.println("1. Basic BST");
            System.out.println("2. Expanded BST");
            System.out.println("3. Exit");
            System.out.println("================");

            System.out.print("Enter your choice: ");
            choice = input.nextInt();

            switch (choice) {
                case 1:
                    BasicConsoleMenu menu1 = new BasicConsoleMenu();
                    menu1.run();
                    break;
                case 2:
                    ExpandedConsoleMenu menu2 = new ExpandedConsoleMenu();
                    menu2.run();
                    break;
                case 3:
                    System.out.println("Exiting...");
                    break;
                default:
                    System.out.println("Invalid choice");
                    break;
            }
        } while (choice != 3);

        input.close();
    }

    private static void expandedBSTTest(){
        // Create a tree
        ExpandedBST tree = new ExpandedBST();
        tree.insert(10);
        tree.insert(5);
        tree.insert(15);
        tree.insert(3);
        tree.insert(7);
        tree.insert(12);
        tree.insert(18);

        // Display the tree
        System.out.println("Inorder traversal of the given tree");
        tree.inorderTraversal(tree.root);

        // Display the tree by level
        System.out.println("\n\nDisplay the tree by level");
        tree.displayByLevel();

        // Display the tree level by level
        System.out.println("\n\nDisplay the tree level by level");
        tree.displayLevelOrder();

        // Find successor of 10
        System.out.println("\n\nSuccessor of 10 is: " + tree.findSuccessor(10).key);

        // Find predecessor of 10
        System.out.println("Predecessor of 10 is: " + tree.findPredecessor(10).key);

        // Display the tree
        System.out.println("\nDisplay the tree");
        tree.displayAsciiTree();
    }
}