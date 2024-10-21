package utilOriginal;

import java.util.Comparator;

import main.*;

public class CarSorters {
    public static void bubbleSort(Car[] cars, Comparator<Car> comparator) {
        boolean swapped;
        do {
            swapped = false;
            for (int i = 0; i < cars.length - 1; i++) {
                if (comparator.compare(cars[i], cars[i + 1]) > 0) {
                    Car temp = cars[i];
                    cars[i] = cars[i + 1];
                    cars[i + 1] = temp;
                    swapped = true;
                }
            }
        } while (swapped);
    }

    public static void insertionSort(Car[] cars, Comparator<Car> comparator) {
        for (int i = 1; i < cars.length; i++) {
            Car current = cars[i];
            int j = i - 1;
            while (j >= 0 && comparator.compare(cars[j], current) > 0) {
                cars[j + 1] = cars[j];
                j--;
            }
            cars[j + 1] = current;
        }
    }

    public static void selectionSort(Car[] cars, Comparator<Car> comparator) {
        for (int i = 0; i < cars.length - 1; i++) {
            int minIndex = i;
            for (int j = i + 1; j < cars.length; j++) {
                if (comparator.compare(cars[j], cars[minIndex]) < 0) {
                    minIndex = j;
                }
            }
            Car temp = cars[i];
            cars[i] = cars[minIndex];
            cars[minIndex] = temp;
        }
    }
}

/*
 * Bubble Sort:
 * 
 * Time complexity: O(n^2) in the worst and average cases, O(n) in the best case
 * (when the input array is already sorted)
 * 
 * Space complexity: O(1)
 * 
 * Basic idea: Iterate through the array repeatedly, comparing adjacent pairs of
 * elements and swapping them if they are in the wrong order. Repeat until the
 * array is fully sorted.
 * 
 * 
 * Selection Sort:
 * 
 * Time complexity: O(n^2) in all cases (worst, average, and best)
 * 
 * Space complexity: O(1)
 * 
 * Basic idea: Find the minimum element in the unsorted portion of the array and
 * swap it with the first unsorted element. Repeat until the array is fully
 * sorted.
 * 
 * 
 * Insertion Sort:
 * 
 * Time complexity: O(n^2) in the worst and average cases, O(n) in the best case
 * (when the input array is already sorted)
 * 
 * Space complexity: O(1)
 * 
 * Basic idea: Build up a sorted subarray from left to right by inserting each
 * new element into its correct position in the subarray. Repeat until the array
 * is fully sorted.
 */