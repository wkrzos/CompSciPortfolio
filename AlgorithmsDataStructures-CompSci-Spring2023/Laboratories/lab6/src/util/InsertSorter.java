package util;

public class InsertSorter {

    public static int insertSorterComparisonCount = 0;
    public static int insertSorterSwapCount = 0;

    public static void sort(int[] arr) {
        for (int i = 1; i < arr.length; i++) {
            int j = i;
            while (j > 0 && arr[j] < arr[j - 1]) {
                swap(arr, j, j - 1);
                insertSorterSwapCount++;
                insertSorterComparisonCount++; // increment the comparison count

                j--;
                if(j == 0) insertSorterSwapCount--;
            }

        }
    }
    
    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}

