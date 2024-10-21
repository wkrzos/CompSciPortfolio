package test.JakubRadzik;

public class SortMethods {

    private static int comparisions = 0;
    private static int rewrites = 0;

    public static int getComparisions() {
        return comparisions;
    }

    public static int getRewrites() {
        return rewrites;
    }


    public static void setComparisions(int comparisions) {
        SortMethods.comparisions = comparisions;
    }

    public static void setRewrites(int rewrites) {
        SortMethods.rewrites = rewrites;
    }


    public static void SelectionSort(int[] arr){
        int n = arr.length;
        for (int i = 0; i < n-1; i++) {
            int min_idx = i;
            for (int j = i + 1; j < n; j++){
                comparisions++;
                if (arr[j] < arr[min_idx])
                    min_idx = j;
                    rewrites++;
            }
            rewrites+=3;
            int temp = arr[min_idx];
            arr[min_idx] = arr[i];
            arr[i] = temp;
        }
    }

    public static void InsertionSort(int[] arr){
        int n = arr.length;
        for (int i = 1; i < n; ++i) {
            rewrites++;
            int key = arr[i];
            int j = i - 1;
            while (j >= 0 && arr[j] > key) {
                rewrites++;
                comparisions++;
                arr[j + 1] = arr[j];
                j = j - 1;
            }

            if(j>=0){
                comparisions++;
            }

            rewrites++;
            arr[j + 1] = key;
        }
    }

    public static void BubbleSort(int[] arr){
        int n = arr.length;
        for (int i = 0; i < n-1; i++)
            for (int j = 0; j < n-i-1; j++){
                comparisions++;
                if (arr[j] > arr[j+1]) {
                    rewrites+=3;
                    int temp = arr[j];
                    arr[j] = arr[j+1];
                    arr[j+1] = temp;
                }}
    }

}