import java.util.ArrayList;
import java.util.ListIterator;

public class FCFS {

    public FCFS(){

    }

    void setProcessIDs(ArrayList<ProcessSJFOld> inputList) {
        for (int i = 0; i < inputList.size(); i++) {
            inputList.get(i).setProcessID(i);
        }
    }

    void calculateArrivalTime(ArrayList<ProcessSJFOld> inputList) {

        int temp = 0;

        try {
            for (int i = 0; i < inputList.size(); i++) {
                temp += inputList.get(i).getBurstTime();
                inputList.get(i + 1).setArrivalTime(temp);
            }
        } catch (Exception e) {
            return;
        }
    }

    void calculateCompletionTime(ArrayList<ProcessSJFOld> inputList) {

        ListIterator<ProcessSJFOld> iter = inputList.listIterator();
        int temp = 0;

        while (iter.hasNext()) {
            temp += iter.next().getBurstTime();

            inputList.get(iter.previousIndex()).setCompletionTime(temp);
        }
    }

    void calculateTurnAroundTime(ArrayList<ProcessSJFOld> inputList) {

        for (ProcessSJFOld process : inputList) {
            process.setTurnAroundTime(process.getCompletionTime() - process.getArrivalTime());
        }
    }

    void calculateWaitingTime(ArrayList<ProcessSJFOld> inputList) {

        ListIterator<ProcessSJFOld> iter = inputList.listIterator();
        int temp = 0;

        while (iter.hasNext()) {
            temp += iter.next().getBurstTime();

            inputList.get(iter.previousIndex()).setWaitingTime(temp);
        }
    }

    double calculateAverageCompletionTime(ArrayList<ProcessSJFOld> inputList) {

        double averageCompletionTime = 0;

        for (int i = 0; i < inputList.size(); i++) {
            averageCompletionTime += inputList.get(i).getCompletionTime();
        }

        averageCompletionTime = averageCompletionTime / inputList.size();
        return averageCompletionTime;
    }
}
