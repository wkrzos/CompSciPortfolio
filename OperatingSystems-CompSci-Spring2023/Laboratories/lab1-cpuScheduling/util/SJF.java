import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;

public class SJF extends FCFS{

    public SJF() {
        
    }
    
    public void sortProcessByBurstTime(ArrayList<ProcessSJFOld> inputList){
        Collections.sort(inputList, new Comparator<ProcessSJFOld>() {
            @Override
            public int compare(ProcessSJFOld o1, ProcessSJFOld o2) {
                return Integer.valueOf(o1.getBurstTime()).compareTo(Integer.valueOf(o2.getBurstTime()));
            }
        });
    }
}
