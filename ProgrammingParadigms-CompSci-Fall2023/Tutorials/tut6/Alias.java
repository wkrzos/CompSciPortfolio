package tut6;

public class Alias{
    public static void main(String[] args){
        int[] ints = {1,2,3};
        for(int i : ints) {
            System.out.println(i);
            i = 0;
        }
        for(int i : ints) System.out.println(i);
        
        int[] ints2 = ints;
        for(int i=0; i<ints2.length; i++) {
            System.out.println(ints2[i]);
            ints2[i] = -1;
        }
        for(int i : ints) System.out.println(i);
    }
}

