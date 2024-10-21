package cpu_load_balancing.Strategies;

import cpu_load_balancing.CPU;
import cpu_load_balancing.CommunicationBroker;
import cpu_load_balancing.Config;
import cpu_load_balancing.Task;

import java.util.HashSet;

public class AlgorithmOne implements Strategy {
    private CommunicationBroker broker;
    @Override
    public void setBroker(CommunicationBroker broker) {
        this.broker = broker;
    }

    @Override
    public void onTaskAssigned(CPU assignedTo, Task task) {
        int[] cpusToQuery = broker.generateRandomCpuSequence(assignedTo, Config.z);
        for(int idx : cpusToQuery) {
            double load = broker.queryCpuLoad(idx);
            if(load < Config.p && load + task.getRequiredLoad() < 100) {
                broker.moveTask(assignedTo, idx, task);
                break;
            }
        }

    }

    @Override
    public void onNotified(CPU notitfiedCPU) {
    }

    @Override
    public String getName() {
        return "Pierwszy";
    }


}
