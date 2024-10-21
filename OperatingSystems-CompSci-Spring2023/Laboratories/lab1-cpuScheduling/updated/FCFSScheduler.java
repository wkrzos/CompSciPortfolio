package updated;

import java.util.ArrayList;
import java.util.Collections;

public class FCFSScheduler {

    public void run(ArrayList<ProcessFCFS> processes, int cpuTime) {

        // Sort the processes by their arrival times
        Collections.sort(processes, (p1, p2) -> Integer.compare(p1.getArrivalTime(), p2.getArrivalTime()));

        // Process each job in order
        for (ProcessFCFS p : processes) {
            // Set waiting time
            p.setWaitingTime(cpuTime - p.getArrivalTime());

            // Set completion time and CPU time
            p.setCompletionTime(cpuTime + p.getBurstTime());
            cpuTime = p.getCompletionTime();

            // Set turnaround time
            p.setTurnaroundTime(p.getCompletionTime() - p.getArrivalTime());
        }

        // Calculate average waiting time and average turnaround time
        int totalCompletionTime = 0;
        int totalWaitingTime = 0;
        int totalTurnaroundTime = 0;
        for (ProcessFCFS p : processes) {
            totalCompletionTime += p.getCompletionTime();
            totalWaitingTime += p.getWaitingTime();
            totalTurnaroundTime += p.getTurnaroundTime();
        }

        double avgCompletionTime = totalCompletionTime / processes.size();
        double avgWaitingTime = totalWaitingTime / processes.size();
        double avgTurnaroundTime = totalTurnaroundTime / processes.size();

        printProcesses(processes, cpuTime);

        System.out.println("Average completion time: " + avgCompletionTime);
        System.out.println("Average waiting time: " + avgWaitingTime);
        System.out.println("Average turnaround time: " + avgTurnaroundTime);
    }

    public void printProcesses(ArrayList<ProcessFCFS> processes, int cpuTime) {
        // Print the header for the process table
        System.out.println("Process\tArrival Time\tBurst Time\tCompletion Time\tWaiting Time\tTurnaround Time");

        // Process each job in order
        for (ProcessFCFS p : processes) {
            p.setWaitingTime(cpuTime - p.getArrivalTime());

            p.setCompletionTime(cpuTime + p.getBurstTime());
            cpuTime = p.getCompletionTime();

            p.setTurnaroundTime(p.getCompletionTime() - p.getArrivalTime());

            System.out.println(p.getId() + "\t" + p.getArrivalTime() + "\t\t" + p.getBurstTime() + "\t\t"
                    + p.getCompletionTime() + "\t\t" + p.getWaitingTime() + "\t\t" + p.getTurnaroundTime());
        }

    }
}