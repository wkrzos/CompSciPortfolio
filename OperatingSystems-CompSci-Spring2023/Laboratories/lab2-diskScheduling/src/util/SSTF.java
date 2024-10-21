package util;

import java.util.ArrayList;
import java.util.List;

public class SSTF {
    public static int sortSSTF(int[] queue, int head) {
        int seekCount = 0;
        int curTrack = head;
        List<Integer> remainingTracks = new ArrayList<>();

        for (int i = 0; i < queue.length; i++) {
            remainingTracks.add(queue[i]);
        }

        while (!remainingTracks.isEmpty()) {
            int shortestDist = Integer.MAX_VALUE;
            int shortestIndex = -1;

            for (int i = 0; i < remainingTracks.size(); i++) {
                int distance = Math.abs(curTrack - remainingTracks.get(i));
                if (distance < shortestDist) {
                    shortestDist = distance;
                    shortestIndex = i;
                }
            }

            seekCount += shortestDist;
            curTrack = remainingTracks.get(shortestIndex);
            remainingTracks.remove(shortestIndex);
        }

        return seekCount;
    }
}