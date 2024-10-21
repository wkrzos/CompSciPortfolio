package main;

import java.util.Random;

public class DataSetGenerator {

    public static int[] generateRandomArray(){
        int[] arr = new int[Main.getARR_SIZE()];

        Random random = new Random();

        for(int i = 0; i < arr.length; i++){
            arr[i] = random.nextInt(Main.getMAX_INT_VALUE());
        }

        return arr;
    }

    public static int[] returnReverseArray(int[] arrToReverse){
        int[] reversedArr = new int[arrToReverse.length];

        for(int i = 0; i < reversedArr.length; i++){
            reversedArr[i] = arrToReverse[reversedArr.length - i - 1]; //out of bound
        }

        return reversedArr;
    }
}

/* Testowanie wykonać na zbiorach danych: - losowym, - uporządkowanym odwrotnie do porządku sortowania, - uporządkowanym zgodnie z porządkiem sortowania,
a także dla różnych wielkości zbiorów, np:
- 8, 32, 128, 512, 2048 elementów. */

