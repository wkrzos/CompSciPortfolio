import java.util.Arrays;

import util.PriorityHeap;

public class Excercise1Test {
    static void testEx1() {
        // Create a new priority heap with capacity 10
        PriorityHeap heap = new PriorityHeap(10);

        // Add some elements to the heap
        heap.enqueue(5);
        heap.enqueue(3);
        heap.enqueue(8);
        heap.enqueue(1);
        heap.enqueue(6);
        heap.printHeap(); // prints: 8 6 5 1 3

        // Remove an element from the heap
        heap.remove(2);
        heap.printHeap(); // prints: 8 6 3 1

        // Change the priority of an element in the heap
        heap.changePriority(1, 10);
        heap.printHeap(); // prints: 10 8 3 1

        // Sort an array using a priority queue
        int[] arr = { 4, 6, 1, 3, 8 };
        int[] sorted = new int[arr.length];

        while(!heap.isEmpty()) {
            heap.dequeue();
        }

        for (int i = 0; i < arr.length; i++) {
            heap.enqueue(arr[i]);
        }

        for (int i = 0; i < sorted.length; i++) {
            sorted[i] = heap.dequeue();
        }

        System.out.println(Arrays.toString(sorted)); // prints: [8, 6, 4, 3, 1]
    }
}
