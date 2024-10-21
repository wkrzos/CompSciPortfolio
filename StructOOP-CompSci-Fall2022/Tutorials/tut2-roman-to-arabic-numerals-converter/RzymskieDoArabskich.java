import java.util.Scanner; //Biblioteka ze scannerem

class Rzymskie {

    public static void main(String[] args) {

        int[] liczb = { 1000, 500, 100, 50, 10, 5, 1 }; // Char liczb odpowiadających rzymskim

        System.out.print("Wprowadz liczbe w postaci rzymskiej: "); // msg
        Scanner input = new Scanner(System.in); // Scanner do inputu

        Scanner dataInput = new Scanner(System.in); // Enter
        String Rzymskie = dataInput.next();
        dataInput.close(); // Zamknięcie drugiego scannera
        Rzymskie = Rzymskie.toUpperCase(); // W przypadku źle wpisanego stringa przez użytkownika

        // Albo jest liczba, albo (or ||) nie ma liter
        if (Rzymskie.matches(".*[0-9].*") || !Rzymskie.matches("[M|D|C|L|X|V|I]*")) {

            System.out.println("Niepoprawna liczba rzymska. Sprobuj ponownie. Zignoruj wynik.");
        }

        // ____________________________________________________________________________
        int counter = 0;
        char czteryLitery = 'c';

        for (int i = 0; i <= Rzymskie.length() - 1; i++) {

            if (Rzymskie.charAt(i) != czteryLitery) {

                counter = 0;
                czteryLitery = Rzymskie.charAt(i);
            } else {

                counter++;
            }
        }

        if (counter >= 3) {

            System.out.println("4 takie same litery pod rzad. Liczba niepoprawna. Sprobuj ponownie. Zignoruj wynik.");
        }
        // ____________________________________________________________________________

        int i = 0; // Pozycja w stringu Rzymskie
        int now = 0; // Aktualna litera
        int before = 0; // W ten sposób zmienna now jest większe niż beofre pierwszy raz w pętli, więc
                        // nic nie będzie odjęte od arab
        int arab = 0; // Odpowiednik w arabskich części stringa, która została już converted

        while (i < Rzymskie.length()) {

            char letter = Rzymskie.charAt(i); // Litera w obecnej pozycji string'a

            switch (letter) {
                case ('I'):
                    now = 1;
                    break;
                case ('V'):
                    now = 5;
                    break;
                case ('X'):
                    now = 10;
                    break;
                case ('L'):
                    now = 50;
                    break;
                case ('C'):
                    now = 100;
                    break;
                case ('D'):
                    now = 500;
                    break;
                case ('M'):
                    now = 1000;
                    break;
            }

            if (now > before) {

                arab += now - (before * 2);
            } else {

                arab += now;
            }

            before = now;
            i = i + 1; // Do następnej pozycji w stringu
        }

        System.out.println("Liczba rzymska " + Rzymskie + " w systemie arabskim to: " + arab);
    }
}

// Wojciech Krzos 276264
