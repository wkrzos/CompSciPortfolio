import java.util.*;

//Line 66, 75 for printing every page replaced by another

public class PageReplacementSimulation {
    private static final int NUM_PROCESSES = 30;
    private static final int NUM_FRAMES = 100;
    private static final int NUM_REFERENCES = 1000;

    private static List<List<Integer>> referenceSequences;

    public static void main(String[] args) {
        initializeReferenceSequences();

        System.out.println("Symulacja strategii przydziału ramek:");
        System.out.println("Liczba procesów: " + NUM_PROCESSES);
        System.out.println("Liczba ramek: " + NUM_FRAMES);
        System.out.println("Liczba odwołań dla każdego procesu: " + NUM_REFERENCES);
        System.out.println();

        // Przydział proporcjonalny
        System.out.println("Przydział proporcjonalny:");
        simulateAllocation(new ProportionalAllocation());
        System.out.println();

        // Przydział równy
        System.out.println("Przydział równy:");
        simulateAllocation(new EqualAllocation());
        System.out.println();

        // Sterowanie częstością błędów strony
        System.out.println("Sterowanie częstością błędów strony:");
        simulateAllocation(new PageFaultFrequencyControl());
        System.out.println();

        // Model strefowy
        System.out.println("Model strefowy:");
        simulateAllocation(new ZoneModel());
        System.out.println();
    }

    private static void initializeReferenceSequences() {
        referenceSequences = new ArrayList<>();
        Random random = new Random();

        for (int i = 0; i < NUM_PROCESSES; i++) {
            List<Integer> references = new ArrayList<>();
            for (int j = 0; j < NUM_REFERENCES; j++) {
                references.add(random.nextInt(NUM_FRAMES));
            }
            referenceSequences.add(references);
        }
    }

    private static void simulateAllocation(FrameAllocationStrategy allocationStrategy) {
        int[] pageFaults = new int[NUM_PROCESSES];

        for (int i = 0; i < NUM_PROCESSES; i++) {
            List<Integer> referenceSequence = referenceSequences.get(i);
            PageTable pageTable = new PageTable(NUM_FRAMES);

            for (int reference : referenceSequence) {
                if (!pageTable.isPresent(reference)) {
                    pageFaults[i]++;
                    int victim = pageTable.replacePage(reference, allocationStrategy);
                    /* System.out.println("Proces " + i + ": Zastąpiono stronę " + victim + " przez " + reference); */
                }
            }
        }

        int totalPageFaults = Arrays.stream(pageFaults).sum();

        System.out.println("Liczba błędów strony dla każdego procesu:");
        for (int i = 0; i < NUM_PROCESSES; i++) {
            /* System.out.println("Proces " + i + ": " + pageFaults[i]); */
        }

        System.out.println("Liczba błędów strony globalnie: " + totalPageFaults);
    }

    private static void printPageFaultsAllAlgorithms() {
        FrameAllocationStrategy[] algorithms = {
            new ProportionalAllocation(),
            new EqualAllocation(),
            new PageFaultFrequencyControl(),
            new ZoneModel()
        };

        for (FrameAllocationStrategy algorithm : algorithms) {
            simulateAllocation(algorithm);
            System.out.println();
        }
    }
}

interface FrameAllocationStrategy {
    int selectVictim(PageTable pageTable);
}

class ProportionalAllocation implements FrameAllocationStrategy {
    @Override
    public int selectVictim(PageTable pageTable) {
        // Algorytm wybiera stronę na podstawie proporcji liczby odwołań do liczby stron w procesie
        int[] pageReferences = pageTable.getPageReferences();
        int[] pageFrames = pageTable.getPageFrames();

        int totalReferences = Arrays.stream(pageReferences).sum();
        double[] probabilities = new double[pageReferences.length];
        double sumProbabilities = 0.0;

        for (int i = 0; i < pageReferences.length; i++) {
            probabilities[i] = (double) pageReferences[i] / totalReferences;
            sumProbabilities += probabilities[i];
        }

        // Popraw ewentualne niedokładności sumy prawdopodobieństw
        probabilities[probabilities.length - 1] += 1.0 - sumProbabilities;

        // Wybierz stronę do zastąpienia na podstawie prawdopodobieństwa
        double randomValue = Math.random();
        double cumulativeProbability = 0.0;

        for (int i = 0; i < probabilities.length; i++) {
            cumulativeProbability += probabilities[i];
            if (randomValue <= cumulativeProbability) {
                return pageFrames[i];
            }
        }

        // Jeśli nie udało się wybrać strony (powinno być niemożliwe), zwróć pierwszą stronę
        return pageFrames[0];
    }
}

