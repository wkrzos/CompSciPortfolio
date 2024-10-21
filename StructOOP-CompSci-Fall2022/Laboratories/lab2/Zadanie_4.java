public class Zadanie_4 {

    public static double Potega(double x, double k) { //x podstawa potegi, k liczba naturalna z 0 (potega)

        double l = 1;                   //Zmienna l dla obliczania połowy potęgi, nie zmieniać
        double potega = 1;               //Wynik potęgowania, nie zmieniać

        if(k % 2 == 0) {                //Dla parzystej liczby potęgi
            l = k / 2;
            
            while (l != 0){ 
                potega = potega * x;
                --l;
            }

            potega = potega * potega;
            return potega;
            
        } else {                        //Dla nieparzystej liczby potęgi
            l = (k - 1) / 2;

            while (l != 0){ 
                potega = potega * x;
                --l;
            }

            potega = potega * potega * x;
            return potega;
        }
    }

    public static double Silnia(double liczba) {
       
        double i;
        double silnia = 1; //Wynik działania 
   
        for (i = 1; i <= liczba; i++){    
            silnia = silnia * i;    
        } 

        while (liczba == 0) {
            silnia = 1;
            liczba = -1; //Przerywamy pętlę zamiast break
        }
   
        return silnia;
    }

    public static double E_x_wk() {
        
        long x = 5; //Wartość x, tylko liczby całkowite
        int n01 = 10; //Ilość wyrazów ciągu (dokładność przybliżenia)

        double Suma01 = 1;
        double tmp01 = 1;
        long k = 0;

        while(k <= n01) { 
            tmp01 = Potega(x, k) / Silnia(k);
            Suma01 = Suma01 + tmp01;
            k = k + 1;
        } 

        System.out.print("Przyblizenie pierwszej funkcji (potega e) do " + n01 + " wyrazu to: " + Suma01);
        return Suma01;
    }

    public static double Sin_x_wk() {

        double x02 = 5; //Wartość x
        int n02 = 10; //Ilość wyrazów ciągu (dokładność przybliżenia)

        double k02 = 0;
        double Suma02 = 0;
        double tmp02 = 0;

        while(k02 < n02) { 
            tmp02 = Potega((-1), k02) * (Potega((x02), (2*k02+1)) / Silnia(2*k02+1));
            Suma02 = Suma02 + tmp02;
            k02 = k02 + 1;
        } 

        System.out.print("\n" + "Przyblizenie drugiej funkcji (sin) do " + n02 + " wyrazu to: " + Suma02);
        return Suma02; 
    }

    public static double Cos_x_wk() {

        double x03 = 5; //Wartość x
        int n03 = 10; //Ilość wyrazów ciągu (dokładność przybliżenia)

        double Suma03 = 0;
        long k03 = 0;
        double tmp03 = 0;

        while(k03 < n03) {
            tmp03 = Potega((-1), k03) * Potega(x03, 2*k03) / Silnia(2*k03);
            Suma03 = Suma03 + tmp03;
            k03 = k03 + 1;
        } 

        System.out.print("\n" + "Przyblizenie trzeciej funkcji (cos) do " + n03 + " wyrazu to: " + Suma03);
        return Suma03; 

    }

    public static void main(String[] args) {
        System.out.println("\n" + "________________________________________________________________________________" + "\n\n");
        E_x_wk();
        Sin_x_wk();
        Cos_x_wk();
        System.out.println("\n\n" + "________________________________________________________________________________" + "\n");
    }
}
//Dużą zaletą stworzenia metod jest łatwość z jaką możemy implementować je w innych częściach kodu.
//Kalkulacje, które były dość nieintuicyjne zostały zastąpione zrozumiałymi metodami Potega i Silnia.
//Nie jest jasny wpływ na wydajność kodu, jednak zakłada się, że została ona zwiększona z racji na zmniejszoną liczbę działań w pętlach dla 3 funkcji.
//Wadą tego rozwiązania może być mniejsza czytelność dla zewnętrznego obserwatora,
//to może wpłynąć na zmniejszoną wydajność pracy zespołowej - czyli podstawie pracy programisty.
//Dodatkowe komentarze są bardzo przydatne w takiej sytuacji.