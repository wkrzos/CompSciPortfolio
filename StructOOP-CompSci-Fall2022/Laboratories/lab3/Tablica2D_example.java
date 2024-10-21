import java.util.Random;

public class Tablica2D_example {

    final static int w = 5;

    public static void main(String[] args) {

        double [][] Tab = new double[w][];

        Tab[0] = new double[2];
        Tab[1] = new double[2];
        Tab[2] = new double[2];
        Tab[3] = new double[2];
        Tab[4] = new double[2];

        Tablica2D_example obT = new Tablica2D_example();
        obT.wypelnijMacierz(Tab);
        obT.drukujMacierz(Tab);

        System.out.println("\n\n" + "Max Tablicy = " + obT.szukajMax(Tab));
    }

    //Wypełnianie tablicy
    public void wypelnijMacierz(double [][] T) {

        Random generator = new Random();

        for(int i = 0; i < T.length; i++) {

            for(int j = 0; j < T[i].length; j++) {

                T[i][j] = generator.nextDouble() * 10;
            }
        }
    }

    //Wartość tablicy
    public void drukujMacierz(double [][] T) {

        for(int i = 0; i < T.length; i++) {

            for(int j = 0; j < T[i].length; j++) {

                System.out.print("Tab[" + i + "]" + "[" + j + "]" + "=" + T[i][j] + "\t");
            }

            System.out.println();
        }
    }

    //Find max
    public double szukajMax(double [][] T) {
        
        double Max = T[0][0];

        for(int i = 0; i < T.length; i++) {

            for(int j=0; j<T[i].length; j++) {

                if (T[i][j] > Max) {

                    Max = T[i][j];
                } 
            }
        }

        return Max;
    }

    public void fillMatrix(double[][] matrix) {
    }
}