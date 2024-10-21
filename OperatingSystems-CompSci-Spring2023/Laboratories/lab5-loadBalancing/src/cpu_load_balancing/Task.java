package cpu_load_balancing;

public class Task {
    private int processingTime;
    private int remainingTime;
    private CPU assignedTo = null;
    private double requiredLoad;

    public Task(int processingTime, double requiredLoad) {
        this.processingTime = processingTime;
        this.remainingTime = processingTime;
        this.requiredLoad = requiredLoad;
    }

    public void reassign(CPU cpu) {
        this.assignedTo = cpu;
    }

    public void unassign() {
        this.assignedTo = null;
    }
    public void tick() {
        remainingTime--;

    }
    public boolean isDone() {
        return remainingTime == 0;
    }

    public int getProcessingTime() {
        return processingTime;
    }

    public int getRemainingTime() {
        return remainingTime;
    }

    public CPU getAssignedTo() {
        return assignedTo;
    }

    public double getRequiredLoad() {
        return requiredLoad;
    }
}
