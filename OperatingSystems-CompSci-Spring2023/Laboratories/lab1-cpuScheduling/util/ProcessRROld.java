public class ProcessRROld extends ProcessSJFOld {

    int burstTimeCountdown;
    boolean isFinished = false;

    public ProcessRROld(int processID, int arrivalTime, int burstTime, int completionTime, int turnAroundTime,
            int waitingTime, int burstTimeCountdown, boolean isFinished) {
        super(processID, arrivalTime, burstTime, completionTime, turnAroundTime, waitingTime);
        this.burstTimeCountdown = burstTimeCountdown;
        this.isFinished = isFinished;
    }

    public int getBurstTimeCountdown() {
        return burstTimeCountdown;
    }

    public void setBurstTimeCountdown(int burstTimeCountdown) {
        this.burstTimeCountdown = burstTimeCountdown;
    }

    public boolean isFinished() {
        return isFinished;
    }

    public void setFinished(boolean isFinished) {
        this.isFinished = isFinished;
    }
}
