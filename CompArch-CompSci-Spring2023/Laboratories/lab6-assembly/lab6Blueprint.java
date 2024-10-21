public class lab6Blueprint {
    public static void main(String[] args) {
        int N = 100; // Zakres początkowych liczb naturalnych
        int[] numbers = new int[N + 1]; // Tablica liczb, zaczynając od 0 do N
        
        // Inicjalizacja tablicy
        for (int i = 1; i <= N; i++) {
            numbers[i] = i;
        }
        
        // Implementacja sita Eratostenesa
        for (int i = 2; i <= Math.sqrt(N); i++) {
            if (numbers[i] != 0) {
                for (int j = i * i; j <= N; j += i) {
                    numbers[j] = 0;
                }
            }
        }
        
        // Liczenie liczby liczb pierwszych
        int nPrimes = 0;
        for (int i = 2; i <= N; i++) {
            if (numbers[i] != 0) {
                nPrimes++;
            }
        }
        
        // Zapisywanie liczb pierwszych do tablicy primes
        int[] primes = new int[nPrimes];
        int index = 0;
        for (int i = 2; i <= N; i++) {
            if (numbers[i] != 0) {
                primes[index] = numbers[i];
                index++;
            }
        }
        
        // Wypisywanie liczb pierwszych na konsoli
        for (int prime : primes) {
            System.out.println(prime);
        }
    }
}