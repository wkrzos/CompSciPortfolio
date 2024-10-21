import java.util.Arrays;
import java.util.Random;

import util.PriorityHeap;

public class Excercise2Test {

    public static void testEx2() {
        int n = 20; // liczba elementów w tablicy
        int valueToSearch = new Random().nextInt(n); // losowa wartość do wyszukania
        int[] array = new int[n];
        fillWithRandom(array);
        int linearResult = linearSearch(array, valueToSearch);
        System.out.println("Wyszukiwanie liniowe: " + linearResult + " porównań");

        heapSort(array);
        int binaryResult = binarySearch(array, valueToSearch);
        System.out.println("Wyszukiwanie binarne: " + binaryResult + " porównań");

        int hits = 0;
        int misses = 0;
        int totalComparisons = 0;
        for (int i = 0; i < n; i++) {
            Counter counter = new Counter();
            int result = binarySearch(array, array[i], counter);
            totalComparisons += counter.getCount();
            if (result == i) {
                hits++;
            } else {
                misses++;
            }
        }
        System.out.println("Średnia liczba porównań przy trafionych wyszukiwaniach: "
                + (double) totalComparisons / hits);
        System.out.println("Średnia liczba porównań przy chybionych wyszukiwaniach: "
                + (double) totalComparisons / misses);
        System.out.println("Łączna średnia liczba porównań: "
                + (double) totalComparisons / n);
    }

    private static void fillWithRandom(int[] array) {
        Random random = new Random();
        for (int i = 0; i < array.length; i++) {
            array[i] = random.nextInt();
        }
    }

    private static int linearSearch(int[] array, int valueToSearch) {
        int comparisons = 0;
        for (int i = 0; i < array.length; i++) {
            comparisons++;
            if (array[i] == valueToSearch) {
                return comparisons;
            }
        }
        return comparisons;
    }

    private static void heapSort(int[] array) {
        PriorityHeap heap = new PriorityHeap(array.length);
        for (int i = 0; i < array.length; i++) {
            heap.enqueue(array[i]);
        }
        for (int i = array.length - 1; i >= 0; i--) {
            array[i] = heap.dequeue();
        }
    }

    private static int binarySearch(int[] array, int valueToSearch) {
        return binarySearch(array, valueToSearch, new Counter());
    }

    private static int binarySearch(int[] array, int valueToSearch, Counter counter) {
        int left = 0;
        int right = array.length - 1;
        while (left <= right) {
            int middle = (left + right) / 2;
            counter.increment();
            if (array[middle] == valueToSearch) {
                return counter.getCount();
            } else if (array[middle] > valueToSearch) {
                right = middle - 1;
            } else {
                left = middle + 1;
            }
        }
        return counter.getCount();
    }
}

class Counter {
    private int count;

    public void increment() {
        count++;
    }

    public int getCount() {
        return count;
    }
}