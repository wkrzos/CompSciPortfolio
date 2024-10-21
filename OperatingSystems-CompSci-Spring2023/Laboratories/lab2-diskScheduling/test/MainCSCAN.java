package test;

import java.util.ArrayList;
import java.util.Collections;

public class MainCSCAN {

    public static void main(String[] args) {
        // Example input
        int headPosition = 50;
        int[] requests = {50, 50, 50};
        
        // Call the SCAN algorithm function
        ArrayList<Integer> sequence = scanAlgorithm(requests, headPosition);
        
        // Print out the resulting sequence
        for (int i : sequence) {
            System.out.print(i + " ");
        }
    }
    
    public static ArrayList<Integer> scanAlgorithm(int[] requests, int headPosition) {
        ArrayList<Integer> sequence = new ArrayList<Integer>();
        
        // Sort the requests in ascending order
        ArrayList<Integer> sortedRequests = new ArrayList<Integer>();
        for (int request : requests) {
            sortedRequests.add(request);
        }
        Collections.sort(sortedRequests);
        
        // Find the position of the head in the sorted requests
        int headIndex = sortedRequests.indexOf(headPosition);
        
        // Determine the direction of movement
        int direction = 1; // 1 for moving right, -1 for moving left
        if (headIndex > sortedRequests.size() / 2) {
            direction = -1;
        }
        
        // Add the head position to the sequence
        sequence.add(headPosition);
        
        // Traverse the disk in the direction of movement
        int currentIndex = headIndex;
        while (currentIndex >= 0 && currentIndex < sortedRequests.size()) {
            currentIndex += direction;
            if (currentIndex >= 0 && currentIndex < sortedRequests.size()) {
                sequence.add(sortedRequests.get(currentIndex));
            }
        }
        
        // If the direction was to the right, add the right end of the disk
        if (direction == 1) {
            sequence.add(requests.length - 1);
        }
        
        // If the direction was to the left, add the left end of the disk
        else {
            sequence.add(0);
        }
        
        return sequence;
    }
}
