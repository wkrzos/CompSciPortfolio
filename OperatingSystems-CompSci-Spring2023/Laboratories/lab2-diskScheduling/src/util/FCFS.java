package util;

public class FCFS{
    public static int sortFCFS(int[] queue, int head) {
        int seekCount = 0;
        int curTrack = head;
        
        for (int i = 0; i < queue.length; i++) {
            seekCount += Math.abs(queue[i] - curTrack);
            curTrack = queue[i];
        }
        
        return seekCount;
    }
    
}
