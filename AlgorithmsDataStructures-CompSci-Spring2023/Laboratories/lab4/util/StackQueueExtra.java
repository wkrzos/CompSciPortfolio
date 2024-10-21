package util;

import java.util.NoSuchElementException;

public class StackQueueExtra<E> {
    private Stack<E> inStack;
    private Stack<E> outStack;

    public StackQueueExtra() {
        inStack = new Stack<>();
        outStack = new Stack<>();
    }

    public void enqueue(E data) {
        inStack.push(data);
    }

    public E dequeue() {
        if (isEmpty()) {
            throw new NoSuchElementException();
        }

        if (outStack.isEmpty()) {
            while (!inStack.isEmpty()) {
                outStack.push(inStack.pop());
            }
        }

        return outStack.pop();
    }

    public E peek() {
        if (isEmpty()) {
            throw new NoSuchElementException();
        }

        if (outStack.isEmpty()) {
            while (!inStack.isEmpty()) {
                outStack.push(inStack.pop());
            }
        }

        return outStack.peek();
    }

    public boolean isEmpty() {
        return inStack.isEmpty() && outStack.isEmpty();
    }
}