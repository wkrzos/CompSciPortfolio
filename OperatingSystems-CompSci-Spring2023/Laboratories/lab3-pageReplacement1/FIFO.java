import java.util.ArrayList;
import java.util.List;

public class FIFO {
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
                int max = time - pages.get(frames[0]).getArriveTime();
                int toDelete = 0;
                for (int i = 0; i < numberOfFrames; i++) {
                    if (time - pages.get(frames[i]).getArriveTime() > max) {
                        max = time - pages.get(frames[i]).getArriveTime();
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

