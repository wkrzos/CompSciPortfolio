package test.Original;

//WORKS!

public class InsertSortLecture {

    public static void main(String[] args) {
        //int[] arr = {3,1,0,2,1}; //expected 8 6
        int[] arr = {1,9,4,7,3}; //expected 9 6
        //int[] arr = {9,7,9,0,6}; //expected 10 7
        sort(arr);
    }

    public static int[] sort(int[] arr) {
        int comparisons = 0;
        int swap = 0;
        
        for (int i = 1; i < arr.length; ++i) {
            int value = arr[i];
            int j;

            comparisons++;

            for (j = i; j > 0 && value < arr[j - 1]; --j) {
                arr[j] = arr[j - 1];
                swap++;
                comparisons++;
            }

            if(j == 0) comparisons -= 1;
            
            arr[j] = value;
            
            System.out.println();
            System.out.println("Iteration (i) = " + i + ", j = " + j);
            System.out.println("comparisons = " + comparisons);
            System.out.println("swaps = " + swap);
            System.out.print("arr = ");
            for (int k = 0; k < arr.length; k++) {
                System.out.print(arr[k] + " ");
            }
            System.out.println();
        }

        System.out.println("\nNumber of comparisons: " + comparisons);
        System.out.println("Number of swaps: " + swap);
        
        return arr;
    }
}
