package cpu_load_balancing.Strategies;

import cpu_load_balancing.CPU;
import cpu_load_balancing.CommunicationBroker;
import cpu_load_balancing.Task;

public interface Strategy {
    void setBroker(CommunicationBroker broker);
    void onTaskAssigned(CPU assignedTo, Task task);
    void onNotified(CPU notitfiedCPU);

    String getName();
}
