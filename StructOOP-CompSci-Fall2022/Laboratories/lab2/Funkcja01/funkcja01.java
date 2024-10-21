package Funkcja01;
public class funkcja01 {

    
    static void silnia(){

    }

     public static void main(String[] args){

        long x = 1; //Wartość x
        int n = 5; //Ilość wyrazów ciągu (dokładność przybliżenia)

        double Suma = 1;
        double tmp = 1;
        long k = 1;

        while(k <= n) { 
            tmp = tmp * x / k;
            Suma = Suma + tmp;
            k = k + 1;
        } 

        System.out.println("Wynik: " + Suma);
    }
}
