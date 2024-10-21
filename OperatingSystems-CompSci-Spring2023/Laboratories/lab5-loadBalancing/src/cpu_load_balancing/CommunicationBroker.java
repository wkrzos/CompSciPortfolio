package cpu_load_balancing;

import java.util.Collections;
import java.util.Random;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class CommunicationBroker {
    private CPU[] cpus;
    private static Random random = new Random();
    private int queryCounter = 0;

    private int moveCounter = 0;

    public CommunicationBroker(CPU[] cpus) {
        this.cpus = cpus;
    }

    public int[] generateRandomCpuSequence(CPU queryingCPU, int length) {
        int[] sequence = new int[length];

        var result = IntStream.range(0, cpus.length).filter(cpuIdx -> queryingCPU != cpus[cpuIdx]).boxed().collect(Collectors.toList());
        Collections.shuffle(result);
        for(int i = 0 ; i < length; i++) {
            sequence[i] = result.get(i);
        }
        return sequence;
    }

    public double queryCpuLoad(int idx) {
        queryCounter++;
        return cpus[idx].getLoad();
    }



    public void moveTask(CPU moveFrom, int destIdx, Task taskToMove) {
        moveCounter++;
        cpus[destIdx].moveTask(moveFrom, taskToMove);
    }

    public CPU getCPU(int idx) {
        return cpus[idx];
    }
    public int getCPUIdx(CPU cpu) {
        for(int i = 0 ; i < cpus.length; i++) {
            if(cpu == cpus[i]) {
                return i;
            }
        }
        return -1;
    }

    // algorytm 3
    public void notifyCPUs() {
        for(CPU cpu: cpus) {
            cpu.onNotified();
        }
    }


    public int getQueryCounter() {
        return queryCounter;
    }
    public int getMoveCounter() {
        return moveCounter;
    }

    public int getCpuCount() {
        return cpus.length;
    }


}
