package util;

import java.util.NoSuchElementException;

public class DoublyLinkedList {
    private Node head;
    private Node tail;
    private int size;

    private class Node {
        int value;
        Node next;
        Node prev;

        Node(int value) {
            this.value = value;
        }
    }

    public DoublyLinkedList() {
        head = null;
        tail = null;
        size = 0;
    }

    public int size() {
        return size;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    public void addFirst(int value) {
        Node newNode = new Node(value);
        if (head == null) {
            head = newNode;
            tail = newNode;
        } else {
            newNode.next = head;
            head.prev = newNode;
            head = newNode;
        }
        size++;
    }

    public void addLast(int value) {
        Node newNode = new Node(value);

        if (tail == null) {
            head = newNode;
            tail = newNode;
        } else {
            newNode.prev = tail;
            tail.next = newNode;
            tail = newNode;
        }
        size++;
    }

    public void add(int value, int index) {
        if (index < 0 || index > size) {
            throw new IndexOutOfBoundsException();
        }
        if (index == 0) {
            addFirst(value);
        } else if (index == size) {
            addLast(value);
        } else {
            Node curr = head;
            for (int i = 0; i < index; i++) {
                curr = curr.next;
            }
            Node newNode = new Node(value);
            newNode.next = curr;
            newNode.prev = curr.prev;
            curr.prev.next = newNode;
            curr.prev = newNode;
            size++;
        }
    }

    public int getFirst() {
        if (head == null) {
            throw new NoSuchElementException();
        }
        return head.value;
    }

    public int getLast() {
        if (tail == null) {
            throw new NoSuchElementException();
        }
        return tail.value;
    }

    public int get(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException();
        }
        if (index == 0) {
            return getFirst();
        } else if (index == size - 1) {
            return getLast();
        } else {
            Node curr = head;
            for (int i = 0; i < index; i++) {
                curr = curr.next;
            }
            return curr.value;
        }
    }

    public int removeFirst() {
        if (head == null) {
            throw new NoSuchElementException();
        }
        int value = head.value;
        if (head == tail) {
            head = null;
            tail = null;
        } else {
            head = head.next;
            head.prev = null;
        }
        size--;
        return value;
    }

    public int removeLast() {
        if (tail == null) {
            throw new NoSuchElementException();
        }
        int value = tail.value;
        if (head == tail) {
            head = null;
            tail = null;
        } else {
            tail = tail.prev;
            tail.next = null;
        }
        size--;
        return value;
    }

    public int remove(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException();
        }
        if (index == 0) {
            return removeFirst();
        } else if (index == size - 1) {
            return removeLast();
        } else {
            Node curr = head;
            for (int i = 0; i < index; i++) {
                curr = curr.next;
            }
            int value = curr.value;
            curr.prev.next = curr.next;
            curr.next.prev = curr.prev;
            size--;
            return value;
        }
    }

    public DoublyLinkedList joinListsAtEnd(DoublyLinkedList list2) {

        DoublyLinkedList newList = new DoublyLinkedList();
        Node curr = head;

        while (curr != null) {
            newList.addLast(curr.value);
            curr = curr.next;
        }

        curr = list2.head;

        while (curr != null) {
            newList.addLast(curr.value);
            curr = curr.next;
        }

        return newList;
    }
    
    public DoublyLinkedList joinListsBeforeIndex(DoublyLinkedList list2, int index) {

        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException("Invalid index");
        }

        DoublyLinkedList newList = new DoublyLinkedList();
        Node curr = head;
        int currIndex = 0;
        
        while (curr != null && currIndex < index) {
            newList.addLast(curr.value);
            curr = curr.next;
            currIndex++;
        }

        curr = list2.head;
        while (curr != null) {
            newList.addLast(curr.value);
            curr = curr.next;
        }

        while (currIndex < size) {
            newList.addLast(get(currIndex));
            currIndex++;
        }

        return newList;
    }

    public void displayList() {
        System.out.print("List elements: ");
        Node curr = head;
        while (curr != null) {
            System.out.print(curr.value + " ");
            curr = curr.next;
        }
        System.out.println();
    }
}

