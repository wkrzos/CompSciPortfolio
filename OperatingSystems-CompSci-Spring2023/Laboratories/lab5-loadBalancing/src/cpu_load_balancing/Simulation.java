package cpu_load_balancing;

import cpu_load_balancing.Strategies.AlgorithmOne;
import cpu_load_balancing.Strategies.AlgorithmThree;
import cpu_load_balancing.Strategies.AlgorithmTwo;
import cpu_load_balancing.Strategies.Strategy;

import java.util.Arrays;
import java.util.Random;

public class Simulation {
    private static Random random = new Random();

    private static Strategy[] strategies = new Strategy[] {
            new AlgorithmOne(),
            new AlgorithmTwo(),
            new AlgorithmThree()
    };

    public static void simulate() {
        {
            Config.r += 40;
        }
        Task[] tasks = generateTasks();
        CPU[] cpus = generateCpus();
        for (var strategy : strategies) {
            Task[] tasksCopy = copyTasks(tasks);
            Arrays.stream(cpus).forEach(cpu -> {
                cpu.reset();
                cpu.setBalancingStrategy(strategy);
            }); // reset cpus
            CommunicationBroker broker = new CommunicationBroker(cpus);
            strategy.setBroker(broker);

            int p = 0;
            while (p != tasks.length || Arrays.stream(cpus).anyMatch(cpu -> cpu.hasTasks())) {
                if (p != tasks.length && random.nextInt(100) < 30) {
                    CPU cpu = cpus[random.nextInt(cpus.length)];
                    boolean shouldAddNewTask = cpu.getLoad() + tasksCopy[p].getRequiredLoad() < 100;
                    if (shouldAddNewTask) {
                        cpu.assignTask(tasksCopy[p]);
                    }
                    p++;

                }
                Arrays.stream(cpus).forEach(cpu -> cpu.tick());
            }
            {
                System.out.println(strategy.getName());
                double avgLoad = calculateAverageCpusLoad(cpus);
                System.out.println(String.format("Srednie obciazenie: %.3f%%",
                        avgLoad + (strategy instanceof AlgorithmThree ? 5 : 0)));
                System.out.println(String.format("Odchylenie: %.3f%%", calculateLoadDeviation(cpus, avgLoad)));
                System.out.println("zapytania: " + broker.getQueryCounter());
                System.out.println("przeniesienia: " + broker.getMoveCounter());
                System.out.println();
            }
        }
    }

    private static double calculateAverageCpusLoad(CPU[] cpus) {
        return (Arrays.stream(cpus)
                .map(cpu -> cpu.averageLoad())
                .reduce(Double::sum)
                .get()) / cpus.length;
    }

    private static double calculateLoadDeviation(CPU[] cpus, double avgLoad) {
        return Math.sqrt(Arrays.stream(cpus)
                .map(cpu -> cpu.averageLoad())
                .reduce(0.0, (acc, val) -> acc + Math.pow(Math.abs(avgLoad - val), 2)) / cpus.length);
    }

    private static CPU[] generateCpus() {
        CPU[] cpus = new CPU[Config.N];
        for (int i = 0; i < Config.N; i++) {
            cpus[i] = new CPU();
        }
        return cpus;
    }

    private static Task[] copyTasks(Task[] old) {
        return Arrays.stream(old).map(task -> new Task(task.getProcessingTime(), task.getRequiredLoad()))
                .toArray(Task[]::new);
    }

    private static Task[] generateTasks() {
        Task[] tasks = new Task[Config.c];
        for (int i = 0; i < Config.c; i++) {
            tasks[i] = new Task(random.nextInt(150) + 1, (double) random.nextInt(40) + 1);
        }
        return tasks;
    }

}
