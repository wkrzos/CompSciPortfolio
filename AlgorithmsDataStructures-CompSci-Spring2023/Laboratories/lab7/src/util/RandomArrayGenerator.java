package util;

import java.util.Random;

public class RandomArrayGenerator {
    
    private int ARR_SIZE;
    private int VALUE_RANGE;

    public RandomArrayGenerator(int size, int range){
        ARR_SIZE = size;
        VALUE_RANGE = range;
    }

    public PriorityHeap generateRandomArray(){
        PriorityHeap ph = new PriorityHeap(ARR_SIZE);

        Random rn = new Random();

        for(int i = 0; i < ARR_SIZE; i++){
            ph.enqueue(rn.nextInt(VALUE_RANGE));
        }

        return ph;
    }
}
