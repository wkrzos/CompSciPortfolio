package util;

import java.util.Arrays;

public class CSCAN {
    public static int sortCSCAN(int[] queue, int head, int direction) {
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
        
        // sort queue in increasing order of track number
        Arrays.sort(queue);
        
        if (direction == 0) { // scan towards 0
            // move head to the beginning of the queue
            seekCount += head;
            curTrack = 0;
            
            // visit tracks in the queue up to the end of the disk
            for (int i = index + 1; i < queue.length; i++) {
                seekCount += queue[i] - curTrack;
                curTrack = queue[i];
            }
            
            // visit tracks at the beginning of the disk
            seekCount += 99 - curTrack;
            curTrack = 99;
            
            // visit tracks in the queue before head
            for (int i = 0; i < index; i++) {
                seekCount += curTrack - queue[i];
                curTrack = queue[i];
            }
        } else { // scan towards end of disk
            // move head to the end of the queue
            seekCount += 99 - head;
            curTrack = 99;
            
            // visit tracks in the queue before head
            for (int i = index - 1; i >= 0; i--) {
                seekCount += curTrack - queue[i];
                curTrack = queue[i];
            }
            
            // visit tracks at the beginning of the disk
            seekCount += curTrack;
            curTrack = 0;
            
            // visit tracks in the queue up to the end of the disk
            for (int i = queue.length - 1; i > index; i--) {
                seekCount += curTrack - queue[i];
                curTrack = queue[i];
            }
        }
        
        return seekCount;
    }
}
