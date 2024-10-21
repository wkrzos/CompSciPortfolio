package main;

import java.util.Arrays;

import util.InsertSorter;
import util.MergeSorter;
import util.QuickSorter;
import util.SelectSorter;
import util.SelectSorterOptimised;

public class Main {

    private static int ARR_SIZE = 2048;
    private static int MAX_INT_VALUE = 100; // given value - 1

    private static int[] arr, arr1, arr2, arr3, arr4, arr5, arrAscendingOrder;

    public static void main(String[] args) {
        generateArrays();
        sortArrays();
        displayData();
        displayDataTable();
        displayDataGraph();
    }

    private static void generateArrays() {
        arr = DataSetGenerator.generateRandomArray();

        arr1 = arr.clone();
        arr2 = arr.clone();
        arr3 = arr.clone();
        arr4 = arr.clone();
        arr5 = arr.clone();

        
/*          arrAscendingOrder = arr.clone();
         InsertSorter.sort(arrAscendingOrder);
          
         arr1 = arrAscendingOrder.clone();
         arr2 = arrAscendingOrder.clone();
         arr3 = arrAscendingOrder.clone();
         arr4 = arrAscendingOrder.clone();
         arr5 = arrAscendingOrder.clone();
          
         arr1 = DataSetGenerator.returnReverseArray(arrAscendingOrder.clone());
         arr2 = DataSetGenerator.returnReverseArray(arrAscendingOrder.clone());
         arr3 = DataSetGenerator.returnReverseArray(arrAscendingOrder.clone());
         arr4 = DataSetGenerator.returnReverseArray(arrAscendingOrder.clone());
         arr5 = DataSetGenerator.returnReverseArray(arrAscendingOrder.clone()); */
         
    }

    private static void sortArrays() {
        InsertSorter.sort(arr1);
        MergeSorter.sort(arr2);
        QuickSorter.sort(arr3);
        SelectSorter.sort(arr4);
        SelectSorterOptimised.sort(arr5);
    }

    private static void displayData() {
        System.out.println("========= NEW RUN =========");
        System.out.println("Array size: " + ARR_SIZE);
        System.out.println("Max int value: " + MAX_INT_VALUE);
        System.out.println();
    }

    private static void displayDataTable() {
        System.out.printf("%-25s%-25s%-25s\n", "", "Comparison count", "Swap count");
        System.out.printf("%-25s%-25d%-25d\n", "InsertSorter", InsertSorter.insertSorterComparisonCount,
                InsertSorter.insertSorterSwapCount);
        System.out.printf("%-25s%-25d%-25d\n", "MergeSorter", MergeSorter.mergeSorterComparisonCount,
                MergeSorter.mergeSorterSwapCount);
        System.out.printf("%-25s%-25d%-25d\n", "QuickSorter", QuickSorter.quickSorterComparisonCount,
                QuickSorter.quickSorterSwapCount);
        System.out.printf("%-25s%-25d%-25d\n", "SelectSorter", SelectSorter.selectSorterComparisonCount,
                SelectSorter.selectSorterSwapCount);
        System.out.printf("%-25s%-25d%-25d\n", "SelectSorterOptimised",
                SelectSorterOptimised.selectSorterOptimisedComparisonCount,
                SelectSorterOptimised.selectSorterOptimisedSwapCount);
    }

    private static void displayDataGraph() {
        String[] sorterNames = { "Insertion", "Merge", "Quick", "Select", "Select (Opt)" };
        int[] comparisonCounts = { InsertSorter.insertSorterComparisonCount, MergeSorter.mergeSorterComparisonCount,
                QuickSorter.quickSorterComparisonCount, SelectSorter.selectSorterComparisonCount,
                SelectSorterOptimised.selectSorterOptimisedComparisonCount };
        int[] swapCounts = { InsertSorter.insertSorterSwapCount, MergeSorter.mergeSorterSwapCount,
                QuickSorter.quickSorterSwapCount, SelectSorter.selectSorterSwapCount,
                SelectSorterOptimised.selectSorterOptimisedSwapCount };

        System.out.println("\nComparison Counts:");
        printBarChart(sorterNames, comparisonCounts);
        System.out.println("\nSwap Counts:");
        printBarChart(sorterNames, swapCounts);
    }

    private static void printBarChart(String[] labels, int[] values) {
        int maxVal = Arrays.stream(values).max().getAsInt();
        int chartWidth = 50;
        double valueRatio = (double) chartWidth / maxVal;

        for (int i = 0; i < labels.length; i++) {
            System.out.printf("%-15s ", labels[i]);
            int barLength = (int) (values[i] * valueRatio);
            for (int j = 0; j < barLength; j++) {
                System.out.print("=");
            }
            System.out.println(" " + values[i]);
        }
    }

    private static void printArray(int[] arr) {
        for (int i = 0; i < arr.length; i++) {
            System.out.print(arr[i] + " ");
        }
        System.out.println();
    }

    public static int getARR_SIZE() {
        return ARR_SIZE;
    }

    public static void setARR_SIZE(int aRR_SIZE) {
        ARR_SIZE = aRR_SIZE;
    }

    public static int getMAX_INT_VALUE() {
        return MAX_INT_VALUE;
    }

    public static void setMAX_INT_VALUE(int mAX_INT_VALUE) {
        MAX_INT_VALUE = mAX_INT_VALUE;
    }
}