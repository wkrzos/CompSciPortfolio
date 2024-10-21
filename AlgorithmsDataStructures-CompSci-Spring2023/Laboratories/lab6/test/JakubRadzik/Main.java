package test.JakubRadzik;

import java.util.Random;

public class Main {

    // @author Jakub Radzik https://github.com/Jakub-Radzik

    private static final int size = 128;

    public static void main(String[] args) {

/*         Random rand = new Random();
        int[] arr = new int[size];
        for (int i = 0; i < size; i++) {
            int n = rand.nextInt(5000);
            arr[i] = n;
        } */

        int[] arr = {9,7,9,0,6};
        // int[] arr = {7,6,5,4,3,2,1,0};

        int[] testArr;



        System.out.println("TABLICA TESTOWA:");
        for (int i = 0; i < arr.length; i++) {
            System.out.print(arr[i] + ", ");
        }

        System.out.println();
        System.out.println("TABLICA PO SORTOWANIU");

        testArr = arr.clone();
        SortMethods.BubbleSort(testArr);
        System.out.println("BUBBLE SORT: [PORÓWNANIA - PRZEPISANIA] - [" + SortMethods.getComparisions() + "-"
                + SortMethods.getRewrites() + "]");
        SortMethods.setComparisions(0);
        SortMethods.setRewrites(0);

        testArr = arr.clone();
        SortMethods.InsertionSort(testArr);
        System.out.println("INSERTION SORT: [PORÓWNANIA - PRZEPISANIA] - [" + SortMethods.getComparisions() + "-"
                + SortMethods.getRewrites() + "]");
        SortMethods.setComparisions(0);
        SortMethods.setRewrites(0);

        testArr = arr.clone();
        SortMethods.SelectionSort(testArr);
        System.out.println("SELECTION SORT: [PORÓWNANIA - PRZEPISANIA] - [" + SortMethods.getComparisions() + "-"
                + SortMethods.getRewrites() + "]");
        SortMethods.setComparisions(0);
        SortMethods.setRewrites(0);

        SortMethods.SelectionSort(arr);
        for (int i = 0; i < arr.length; i++) {
            System.out.print(testArr[i] + ", ");
        }

    }
}
