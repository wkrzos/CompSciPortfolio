package updated;

import java.util.ArrayList;

public class RRScheduler {
    private ArrayList<ProcessRR> processes;
    private int quantum;

    public RRScheduler(ArrayList<ProcessRR> processes, int quantum) {
        this.processes = processes;
        this.quantum = quantum;
    }

    public void run() {
        int time = 0;
        int n = processes.size();

        while (true) {
            boolean done = true;

            for (int i = 0; i < n; i++) {
                ProcessRR p = processes.get(i);

                if (p.getRemainingTime() > 0) {
                    done = false;

                    if (p.getRemainingTime() > quantum) {
                        time += quantum;
                        p.setRemainingTime(p.getRemainingTime() - quantum);
                    } else {
                        time += p.getRemainingTime();
                        p.setCompletionTime(time);
                        p.setTurnaroundTime(p.getCompletionTime() - p.getArrivalTime());
                        p.setWaitingTime(p.getTurnaroundTime() - p.getBurstTime());
                        p.setRemainingTime(0);
                    }
                }
            }

            if (done == true) {
                break;
            }
        }
    }

    public void printResults() {
        int totalCompletionTime = 0;
        int totalWaitingTime = 0;
        int totalTurnaroundTime = 0;

        System.out.println("Process\tBurst Time\tArrival Time\tWaiting Time\tTurnaround Time");

        for (int i = 0; i < processes.size(); i++) {
            ProcessRR p = processes.get(i);
            totalCompletionTime += p.getCompletionTime();
            totalWaitingTime += p.getWaitingTime();
            totalTurnaroundTime += p.getTurnaroundTime();
            System.out.println(p.getName() + "\t\t" + p.getBurstTime() + "\t\t" + p.getArrivalTime() + "\t\t" + p.getWaitingTime() + "\t\t" + p.getTurnaroundTime());
        }

        System.out.println("Average Completion Time: " + (float)totalCompletionTime / (float)processes.size());
        System.out.println("Average Waiting Time: " + (float)totalWaitingTime / (float)processes.size());
        System.out.println("Average Turnaround Time: " + (float)totalTurnaroundTime / (float)processes.size());
    }
}
