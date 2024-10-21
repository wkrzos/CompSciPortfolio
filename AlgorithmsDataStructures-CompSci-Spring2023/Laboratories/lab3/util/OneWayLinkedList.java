package util;

public class OneWayLinkedList<E> {

    public Element head;

    public class Element {

        private E data;
        private Element next;

        Element(E data) {
            this.data = data;
            next = null;
        }

        public E getValue() {
            return data;
        }

        public void setValue(E value) {
            this.data = value;
        }

        public Element getNext() {
            return next;
        }

        public void setNext(Element next) {
            this.next = next;
        }
    }

    // Method to insert a new node
    public OneWayLinkedList<E> insert(OneWayLinkedList<E> list, E data) {

        // Create a new node with given data
        Element new_node = new Element(data);

        // If the Linked List is empty,
        // then make the new node as head
        if (list.head == null) {
            list.head = new_node;
        } else {
            // Else traverse till the last node
            // and insert the new_node there
            Element last = list.head;
            while (last.next != null) {
                last = last.next;
            }

            // Insert the new_node at last node
            last.next = new_node;
        }

        // Return the list by head
        return list;
    }

    public void printList(OneWayLinkedList<E> list) {
        System.out.print("LinkedList: ");
        printListRecursive(list.head);
    }

    //helper
    private void printListRecursive(Element currNode) {
        if (currNode != null) {
            // Print the data at current node
            System.out.print(currNode.data + " ");
            // Call the function recursively with the next node
            printListRecursive(currNode.next);
        }
    }

    public void printListReverse(OneWayLinkedList<E> list) {
        System.out.print("LinkedList (reverse order): ");
        printListReverseRecursive(list.head);
        System.out.println();
    }

    private void printListReverseRecursive(Element currNode) {
        if (currNode == null) {
            return;
        }
        // Recursively print the next node
        printListReverseRecursive(currNode.next);
        // Print the data at current node
        System.out.print(currNode.data + " ");
    }

    public OneWayLinkedList<E> copy(OneWayLinkedList<E> list) {
        OneWayLinkedList<E> copyList = new OneWayLinkedList<>();
        copyList.head = copyListRecursive(list.head);
        return copyList;
    }

    private Element copyListRecursive(Element currNode) {
        if (currNode == null) {
            return null;
        }
        Element copiedNode = new Element(currNode.data);
        if (currNode.next != null) {
            copiedNode.next = copyListRecursive(currNode.next);
        }
        return copiedNode;
    }

    public int size() {
        return sizeRecursive(head);
    }

    private int sizeRecursive(Element currNode) {
        if (currNode == null) {
            return 0;
        }
        return 1 + sizeRecursive(currNode.next);
    }

    public int sumOfKeys(Element currNode) {
        if (currNode == null) {
            return 0;
        }
        return (Integer) currNode.data + sumOfKeys(currNode.next);
    }
}