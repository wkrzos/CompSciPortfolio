package util;

public class SelectSorterOptimised {

    public static int selectSorterOptimisedComparisonCount = 0;
    public static int selectSorterOptimisedSwapCount = 0;

    public static void sort(int[] arr) {
        for (int i = 0; i < arr.length - 1; i++) {
            int minIndex = i;
            for (int j = i + 1; j < arr.length; j++) {
                selectSorterOptimisedComparisonCount++;
                if (arr[j] < arr[minIndex]) {
                    minIndex = j;
                }
            }
            if (minIndex != i) { // check if a swap is needed
                swap(arr, i, minIndex);
                selectSorterOptimisedSwapCount++; // increment swap count
            }
        }
    }

    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
