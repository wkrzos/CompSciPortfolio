class obliczanieSilni{  //Klasa
  
    static double silnia(double n){  //Metoda silnia  
     if (n == 0)    
       return 1;    
     else    
       return(n * silnia(n-1));    
    }    
    
    public static void main(String args[]){  

     double silnia = 1; //Wynik działania silnia
     double liczba = 170; //Liczba na której użyjemy silni 

     silnia = silnia(liczba); //Przywołanie metody

     System.out.println("_________________________" + "\n\n" + "Silnia z " + liczba + " to " + silnia + "\n" + "_________________________");    
    }  
   }  