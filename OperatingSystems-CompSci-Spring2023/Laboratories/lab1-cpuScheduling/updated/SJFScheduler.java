package updated;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.PriorityQueue;

public class SJFScheduler {
    private List<ProcessSJF> processes;
    private PriorityQueue<ProcessSJF> readyQueue;
    private int currentTime;
    private boolean isPreemptive;

    public SJFScheduler(List<ProcessSJF> processes, boolean isPreemptive) {
        this.processes = new ArrayList<>(processes);
        this.readyQueue = new PriorityQueue<>(Comparator.comparing(ProcessSJF::getBurstTime));
        this.currentTime = 0;
        this.isPreemptive = isPreemptive;
    }

    public void run() {
        int totalProcesses = processes.size();
        int completedProcesses = 0;
        int totalCompletionTime = 0;
        int totalWaitingTime = 0;
        int totalTurnaroundTime = 0;
    
        while (completedProcesses < totalProcesses) {
            // Add arrived processes to the ready queue
            for (ProcessSJF process : processes) {
                if (process.getArrivalTime() <= currentTime && !process.isCompleted()) {
                    readyQueue.add(process);
                }
            }
    
            if (readyQueue.isEmpty()) {
                // No processes in the ready queue, so we need to wait for the next process to
                // arrive
                currentTime++;
                continue;
            }
    
            // Get the next process to run
            ProcessSJF nextProcess = readyQueue.poll();
    
            if (!isPreemptive) {
                // Run the process to completion
                int completionTime = currentTime + nextProcess.getBurstTime();
                nextProcess.setCompletionTime(completionTime);
                nextProcess.setTurnaroundTime(completionTime - nextProcess.getArrivalTime());
                nextProcess.setWaitingTime(nextProcess.getTurnaroundTime() - nextProcess.getBurstTime());
                currentTime = completionTime;
                nextProcess.setCompleted(true);
                completedProcesses++;
                totalWaitingTime += nextProcess.getWaitingTime();
                totalTurnaroundTime += nextProcess.getTurnaroundTime();
            } else {
                // Run the process for the current time slice
                int timeSlice = 1;
                if (!nextProcess.isCompleted()) {
                    nextProcess.setRemainingTime(nextProcess.getRemainingTime() - timeSlice);
                    currentTime += timeSlice;
    
                    // Check if the process is completed
                    if (nextProcess.getRemainingTime() == 0) {
                        nextProcess.setCompletionTime(currentTime);
                        nextProcess.setTurnaroundTime(currentTime - nextProcess.getArrivalTime());
                        nextProcess.setWaitingTime(nextProcess.getTurnaroundTime() - nextProcess.getBurstTime());
                        nextProcess.setCompleted(true);
                        completedProcesses++;
                        totalWaitingTime += nextProcess.getWaitingTime();
                        totalTurnaroundTime += nextProcess.getTurnaroundTime();
                    } else {
                        // Add the process back to the ready queue
                        readyQueue.add(nextProcess);
                    }
                }
                else {
                    continue;
                }
            }
        }
    
        for(ProcessSJF process : processes){
            process.print();
        }
    
        for(ProcessSJF process : processes){
            totalCompletionTime += process.getCompletionTime();
        }
    
        double avgCompletionTime = totalCompletionTime / totalProcesses;
        double avgWaitingTime = totalWaitingTime / totalProcesses;
        double avgTurnaroundTime = totalTurnaroundTime / totalProcesses;
    
        System.out.println("Average completion time: " + avgCompletionTime);
        System.out.println("Average waiting time: " + avgWaitingTime);
        System.out.println("Average turnaround time: " + avgTurnaroundTime);
    }
}
