package util;

import java.util.NoSuchElementException;

public class FIFOQueue<T> {

    private Node<T> first;
    private Node<T> last;

    private static class Node<T> {
        private T element;
        private Node<T> next;

        public Node(T element) {
            this.element = element;
            this.next = null;
        }
    }

    public void enqueue(T element) {

        Node<T> newNode = new Node<>(element);

        if (isEmpty()) {
            first = newNode;
            last = newNode;
        } else {
            last.next = newNode;
            last = newNode;
        }
    }

    public T dequeue() {

        if (isEmpty()) {
            throw new NoSuchElementException();
        }

        T element = first.element;
        first = first.next;

        if (first == null) {
            last = null;
        }
        
        return element;
    }

    public boolean isEmpty() {
        return first == null;
    }
}