import java.util.ArrayList;

import updated.FCFSScheduler;
import updated.ProcessFCFS;
import updated.ProcessRR;
import updated.ProcessSJF;
import updated.RRScheduler;
import updated.SJFScheduler;


public class MainUpdated {

    static ArrayList<ProcessSJFOld> processList1 = new ArrayList<>();

    public static void main(String args[]) {
        generateRandomProcessList();

        calculateFCFS();
        calculateSJF();
        calculateRR();
    }

    private static void generateRandomProcessList(){
        RandomBurstTimeGenerator rbtg = new RandomBurstTimeGenerator();
        processList1 = rbtg.fillProcessList();
    }

    private static void calculateFCFS(){
        System.out.println("_________new test_________");
        
        ArrayList<ProcessFCFS> arr = new ArrayList<>();

        for(int i = 0; i < processList1.size(); i++){
            arr.add(new ProcessFCFS(i, 0, processList1.get(i).getBurstTime()));
        }

        FCFSScheduler fcfs = new FCFSScheduler();
        fcfs.run(arr, 0);
    }

    private static void calculateSJF(){
        System.out.println("_________new test_________");

        ArrayList<ProcessSJF> arr = new ArrayList<>();

        for(int i = 0; i < processList1.size(); i++){
            arr.add(new ProcessSJF(i, 0, processList1.get(i).getBurstTime()));
        }

        SJFScheduler sjfs = new SJFScheduler(arr, true);
        sjfs.run();
    }

    private static void calculateRR(){
        System.out.println("_________new test_________");

        ArrayList<ProcessRR> arr = new ArrayList<>();

        for(int i = 0; i < processList1.size(); i++){
            arr.add(new ProcessRR(Integer.toString(i), 0, processList1.get(i).getBurstTime()));
        }

        RRScheduler rrs = new RRScheduler(arr, 10000);
        rrs.run();
        rrs.printResults();
    }

    
}