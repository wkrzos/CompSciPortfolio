import java.util.ArrayList;
import java.util.List;

public class LRU {
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
                    pages.get(req).setLastUsed(time);
                    done = true;
                    break;
                }
            }

            if (!done) {
                for (int i = 0; i < numberOfFrames; i++) {
                    if (frames[i] == -1) {
                        frames[i] = req;
                        pages.get(req).setArriveTime(time);
                        pages.get(req).setLastUsed(time);
                        errors++;
                        done = true;
                        break;
                    }
                }
            }

            if (!done) {
                int max = 0;
                int toDelete = -1;
                for (int i = 0; i < numberOfFrames; i++) {
                    if (time - pages.get(frames[i]).getLastUsed() > max) {
                        toDelete = i;
                        max = time - pages.get(frames[i]).getLastUsed();
                    }
                }
                frames[toDelete] = req;
                pages.get(req).setArriveTime(time);
                pages.get(req).setLastUsed(time);
                errors++;
            }
            time++;
        }
        return errors;
    }
}

