import java.util.Scanner;

public class ConsolControl {
  private RedBlackTree redBlackTree;
  private Scanner scanner;

  public ConsolControl() {
    redBlackTree = new RedBlackTree();
    scanner = new Scanner(System.in);
  }

  private void printMenu() {
    System.out.println("Red-Black Tree Operations:");
    System.out.println("1. Insert a node");
    System.out.println("2. Delete a node");
    System.out.println("3. Search for a node");
    System.out.println("4. Print the tree");
    System.out.println("5. Print the number of nodes");
    System.out.println("6. Print the number of nodes in the left subtree");
    System.out.println("7. Print the number of nodes in the right subtree");
    System.out.println("8. Print the height of the left subtree");
    System.out.println("9. Print the height of the right subtree");
    System.out.println("10. Pre-order traversal");
    System.out.println("11. In-order traversal");
    System.out.println("12. Post-order traversal");
    System.out.println("13. Update tree parameters");
    System.out.println("14. Exit");
  }

  private void insertNode() {
    System.out.print("Enter the value to insert: ");
    int value = scanner.nextInt();
    redBlackTree.insert(value);
    System.out.println("Node inserted successfully.");
  }

  private void deleteNode() {
    System.out.print("Enter the value to delete: ");
    int value = scanner.nextInt();
    redBlackTree.deleteNode(value);
    System.out.println("Node deleted successfully.");
  }

  private void searchNode() {
    System.out.print("Enter the value to search: ");
    int value = scanner.nextInt();
    Node result = redBlackTree.searchTree(value);
    if (result != null) {
      System.out.println("Node found in the tree. Parameters:");
        System.out.println("Value: " + result.data);
        System.out.println("Color: " + result.color);
        System.out.println("Height of the left subtree: " + result.heightLeftSubtree);
        System.out.println("Height of the right subtree: " + result.heightRightSubtree);
        System.out.println("Number of nodes in the left subtree: " + result.numLeftSubtreeNodes);
        System.out.println("Number of nodes in the right subtree: " + result.numRightSubtreeNodes);
    } else {
      System.out.println("Node not found in the tree.");
    }
  }

  private void printTree() {
    redBlackTree.prettyPrint();
  }

  private void printNumNodes() {
    int numNodes = redBlackTree.countNodes(redBlackTree.getRoot());
    System.out.println("Number of nodes in the tree: " + numNodes);
  }

  private void printNumNodesInLeftSubtree() {
    int numNodes = redBlackTree.countNodesLeftSubtree();
    System.out.println("Number of nodes in the left subtree: " + numNodes);
  }

  private void printNumNodesInRightSubtree() {
    int numNodes = redBlackTree.countNodesRightSubtree();
    System.out.println("Number of nodes in the right subtree: " + numNodes);
  }

  private void printHeightOfLeftSubtree() {
    int height = redBlackTree.calculateLeftSubtreeHeight();
    System.out.println("Height of the left subtree: " + height);
  }

  private void printHeightOfRightSubtree() {
    int height = redBlackTree.calculateRightSubtreeHeight();
    System.out.println("Height of the right subtree: " + height);
  }

  private void preOrderTraversal() {
    System.out.println("Pre-order traversal:");
    redBlackTree.preorder();
    System.out.println();
  }

  private void inOrderTraversal() {
    System.out.println("In-order traversal:");
    redBlackTree.inorder();
    System.out.println();
  }

  private void postOrderTraversal() {
    System.out.println("Post-order traversal:");
    redBlackTree.postorder();
    System.out.println();
  }

  private void updateTreeParameters() {
    redBlackTree.updateSubtreeParameters();
    System.out.println("Tree parameters updated successfully.");
  }

  public void start() {
    boolean exit = false;

    while (!exit) {
      printMenu();
      System.out.print("Enter your choice: ");
      int choice = scanner.nextInt();

      switch (choice) {
        case 1:
          insertNode();
          break;
        case 2:
          deleteNode();
          break;
        case 3:
          searchNode();
          break;
        case 4:
          printTree();
          break;
        case 5:
          printNumNodes();
          break;
        case 6:
          printNumNodesInLeftSubtree();
          break;
        case 7:
          printNumNodesInRightSubtree();
          break;
        case 8:
          printHeightOfLeftSubtree();
          break;
        case 9:
          printHeightOfRightSubtree();
          break;
        case 10:
          preOrderTraversal();
          break;
        case 11:
          inOrderTraversal();
          break;
        case 12:
          postOrderTraversal();
          break;
        case 13:
          updateTreeParameters();
          break;
        case 14:
          exit = true;
          break;
        default:
          System.out.println("Invalid choice. Please try again.");
          break;
      }

      System.out.println();
    }
  }
}
