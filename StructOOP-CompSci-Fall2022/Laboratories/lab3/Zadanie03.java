import java.util.Random;

public class Zadanie03{

    final static int m = 2;

    public static void main(String[] args) {
    
        double [][] Matrix = new double[m][m];

        Zadanie03 obT = new Zadanie03();

        obT.fillMatrix(Matrix);
        obT.Multiplication(Matrix);
        obT.Addition(Matrix);
    }

    //Filling the Matrix_______________________________________________
    public void fillMatrix(double [][] T) {

        Random generator = new Random();

        for(int i = 0; i < T.length; i++) {

            for(int j = 0; j < T[i].length; j++) {

                T[i][j] = generator.nextDouble() * 10;
            }
        }
    }

    //Multiplication Method_______________________________________________
    public void Multiplication(double [][] T) {

        System.out.println("\nMnozenie_________________________________\n");//new line

        //creating two matrices    
        double a[][]= T;    
        double b[][]= T;    
            
        //creating another matrix to store the multiplication of two matrices    
        double c[][]=new double[m][m];  //m rows and m columns  
            
        //multiplying and printing multiplication of 2 matrices    
        for(int i=0;i<m;i++){    

            for(int j=0;j<m;j++){   
                c[i][j]=0;      

                for(int k=0;k<m;k++){ 
                c[i][j]+=a[i][k]*b[k][j];      
                }

                System.out.print(c[i][j]+" ");  //printing matrix element  
            } 

        System.out.println();//new line    
        }  
        
        System.out.println("_________________________________\n");//new line
    }    

    //Addition Method_______________________________________________
    public void Addition(double [][] T){ 

        System.out.println("\nDodawanie_________________________________\n");//new line

        //creating two matrices    
        double a[][]=T;    
        double b[][]=T;    
            
        //creating another matrix to store the sum of two matrices    
        double c[][]=new double[m][m];  //m rows and m columns  
            
        //adding and printing addition of 2 matrices    
        for(int i=0;i<m;i++){    

            for(int j=0;j<m;j++){    
                c[i][j]=a[i][j]+b[i][j];    //use - for subtraction  
                System.out.print(c[i][j]+" ");    
            }    

            System.out.println();//new line    
        }    

        System.out.println("_________________________________\n");//new line
    }    
}