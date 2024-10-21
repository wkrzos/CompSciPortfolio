import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

public class ALRU {
    public int run(int numberOfPages, int numberOfFrames, List<Integer> requests) {
        int errors = 0;
        int time = 0;

        List<Page> pages = new ArrayList<>();
        int[] frames = new int[numberOfFrames];
        for (int i = 0; i < numberOfFrames; i++) {
            frames[i] = -1;
        }

        Queue<Page> queue = new LinkedList<>();

        for (int i = 0; i < numberOfPages; i++) {
            pages.add(new Page(i));
        }

        for (int req : requests) {
            boolean done = false;
            for (int i = 0; i < numberOfFrames; i++) {
                if (frames[i] == req) {
                    done = true;
                    pages.get(req).setBit(1);
                    break;
                }
            }

            if (!done) {
                for (int i = 0; i < numberOfFrames; i++) {
                    if (frames[i] == -1) {
                        frames[i] = req;
                        pages.get(req).setBit(1);
                        queue.add(pages.get(req));
                        errors++;
                        done = true;
                        break;
                    }
                }
            }

            if (!done) {
                Page first = queue.poll();
                if (first.getBit() == 0) {
                    for (int i = 0; i < numberOfFrames; i++) {
                        if (frames[i] == first.getId()) {
                            frames[i] = req;
                            pages.get(req).setBit(1);
                            queue.add(pages.get(req));
                            break;
                        }
                    }
                } else {
                    while (true) {
                        Page toDelete = first;
                        if (toDelete.getBit() == 0) {
                            break;
                        } else {
                            toDelete.setBit(0);
                            queue.add(toDelete);
                            first = queue.poll();
                        }
                    }
                    for (int i = 0; i < numberOfFrames; i++) {
                        if (frames[i] == first.getId()) {
                            frames[i] = req;
                            pages.get(req).setBit(1);
                            queue.add(pages.get(req));
                            break;
                        }
                    }
                }
                errors++;
            }
            time++;
        }
        return errors;
    }
}

