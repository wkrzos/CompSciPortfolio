package main;

import util.CSCAN;
import util.EDF;
import util.FCFS;
import util.FDSCAN;
import util.RandomProcessGenerator;
import util.SCAN;
import util.SSTF;
import util.schedulingAlgorithms.*;

public class Main {

    int[] requests;
    int[] deadlines;

    public static void main(String[] args) {

        int head = 50;
        int direction = 1;

        //Test data
        //int[] requests = {98, 183, 37, 122, 14, 124, 65, 67}; // przykładowa kolejka żądań
        //int[] deadlines = {200, 300, 250, 500, 150, 400, 300, 350 };

        //int[] requests = {50, 50, 50, 50, 50, 50, 50, 50};
        //int[] deadlines = {100, 100, 100, 100, 100, 100, 100, 100};

        //int[] requests = {1000, 2000, 500, 2500, 100, 3000, 1500, 800};
        //int[] deadlines = {2000, 2500, 3000, 4000, 1500, 3500, 4500, 5000};

        //Randomized
        int maxTrack = 500; // maksymalna liczba bloków na dysku
        int[] requests = RandomProcessGenerator.generate(maxTrack, 100);
        int[] deadlines = RandomProcessGenerator.generateRandomDeadlines(requests, 10);

        
        // testowanie algorytmu FCFS
        int fcfsSeekCount = FCFS.sortFCFS(requests.clone(), head);
        System.out.println("FCFS: " + fcfsSeekCount);
        
        // testowanie algorytmu SSTF
        int sstfSeekCount = SSTF.sortSSTF(requests.clone(), head);
        System.out.println("SSTF: " + sstfSeekCount);
        
        // testowanie algorytmu SCAN
        int scanSeekCount = SCAN.sortSCAN(requests.clone(), head, direction);
        System.out.println("SCAN: " + scanSeekCount);
        
        // testowanie algorytmu C-SCAN
        int cScanSeekCount = CSCAN.sortCSCAN(requests.clone(), head, direction);
        System.out.println("C-SCAN: " + cScanSeekCount);
        
        // testowanie algorytmu EDF
        int edfSeekCount = EDF.sortEDF(requests.clone(), head, deadlines);
        System.out.println("EDF: " + edfSeekCount);
        
        // testowanie algorytmu FD-SCAN
        int fdScanSeekCount = FDSCAN.sortFDSCAN(requests.clone(), head, deadlines, direction);
        System.out.println("FD-SCAN: " + fdScanSeekCount);
    }
}