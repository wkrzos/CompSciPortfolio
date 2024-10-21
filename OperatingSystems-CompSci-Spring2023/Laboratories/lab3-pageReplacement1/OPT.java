import java.util.ArrayList;
import java.util.List;

public class OPT {
    public int run(int numberOfPages, int numberOfFrames, List<Integer> requests) {
        int errors = 0;
        int time = 0;

        List<Page> pages = new ArrayList<>();
        int[] frames = new int[numberOfFrames];
        for (int i = 0; i < numberOfFrames; i++) {
            frames[i] = -1;
        }

        for (int i = 0; i < numberOfPages; i++) {
            pages.add(new Page(i));
        }

        for (int req : requests) {
            boolean done = false;
            for (int i = 0; i < numberOfFrames; i++) {
                if (frames[i] == req) {
                    done = true;
                    break;
                }
            }

            if (!done) {
                for (int i = 0; i < numberOfFrames; i++) {
                    if (frames[i] == -1) {
                        frames[i] = req;
                        pages.get(req).setArriveTime(time);
                        errors++;
                        done = true;
                        break;
                    }
                }
            }

            if (!done) {
                int toDelete = 0; // Initialize to a valid index
                int farthestUse = -1; // Tracks the farthest future use of a page
                for (int i = 0; i < numberOfFrames; i++) {
                    int currentFrame = frames[i];
                    int futureUse = Integer.MAX_VALUE;
                    for (int j = time + 1; j < requests.size(); j++) {
                        if (requests.get(j) == currentFrame) {
                            futureUse = j;
                            break;
                        }
                    }
                    if (futureUse > farthestUse) {
                        farthestUse = futureUse;
                        toDelete = i;
                    }
                }
                frames[toDelete] = req;
                pages.get(req).setArriveTime(time);
                errors++;
            }
            time++;
        }
        return errors;
    }
}
