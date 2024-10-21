public class ProcessWSJF extends ProcessSJFOld {

    int weight;

    public ProcessWSJF(int processID, int arrivalTime, int burstTime, int completionTime, int turnAroundTime,
            int waitingTime, int weight) {
        super(processID, arrivalTime, burstTime, completionTime, turnAroundTime, waitingTime);
        this.weight = weight;
    }

    public void printState(){  
        System.out.format("%5s%5s%5s%5s%5s%5s%5s", "\n" + processID, arrivalTime, burstTime, completionTime, turnAroundTime, waitingTime, weight);
    }

    public int getWeight() {
        return weight;
    }

    public void setWeight(int weight) {
        this.weight = weight;
    }
}
