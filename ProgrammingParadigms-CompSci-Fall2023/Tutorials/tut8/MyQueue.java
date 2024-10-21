package tut8;

public interface MyQueue<E> {
    void enqueue(E x) throws FullException;
    void dequeue() throws EmptyException;
    E first() throws EmptyException;
    boolean isEmpty();
    boolean isFull();
}
