public class quadratic {

    public static void main(String[] args) {
  
      //Podanie wartości potrzebnych 
      //do obliczenia ax²+bx+c=0 
      double a = -325, b = 125, c = -2;

      //Stworzenie zmiennych dla 
      //2 możliwych pierwiastków
      double pierwiastek1, pierwiastek2;
  
      //Obliczanie delty
      double delta = b * b - 4 * a * c;
  
      //Jeżeli delta większa od 0
      if (delta > 0) {
  
        //Mamy 2 pierwiastki
        //pierwiastek 1
        pierwiastek1 = (-b + Math.sqrt(delta)) / (2 * a);
        //pierwiastek 2
        pierwiastek2 = (-b - Math.sqrt(delta)) / (2 * a);

        //Zwrot informacji
        System.out.format("pierwiastek1 = %.2f and pierwiastek2 = %.2f", pierwiastek1, pierwiastek2);
      }
  
      //Jeżeli delta równa 0
      else if (delta == 0) {

        pierwiastek1 = pierwiastek2 = -b / (2 * a);
        System.out.format("pierwiastek1 = pierwiastek2 = %.2f;", pierwiastek1);
      }
  
      //Delta mniejsza od 0, liczby zespolone
      else {
  
        double rzeczywiste = -b / (2 * a);
        double zespolone = Math.sqrt(-delta) / (2 * a);
        System.out.format("pierwiastek1 = %.2f+%.2fi", rzeczywiste, zespolone); //System.out.println nie działa dla tych argumentów
        System.out.format("\npierwiastek2 = %.2f-%.2fi", rzeczywiste, zespolone);
      }
    }
  }