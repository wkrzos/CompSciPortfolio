package util;

import java.util.Random;

public class RandomProcessGenerator {
    
    private static int MAX_PROCESSES;
    private static int MAX_VALUE;

    public RandomProcessGenerator(int mAX_PROCESSES) {
        MAX_PROCESSES = mAX_PROCESSES;
    }

    public void generateRandomProcessQueue(int numberOfProcesses, int lowerRange, int upperRange){
        MAX_PROCESSES = numberOfProcesses;

        
    }

    

    public static int[] generate(int numberOfProcesses, int maxProcessRequest) {
        
        MAX_PROCESSES = numberOfProcesses;
        MAX_VALUE = maxProcessRequest;

        int[] array = new int[MAX_PROCESSES];
        Random random = new Random();

        for (int i = 0; i < MAX_PROCESSES; i++) {
            array[i] = random.nextInt(MAX_VALUE + 1);
        }

        return array;
    }
    public static int[] generateRandomDeadlines(int[] queue, int maxDeadline) {
        int[] deadlines = new int[queue.length];
        Random rand = new Random();
        for (int i = 0; i < queue.length; i++) {
            deadlines[i] = rand.nextInt(maxDeadline) + 1; // add 1 to avoid 0 deadlines
        }
        return deadlines;
    }
}
