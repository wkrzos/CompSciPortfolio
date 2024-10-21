import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class Generator {

    public static List<Integer> generate(int numberOfPages, int amount, int maxLocalSubsetSize, double localProb, int maxLocalAmount) {
        List<Integer> requests = new ArrayList<>();
        int counter = 0;
        Random random = new Random();

        while (counter != amount) {
            if (random.nextDouble() < localProb) {
                List<Integer> subset = new ArrayList<>();

                int localSubsetSize = Math.max(random.nextInt(maxLocalSubsetSize), 1);  // Ensure positive upper bound
                for (int i = 0; i < localSubsetSize; i++) {
                    subset.add(random.nextInt(numberOfPages));
                }
                int localAmount = Math.max(random.nextInt(maxLocalAmount), 1);  // Ensure positive upper bound
                for (int i = 0; i < localAmount; i++) {
                    if (counter >= amount) {
                        break;
                    }
                    counter++;
                    int toAdd = subset.get(random.nextInt(localSubsetSize));

                    requests.add(toAdd);
                }

            } else {
                int toAdd = random.nextInt(numberOfPages);
                requests.add(toAdd);
                counter++;
            }
        }

        return requests;
    }
}