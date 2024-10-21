public class nwd {
    //Metoda nwd
    static int nwd(int num01, int num02){
        
        //Przechowuje zmienną a dla pętli poniżej
        int a = 0;                                              //Przypisanie chwilowej wartości int a
        if (num01 < num02)
            a = num01;
        else                                                    //(num01 > num02)
            a = num02;

        //Loop dla mniejszej z num01 i num02
        for (a = a; a > 1; a--){

            if (num01 % a == 0 && num02 % a == 0)
                return a;
        }

        return 1;                                               //W wypadku num01=0 albo num02=0
    }

    public static void main(String[] args){                     //Przywołanie + komunikat
        int num01 = 244, num02 = 320;                           //Dane wejściowe

        System.out.println("nwd = " + nwd(num02, num01)); 
    }
}
