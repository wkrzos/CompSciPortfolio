package Składzik;
import java.util.Random;

public class Zadanie01 {

    static int m = 20; //Size of the array
    static int k = 50; //How many whole numbers?

    public static void main(String[] args)
    {
            int [] x = new int[m];

            Zadanie01 object = new Zadanie01();

            object.fill(x,k);

            int p = object.evenCounter(x);
            int [] even = new int[p];
            int [] odd = new int[x.length-p];
            
            System.out.println("\n_______________\nPrint: ");
            object.print(x);

            System.out.println("\n\nPrint reversed:");
            object.printR(x);
            System.out.println("\n_______________");

            object.oddAndEven(x,even,odd);
            System.out.println("\n\n_______________\nEven:");
            object.print(even);
            System.out.println("\nOdd:");
            object.print(odd);
            System.out.println("\n_______________");

            System.out.print("\n_______________\nMin: " + object.min(x));
            System.out.print("\nMax: " + object.max(x) + "\n_______________");       
    }

    //Fill the array_____________________________
    public void fill(int [] x,int k){
        Random generated = new Random();
        for (int i = 0; i < x.length; i++) {
            x[i] = generated.nextInt(k);
        }
    }

    //Print_______________________________________
    public void print(int [] x){
        for (int i = 0; i < x.length; i++) {
            System.out.print(x[i]+" ");
        }
    }

    //Print in reversed order_____________________
    public void printR(int [] x){
        for (int i = x.length-1; i > -1; i--) {
            System.out.print(x[i]+" ");
        }
    }

    //Counting even nubmers________________________
    public int evenCounter(int [] x){
        int numOfEven = 0;
        for (int i = 0; i < x.length; i++) {
            if (x[i] % 2 == 0){
                numOfEven += 1;
            }
        }
        return numOfEven;
    }

    //Odd or Even___________________________________
    public void oddAndEven(int [] x,int [] p,int [] n){
        int j = 0;

        for (int i = 0; i < x.length; i++) {
            if (x[i]%2==0){
                p[j]=x[i];
                j += 1;
            }
        }

        j = 0;
        for (int i = 0; i < x.length; i++) {

            if (x[i]%2!=0){
                n[j]=x[i];
                j += 1;
            }
        }
    }

    //Findinx MIN_________________________________
    public int min(int [] x){

        int min = x[0];

        for (int i = 0; i < x.length; i++) {

            for (int j = 1; j < x.length; j++) {

                if (min>x[j]){

                    min = x[j];
                }
            }
        }

        return min;
    }

    //Findinx MAX__________________________________
    public int max(int [] x){

        int max = x[0];

        for (int i = 0; i < x.length; i++) {

            for (int j = 1; j < x.length; j++) {

                if (max<x[j]){

                    max = x[j];
                }
            }
        }

        return max;
    }
}
