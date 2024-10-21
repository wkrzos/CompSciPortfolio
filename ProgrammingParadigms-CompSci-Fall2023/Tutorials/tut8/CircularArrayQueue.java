package tut8;

import java.util.ArrayList;

public class CircularArrayQueue<E> implements MyQueue<E> {
    private ArrayList<E> queue;
    private int front, rear, size, capacity;

    public CircularArrayQueue(int capacity) {
        this.capacity = capacity;
        queue = new ArrayList<>(capacity);
        for (int i = 0; i < capacity; i++) {
            queue.add(null);
        }
        front = size = 0;
        rear = capacity - 1;
    }

    @Override
    public void enqueue(E x) throws FullException {
        if (isFull()) {
            throw new FullException("Queue is full");
        }
        rear = (rear + 1) % capacity;
        queue.set(rear, x);
        size++;
    }

    @Override
    public void dequeue() throws EmptyException {
        if (isEmpty()) {
            throw new EmptyException("Queue is empty");
        }
        front = (front + 1) % capacity;
        size--;
    }

    @Override
    public E first() throws EmptyException {
        if (isEmpty()) {
            throw new EmptyException("Queue is empty");
        }
        return queue.get(front);
    }

    @Override
    public boolean isEmpty() {
        return size == 0;
    }

    @Override
    public boolean isFull() {
        return size == capacity;
    }
}