package cpu_load_balancing.Strategies;

import cpu_load_balancing.CPU;
import cpu_load_balancing.CommunicationBroker;
import cpu_load_balancing.Config;
import cpu_load_balancing.Task;

public class AlgorithmThree implements Strategy{
    private CommunicationBroker broker;

    @Override
    public void setBroker(CommunicationBroker broker) {
        this.broker = broker;
    }

    @Override
    public void onTaskAssigned(CPU assignedTo, Task task) {
        broker.notifyCPUs();
    }

    @Override
    public void onNotified(CPU notitfiedCPU) {
        if(notitfiedCPU.getLoad() > Config.r) {
            return;
        }
        int idx = broker.generateRandomCpuSequence(notitfiedCPU, 1)[0];
        double load = broker.queryCpuLoad(idx);
        if(load < Config.p) {
            return;
        }
        CPU offloadedCPU = broker.getCPU(idx);
        while(offloadedCPU.getLoad() > Config.p) {
            if(notitfiedCPU.getLoad() + offloadedCPU.getLastTask().getRequiredLoad() > 100) {
                break;
            }
            broker.moveTask(offloadedCPU, broker.getCPUIdx(notitfiedCPU), offloadedCPU.getLastTask());
        }

    }

    @Override
    public String getName() {
        return "Trzeci";
    }
}
