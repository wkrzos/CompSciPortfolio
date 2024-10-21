package util;

public class PriorityHeap {
    private int[] heap;
    private int size;

    public PriorityHeap(int capacity) {
        heap = new int[capacity];
        size = 0;
    }

    public void enqueue(int value) {
        if (size == heap.length) {
            throw new IllegalStateException("Kolejka priorytetowa jest pełna");
        }

        heap[size] = value;
        siftUp(size);
        size++;
    }

    public int dequeue() {
        if (isEmpty()) {
            throw new IllegalStateException("Kolejka priorytetowa jest pusta");
        }

        int root = heap[0];
        heap[0] = heap[size - 1];
        size--;
        siftDown(0);
        return root;
    }

    public void changePriority(int index, int priority) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException("Indeks spoza zakresu kolejki");
        }

        int oldPriority = heap[index];
        heap[index] = priority;

        if (priority > oldPriority) {
            siftUp(index);
        } else {
            siftDown(index);
        }
    }

    public void remove(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException("Indeks spoza zakresu kolejki");
        }

        heap[index] = heap[size - 1];
        size--;
        siftDown(index);
    }

    public boolean isEmpty() {
        return size == 0;
    }

    // Used after adding a new element to the heap to maintain the heap property
    // (parent > children)
    private void siftUp(int index) {
        int parent = (index - 1) / 2;

        while (index > 0 && heap[index] > heap[parent]) {
            swap(index, parent);
            index = parent;
            parent = (index - 1) / 2;
        }
    }

    // Used after removing the root element to maintain the heap property (parent >
    // children)
    private void siftDown(int index) {
        int leftChild = 2 * index + 1;
        int rightChild = 2 * index + 2;
        int maxIndex = index;

        if (leftChild < size && heap[leftChild] > heap[maxIndex]) {
            maxIndex = leftChild;
        }

        if (rightChild < size && heap[rightChild] > heap[maxIndex]) {
            maxIndex = rightChild;
        }

        if (index != maxIndex) {
            swap(index, maxIndex);
            siftDown(maxIndex);
        }
    }

    private void swap(int i, int j) {
        int temp = heap[i];
        heap[i] = heap[j];
        heap[j] = temp;
    }

    public void printHeap() {
        for (int i = 0; i < size; i++) {
            System.out.print(heap[i] + " ");
        }
        System.out.println();
    }
}
