import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class RandomReplacement {
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

        Random random = new Random();

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
                        errors++;
                        done = true;
                        break;
                    }
                }
            }

            if (!done) {
                int toDelete = random.nextInt(numberOfFrames);
                frames[toDelete] = req;
                errors++;
            }
            time++;
        }
        return errors;
    }
}