package util;

import java.util.NoSuchElementException;

public class DrowningStack<E> {
    private E[] array;
    private int size;
    private int top;
    private int bottom;

    public DrowningStack(int capacity) {
        this.array = (E[]) new Object[capacity];
        this.size = 0;
        this.top = 0;
        this.bottom = 0;
    }

    /*
     * The push method in this implementation of a DrowningStack data structure adds
     * an item to the top of the stack. Here's how the method works:
     * 
     * If the stack is already full (i.e., size == array.length), then the bottom
     * index of the stack is moved up by one to make room for the new item. This is
     * done by using the modulo operator % to "wrap around" to the beginning of the
     * array if necessary. This ensures that the stack always remains circular and
     * that the oldest item in the stack is always at the bottom index.
     * 
     * If the stack is not full, then the size of the stack is incremented by one to
     * reflect the addition of the new item.
     * 
     * The item is added to the top of the stack by assigning it to the current top
     * index of the array.
     * 
     * The top index is then incremented by one to point to the next available
     * position in the stack. Again, the modulo operator % is used to wrap around to
     * the beginning of the array if necessary.
     * 
     * Overall, the push method maintains the circular nature of the DrowningStack
     * data structure by adjusting the top and bottom indices as needed when items
     * are added or removed from the stack.
     */

    public void push(E item) {
        if (size == array.length) {
            bottom = (bottom + 1) % array.length;
        } else {
            size++;
        }
        array[top] = item;
        top = (top + 1) % array.length;
    }

    /*
     * The pop method in this implementation of a DrowningStack data structure
     * removes and returns the item at the top of the stack. Here's how the method
     * works:
     * 
     * If the stack is empty (i.e., size == 0), then the method throws a
     * NoSuchElementException with the message "Stack is empty".
     * 
     * If the stack is not empty, then the item at the top of the stack is retrieved
     * by indexing into the array at the top-1 position. Since the stack is
     * circular, the % operator is used to wrap around to the end of the array if
     * the top-1 position goes out of bounds.
     * 
     * The top index is then decremented by one to reflect the removal of the item
     * from the stack. Again, the % operator is used to wrap around to the end of
     * the array if the top index goes out of bounds.
     * 
     * The size of the stack is decremented by one to reflect the removal of the
     * item.
     * 
     * The item that was retrieved from the top of the stack is returned.
     * 
     * Overall, the pop method maintains the circular nature of the DrowningStack
     * data structure by adjusting the top and bottom indices as needed when items
     * are added or removed from the stack.
     */

    public E pop() {

        if (isEmpty()) {
            throw new NoSuchElementException("Stack is empty");
        }

        E item = array[(top - 1 + array.length) % array.length];
        top = (top - 1 + array.length) % array.length;
        size--;

        return item;
    }

    public E peek() {
        if (isEmpty()) {
            throw new NoSuchElementException("Stack is empty");
        }
        return array[(top - 1 + array.length) % array.length];
    }

    public boolean isEmpty() {
        return size == 0;
    }

    public int size() {
        return size;
    }
}