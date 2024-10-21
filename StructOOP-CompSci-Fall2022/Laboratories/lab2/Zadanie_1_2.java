class Zadanie_1_2{

    public static void main(String args[]){  

     int i; //Zmienna dla for loop
     double silnia = 1; //Wynik działania 
     double liczba = 170; //Liczba na którą nakładamy silnię 

     for (i = 1; i <= liczba; i++){    
         silnia = silnia * i;    
     }    

     System.out.println("_________________________" + "\n\n" + "Silnia z " + liczba + " to " + silnia + "\n" + "_________________________");    
    }  
   }  