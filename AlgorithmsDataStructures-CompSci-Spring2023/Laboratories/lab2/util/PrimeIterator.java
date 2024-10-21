package util;

import java.util.Iterator;
import java.util.NoSuchElementException;

public class PrimeIterator implements Iterator<Integer> {
    
    private int min;
    private int max;

    public PrimeIterator(int start, int end) {
        this.min = start;
        this.max = end;
    }

    @Override
    public boolean hasNext() {
        while (min <= max) {
            if (isPrime(min)) {
                return true;
            }
            min++;
        }
        return false;
    }

    @Override
    public Integer next() {
        if (!hasNext()) {
            throw new NoSuchElementException();
        }
        int prime = min;
        min++;
        while (min <= max) {
            if (isPrime(min)) {
                break;
            }
            min++;
        }
        return prime;
    }

    private boolean isPrime(int number) {
        if (number <= 1) {
            return false;
        }
        for (int i = 2; i <= Math.sqrt(number); i++) {
            if (number % i == 0) {
                return false;
            }
        }
        return true;
    }
}