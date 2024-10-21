package cpu_load_balancing;

import cpu_load_balancing.Strategies.Strategy;

import java.util.ArrayList;

public class CPU {
    private ArrayList<Task> tasks = new ArrayList<>();

    double averageLoad = 0.0;
    long time = 0;

    private ArrayList<Double> loadHistory = new ArrayList<>();
    private Strategy balancingStrategy;

    public void assignTask(Task task) {
        tasks.add(task);
        task.reassign(this);

        balancingStrategy.onTaskAssigned(this, task);

    }

    public Task getLastTask() {
        return this.tasks.get(this.tasks.size() - 1);
    }

    public boolean hasTasks() {
        return this.tasks.size() > 0;
    }

    public boolean unassignTask(Task task) {
        if (tasks.remove(task)) {
            task.unassign();
            return true;
        } else {
            return false;
        }
    }

    public void moveTask(CPU moveFrom, Task taskToMove) {
        if (moveFrom.unassignTask(taskToMove)) {
            tasks.add(taskToMove);
            taskToMove.reassign(this);
        }

    }

    public void tick() {
        time++;
        if (tasks.size() != 0) {
            Task t = tasks.get(0);
            t.tick();
            if (t.isDone()) {
                t.unassign();
                tasks.remove(0);
            }
        }
        averageLoad = averageLoad + (getLoad() - averageLoad) / time;
    }

    public double getLoad() {
        if (tasks.size() == 0) {
            return 0.0;
        }
        double load = this.tasks.stream().map(t -> t.getRequiredLoad()).reduce(Double::sum).get();
        if (load > 100) {

        }
        return load;
    }

    public double averageLoad() {
        return averageLoad;
    }

    // algorytm 3
    public void onNotified() {
        balancingStrategy.onNotified(this);
    }

    public void reset() {
        tasks = new ArrayList<>();
        loadHistory = new ArrayList<>();

        averageLoad = 0.0;
        time = 0;
    }

    public void setBalancingStrategy(Strategy balancingStrategy) {
        this.balancingStrategy = balancingStrategy;
    }
}
