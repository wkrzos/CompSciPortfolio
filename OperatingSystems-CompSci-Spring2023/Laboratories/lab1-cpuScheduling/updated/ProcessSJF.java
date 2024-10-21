package updated;

public class ProcessSJF {
    private final int pid;
    private final int arrivalTime;
    private final int burstTime;
    private int completionTime;
    private int turnaroundTime;
    private int waitingTime;
    private int remainingTime;
    private boolean completed;

    public ProcessSJF(int pid, int arrivalTime, int burstTime) {
        this.pid = pid;
        this.arrivalTime = arrivalTime;
        this.burstTime = burstTime;
        this.remainingTime = burstTime;
        this.completed = false;
    }

    public int getPid() {
        return pid;
    }

    public int getArrivalTime() {
        return arrivalTime;
    }

    public int getBurstTime() {
        return burstTime;
    }

    public int getCompletionTime() {
        return completionTime;
    }

    public void setCompletionTime(int completionTime) {
        this.completionTime = completionTime;
    }

    public int getTurnaroundTime() {
        return turnaroundTime;
    }

    public void setTurnaroundTime(int turnaroundTime) {
        this.turnaroundTime = turnaroundTime;
    }

    public int getWaitingTime() {
        return waitingTime;
    }

    public void setWaitingTime(int waitingTime) {
        this.waitingTime = waitingTime;
    }

    public int getRemainingTime() {
        return remainingTime;
    }

    public void setRemainingTime(int remainingTime) {
        this.remainingTime = remainingTime;
    }

    public boolean isCompleted() {
        return completed;
    }

    public void setCompleted(boolean completed) {
        this.completed = completed;
    }

    public void print() {
        System.out.println("\n" + pid + "\t" + arrivalTime + "\t" + burstTime + "\t" + completionTime + "\t" + turnaroundTime
        + "\t" + waitingTime + "\t" + remainingTime + "\t" + completed); 
    }
}