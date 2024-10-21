package util;

public class QuickSorter {

    public static int quickSorterComparisonCount = 0;
    public static int quickSorterSwapCount = 0;

    public static void sort(int[] arr) {
        quickSort(arr, 0, arr.length - 1);
    }
    
    private static void quickSort(int[] arr, int left, int right) {
        if (left < right) {
            int pivotIndex = partition(arr, left, right);
            quickSort(arr, left, pivotIndex - 1);
            quickSort(arr, pivotIndex + 1, right);
        }
    }
    
    private static int partition(int[] arr, int left, int right) {
        int pivot = arr[right];
        int i = left - 1;
        for (int j = left; j < right; j++) {
            quickSorterComparisonCount++;
            if (arr[j] < pivot) {
                i++;
                swap(arr, i, j);
                quickSorterSwapCount++;
            }
        }
        swap(arr, i + 1, right);
        quickSorterSwapCount++;
        return i + 1;
    }
    
    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}