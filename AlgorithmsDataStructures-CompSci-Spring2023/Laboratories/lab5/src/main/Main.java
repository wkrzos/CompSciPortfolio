package main;

import java.util.Arrays;
import java.util.Comparator;

public class Main {

    int CAR_ARR_SIZE = 5;

    Car[] carArray = new Car[5];

    public static void main(String[] args) {
        demo1();
    }

    private static void demo1() {

        Car[] samochody = {
                new Car("Toyota", "Czarny", 2015),
                new Car("Ford", "Niebieski", 2011)
        };

        System.out.println("Nieposortowane: " + Arrays.toString(samochody));

        // Sortowanie bąbelkowe po marce
        bubbleSort(samochody, Comparator.comparing(s -> s.brand));
        System.out.println("Posortowane po marce (bubble sort): " + Arrays.toString(samochody));

        // Sortowanie przez wstawianie po roku produkcji
        insertionSort(samochody, Comparator.comparingInt(s -> s.yearOfProduction));
        System.out.println("Posortowane po roku produkcji (insertion sort): " + Arrays.toString(samochody));

        // Sortowanie przez wybieranie po kolorze i marce
        selectionSort(samochody, Comparator.comparing((s -> s.colour).thenComparing(s -> s.brand)));
        System.out.println("Posortowane po kolorze i marce (selection sort): " + Arrays.toString(samochody));

        // Sortowanie przez wstawianie z wykorzystaniem złożonej metody porównywania
        Arrays.sort(samochody, (s1, s2) -> {
            if (s1.brand.compareTo(s2.brand) != 0) {
                return s1.brand.compareTo(s2.brand);
            } else if (s1.colour
                    .compareTo(s2.colour) != 0) {
                return s1.colour
                        .compareTo(s2.colour);
            } else {
                return Integer.compare(s1.yearOfProduction, s2.yearOfProduction);
            }
        });
        System.out.println("Posortowane z wykorzystaniem złożonej metody porównywania (insertion sort): "
                + Arrays.toString(samochody));
    }
}
