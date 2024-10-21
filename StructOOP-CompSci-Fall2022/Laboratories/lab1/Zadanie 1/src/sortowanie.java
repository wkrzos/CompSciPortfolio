public class sortowanie {
    public static void main(String[] args){
        //wprowadź 3 liczby w postaci numerycznej, nie używaj liter
        double num01 = -7, num02 = 234, num03 = 333;
        
        double max = Math.max(num01, Math.max(num02, num03)); //szukanie największej
        double min = Math.min(num01, Math.min(num02,num03)); //szukanie najmniejszej
        double sro = num01 + num02 + num03 - max - min; //szukanie środka

        System.out.printf("W kolejności %f %f %f%n", min, sro, max);
    }
}