class EqualAllocation implements FrameAllocationStrategy {
    @Override
    public int selectVictim(PageTable pageTable) {
        // Algorytm wybiera stronę na podstawie równego podziału ramek pomiędzy procesy
        int[] pageFrames = pageTable.getPageFrames();
        return pageFrames[0]; // Zawsze zastępuj pierwszą stronę
    }
}

class PageFaultFrequencyControl implements FrameAllocationStrategy {
    private static final int THRESHOLD = 5;

    @Override
    public int selectVictim(PageTable pageTable) {
        int[] pageReferences = pageTable.getPageReferences();
        int[] pageFrames = pageTable.getPageFrames();
        int[] pageFaults = pageTable.getPageFaults();

        // Find the page with the highest fault frequency
        int maxFaultFrequency = Integer.MIN_VALUE;
        int maxFaultFrequencyIndex = -1;

        for (int i = 0; i < pageFrames.length; i++) {
            int faultFrequency = pageFaults[i];
            if (faultFrequency > maxFaultFrequency) {
                maxFaultFrequency = faultFrequency;
                maxFaultFrequencyIndex = i;
            }
        }

        // If the fault frequency is above the threshold, select the page as the victim
        if (maxFaultFrequency >= THRESHOLD) {
            return pageFrames[maxFaultFrequencyIndex];
        }

        // If no page has fault frequency above the threshold, select a random page as the victim
        int randomIndex = new Random().nextInt(pageFrames.length);
        return pageFrames[randomIndex];
    }
}

class ZoneModel implements FrameAllocationStrategy {
    
    @Override
    public int selectVictim(PageTable pageTable) {
        // Algorytm wybiera stronę na podstawie modelu strefowego
        int[] pageReferences = pageTable.getPageReferences();
        int[] pageFrames = pageTable.getPageFrames();

        int localPages = 0;
        int globalPages = 0;

        for (int i = 0; i < pageReferences.length; i++) {
            if (pageReferences[i] < pageReferences.length / 2) {
                localPages++;
            } else {
                globalPages++;
            }
        }

        // Przydziel więcej ramek dla strefy lokalnej
        int localFrames = (int) (pageTable.getNumFrames() * 0.9); //0.7 is a var
        int globalFrames = pageTable.getNumFrames() - localFrames;  //also var

        if (localPages > localFrames) {
            // Wybierz stronę ze strefy lokalnej
            List<Integer> candidates = new ArrayList<>();

            for (int i = 0; i < pageReferences.length; i++) {
                if (pageReferences[i] < pageReferences.length / 2) {
                    candidates.add(pageFrames[i]);
                }
            }

            // Jeśli jest więcej niż jedna kandydatka, wybierz losowo
            int randomIndex = new Random().nextInt(candidates.size());
            return candidates.get(randomIndex);
        } else if (globalPages > globalFrames) {
            // Wybierz stronę ze strefy globalnej
            List<Integer> candidates = new ArrayList<>();

            for (int i = 0; i < pageReferences.length; i++) {
                if (pageReferences[i] >= pageReferences.length / 2) {
                    candidates.add(pageFrames[i]);
                }
            }

            // Jeśli jest więcej niż jedna kandydatka, wybierz losowo
            int randomIndex = new Random().nextInt(candidates.size());
            return candidates.get(randomIndex);
        } else {
            // Wybierz stronę losowo
            int randomIndex = new Random().nextInt(pageFrames.length);
            return pageFrames[randomIndex];
        }
    }
}

class PageTable {
    private int[] pageFrames;
    private int[] pageReferences;
    private int[] pageFaults;

    public PageTable(int numFrames) {
        pageFrames = new int[numFrames];
        pageReferences = new int[numFrames];
        pageFaults = new int[numFrames];
    }

    public int[] getPageFrames() {
        return pageFrames;
    }

    public int[] getPageReferences() {
        return pageReferences;
    }

    public int[] getPageFaults() {
        return pageFaults;
    }

    public int getNumFrames() {
        return pageFrames.length;
    }

    public boolean isPresent(int reference) {
        for (int i = 0; i < pageFrames.length; i++) {
            if (pageFrames[i] == reference) {
                pageReferences[i]++;
                return true;
            }
        }
        return false;
    }

    public int replacePage(int reference, FrameAllocationStrategy allocationStrategy) {
        int victim = allocationStrategy.selectVictim(this);

        for (int i = 0; i < pageFrames.length; i++) {
            if (pageFrames[i] == victim) {
                pageFrames[i] = reference;
                pageReferences[i] = 1;
                pageFaults[i]++;
                break;
            }
        }

        return victim;
    }
}
