package util;

public class EDF {
    public static int sortEDF(int[] queue, int head, int[] deadlines) {
        int seekCount = 0;
        int curTrack = head;
        int index = -1;
        
        // find index of head in queue
        for (int i = 0; i < queue.length; i++) {
            if (queue[i] == head) {
                index = i;
                break;
            }
        }
        
        // sort queue by deadline
        for (int i = 0; i < queue.length - 1; i++) {
            for (int j = i + 1; j < queue.length; j++) {
                if (deadlines[i] > deadlines[j]) {
                    int temp = queue[i];
                    queue[i] = queue[j];
                    queue[j] = temp;
                    
                    temp = deadlines[i];
                    deadlines[i] = deadlines[j];
                    deadlines[j] = temp;
                }
            }
        }
        
        // visit tracks in the queue in deadline order
        for (int i = 0; i < queue.length; i++) {
            seekCount += Math.abs(curTrack - queue[i]);
            curTrack = queue[i];
        }
        
        return seekCount;
    }
    
}
