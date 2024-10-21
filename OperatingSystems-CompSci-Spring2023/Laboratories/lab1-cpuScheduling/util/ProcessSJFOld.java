public class ProcessSJFOld {
    
    int processID; //number unique to a process
    int arrivalTime; //when a process is ready to be executed
    int burstTime; //time recquired for execution
    int completionTime; //time when process stops executing
    int turnAroundTime; //completion time - arrival time
    int waitingTime; //Turnaround time - burst time

    public ProcessSJFOld(int processID, int arrivalTime, int burstTime, int completionTime, int turnAroundTime,
            int waitingTime) {
        this.processID = processID;
        this.arrivalTime = arrivalTime;
        this.burstTime = burstTime;
        this.completionTime = completionTime;
        this.turnAroundTime = turnAroundTime;
        this.waitingTime = waitingTime;
    }

    public void printState(){  
        System.out.format("%20s%20s%20s%20s%20s%20s", "\n" + processID, arrivalTime, burstTime, completionTime, turnAroundTime, waitingTime);
    }

    public int getProcessID() {
        return processID;
    }

    public void setProcessID(int processID) {
        this.processID = processID;
    }

    public int getArrivalTime() {
        return arrivalTime;
    }

    public void setArrivalTime(int arrivalTime) {
        this.arrivalTime = arrivalTime;
    }

    public int getBurstTime() {
        return burstTime;
    }

    public void setBurstTime(int burstTime) {
        this.burstTime = burstTime;
    }

    public int getCompletionTime() {
        return completionTime;
    }

    public void setCompletionTime(int completionTime) {
        this.completionTime = completionTime;
    }

    public int getTurnAroundTime() {
        return turnAroundTime;
    }

    public void setTurnAroundTime(int turnAroundTime) {
        this.turnAroundTime = turnAroundTime;
    }

    public int getWaitingTime() {
        return waitingTime;
    }

    public void setWaitingTime(int waitingTime) {
        this.waitingTime = waitingTime;
    } 
}
