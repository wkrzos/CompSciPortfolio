import java.util.ArrayList;

import updated.ProcessRR;


public class MainOld {

    static ArrayList<ProcessSJFOld> processList1 = new ArrayList<>();
    static ArrayList<ProcessSJFOld> processList2 = new ArrayList<>();
    static ArrayList<ProcessSJFOld> processList3 = new ArrayList<>();
    static ArrayList<ProcessRR> processList4 = new ArrayList<>();

    public static void main(String args[]) {
        //createProcessList();
        generateRandomProcessList();

        calculateFCFS();
        calculateSJF();
        calculateWSJF();
    }

/*     private static void createProcessList() {
        processList1.add(new Process(0, 0, 3, 0, 0, 0));
        processList1.add(new Process(0, 0, 25, 0, 0, 0));
        processList1.add(new Process(0, 0, 5, 0, 0, 0));
        processList1.add(new Process(0, 0, 71, 0, 0, 0));
        processList1.add(new Process(0, 0, 12, 0, 0, 0));
        processList1.add(new Process(0, 0, 49, 0, 0, 0));
        processList1.add(new Process(0, 0, 9, 0, 0, 0));

        processList2 = processList1;
    } */

    private static void generateRandomProcessList(){
        RandomBurstTimeGenerator rbtg = new RandomBurstTimeGenerator();
        processList1 = rbtg.fillProcessList();
        processList2 = processList1;

    }

/*     private static void generateRandomProcessRRList(){
        processList4.add(new ProcessRR(0, 0, 0, 0, 0, 0, 0, false));
    } */

    private static void printProcesses(ArrayList<ProcessSJFOld> inputList) {
        for (int i = 0; i < inputList.size(); i++) {
            inputList.get(i).printState();
        }
    }

    private static void calculateFCFS(){
        FCFS fcfs = new FCFS();
        System.out.println("_________new test_________");
        fcfs.setProcessIDs(processList1);
        fcfs.calculateArrivalTime(processList1);
        fcfs.calculateCompletionTime(processList1);
        fcfs.calculateTurnAroundTime(processList1);
        fcfs.calculateWaitingTime(processList1);
        printProcesses(processList1);
        System.out.println("\n\nAverage Completion Time: " + fcfs.calculateAverageCompletionTime(processList1));
    }

    private static void calculateSJF(){
        SJF sjf = new SJF();
        sjf.sortProcessByBurstTime(processList2);
        System.out.println("_________new test_________");
        sjf.setProcessIDs(processList2);
        sjf.calculateArrivalTime(processList2);
        sjf.calculateCompletionTime(processList2);
        sjf.calculateTurnAroundTime(processList2);
        sjf.calculateWaitingTime(processList2);
        printProcesses(processList2);
        System.out.println("\n\nAverage Completion Time: " + sjf.calculateAverageCompletionTime(processList2));
    }

    private static void calculateWSJF(){
        WSJF wsjf = new WSJF();
        wsjf.sortProcessByBurstTime(processList2);
        System.out.println("_________new test_________");
        wsjf.setProcessIDs(processList2);
        wsjf.calculateArrivalTime(processList2);
        wsjf.calculateCompletionTime(processList2);
        wsjf.calculateTurnAroundTime(processList2);
        wsjf.calculateWaitingTime(processList2);
        printProcesses(processList2);
        System.out.println("\n\nAverage Completion Time: " + wsjf.calculateAverageCompletionTime(processList2));
    }
}