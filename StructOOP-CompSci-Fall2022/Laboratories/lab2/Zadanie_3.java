public class Zadanie_3 {

    public static double E_x_wk() {
        
        long x01 = 500; //Wartość x, tylko liczby całkowite
        int n01 = 10000; //Ilość wyrazów ciągu (dokładność przybliżenia)

        double Suma01 = 1;
        double tmp01 = 1;
        long k01 = 1;

        while(k01 <= n01) { 
            tmp01 = tmp01 * x01 / k01;
            Suma01 = Suma01 + tmp01;
            k01 = k01 + 1;
        } 

        System.out.print("Przyblizenie 2 funkcji do " + n01 + " wyrazu to: " + Suma01);
        return Suma01;
    }

    public static double Sin_x_wk() {

        double x02 = 1; //Wartość x
        int n02 = 3; //Ilość wyrazów ciągu (dokładność przybliżenia)

        long k02 = 1;
        double Suma02 = x02;
        double tmp02 = x02;

        while(k02 < n02) { 
            tmp02 = (-1) * tmp02 * ((x02 * x02) / ((2 * k02 + 1) * (2 * k02)));
            Suma02 = Suma02 + tmp02;
            k02 = k02 + 1;
        } 

        System.out.print("\n" + "Przyblizenie 2 funkcji do " + n02 + " wyrazu to: " + Suma02);
        return Suma02; 
    }

    public static double Cos_x_wk() { //Parametry funckji w () - na wejściu

        double x03 = 5; //Wartość x
        int n03 = 10000; //Ilość wyrazów ciągu (dokładność przybliżenia)

        double Suma03 = 1;
        long k03 = 1;
        double tmp03 = x03;

        while(k03 < n03) {
            tmp03 = (-1) * tmp03 * ((x03 * x03) / ((2 * k03) * (2 * k03 - 1)));
            Suma03 = Suma03 + tmp03;
            k03 = k03 + 1;
        } 

        System.out.print("\n" + "Przyblizenie 2 funkcji do " + n03 + " wyrazu to: " + Suma03);
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
