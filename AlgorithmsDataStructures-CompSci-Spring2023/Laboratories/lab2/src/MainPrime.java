package src;

import util.PrimeIterator;

public class MainPrime {

    private static final int MIN_INT = 1;
    private static final int MAX_INT = 100;

    public static void main(String[] args){
        generatePrimeNumbers();
    }

    private static void generatePrimeNumbers(){
        PrimeIterator fpi = new PrimeIterator(MIN_INT, MAX_INT);

        while(fpi.hasNext()){
            System.out.println(fpi.next());
        }
    }
}
