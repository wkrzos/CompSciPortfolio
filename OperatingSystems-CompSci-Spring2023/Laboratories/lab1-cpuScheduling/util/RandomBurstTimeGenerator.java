
import java.util.ArrayList;
import java.util.concurrent.ThreadLocalRandom;

public class RandomBurstTimeGenerator {

    public RandomBurstTimeGenerator() {

    }

    public ArrayList<ProcessSJFOld> fillProcessList() {
        int NUMBER_OF_PROCESSES = 20;
        ArrayList<ProcessSJFOld> outputList = new ArrayList<>();

        for (int i = 0; i < NUMBER_OF_PROCESSES; i++) {
            outputList.add(new ProcessSJFOld(0, 0, randomBurstTimeGenerator(), 0, 0, 0));
        }

        return outputList;
    }

    public int randomBurstTimeGenerator() {

        int randomNum = ThreadLocalRandom.current().nextInt(0, 150 + 1);

        return randomNum;
    }
}
