public class Zadanie_2 {

    public static void main(String[] args){
    
        double x = 3;                   //Podstawa potęgi
        long k = 646;                   //Liczba naturalna z 0

        double l = 1;                   //Zmienna l dla obliczania połowy potęgi, nie zmieniać
        double wynik = 1;               //Wynik potęgowania, nie zmieniać

        if(k % 2 == 0) {                //Dla parzystej liczby potęgi
            l = k / 2;
            
            while (l != 0){ 
                wynik = wynik * x;
                --l;
            }

            wynik = wynik * wynik;
            
        } else {                        //Dla nieparzystej liczby potęgi
            l = (k - 1) / 2;

            while (l != 0){ 
                wynik = wynik * x;
                --l;
            }

            wynik = wynik * wynik * x;
        }

        System.out.println("__________________________" + "\n\n" + "Wynik tej potegi = " + wynik + "\n" + "__________________________" + "\n");
    }
}

//Można rozdzielić na mniej mnożeń: x^4 = x^2 * x^2, zamiast 4 mamy 3.
//Przy potęgach nieparzystych: 5 = (2 + 2) + 1 lub 5 = (3 + 3) - 1
//Poprzez ten zabieg maskymalna potęga wzrosła ze 170 do 646