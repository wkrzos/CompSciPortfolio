package util;

import java.util.Arrays;

public class FDSCAN {
    public static int sortFDSCAN(int[] queue, int head, int[] deadlines, int direction) {
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

        int nextTrackIndex = (direction == 0) ? index - 1 : index + 1;

        while (nextTrackIndex >= 0 && nextTrackIndex < queue.length) {
            int nextTrack = queue[nextTrackIndex];

            // calculate seek time to next track
            seekCount += Math.abs(curTrack - nextTrack);

            // update current track
            curTrack = nextTrack;

            // check if deadline has been missed
            if (seekCount > deadlines[nextTrackIndex]) {
                // find the next track with the earliest deadline
                int earliestDeadline = Integer.MAX_VALUE;
                int earliestDeadlineIndex = -1;

                for (int i = 0; i < queue.length; i++) {
                    if (i != nextTrackIndex && deadlines[i] < earliestDeadline && seekCount + Math.abs(curTrack - queue[i]) <= deadlines[i]) {
                        earliestDeadline = deadlines[i];
                        earliestDeadlineIndex = i;
                    }
                }

                // move to next track with earliest deadline
                if (earliestDeadlineIndex != -1) {
                    nextTrackIndex = earliestDeadlineIndex;
                }
            } else {
                // move to next track in same direction
                nextTrackIndex += (direction == 0) ? -1 : 1;
            }
        }

        return seekCount;
    }
}