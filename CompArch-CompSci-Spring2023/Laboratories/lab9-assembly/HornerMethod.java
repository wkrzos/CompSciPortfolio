public class HornerMethod {

    static double currX;
    
    public static void main(String[] args) {

        float[] coefs = {2.3f, 3.45f, 7.67f, 5.32f}; // wektory przed kolejnymi potegami x
        int degree = 3; // stopień wielomianu

        String prompt1 = "Wprowadz wartosc x: ";
        String prompt2 = "Wartosc wielomianu to: ";
        String prompt3 = " | Kontynuowac? No (0) / Yes (1) ";

        try (java.util.Scanner scanner = new java.util.Scanner(System.in)) {
            while (true) {

                System.out.print(prompt1);
                double x = scanner.nextDouble();
                currX = x;
                
                double result = hornerMethod(x, degree, coefs);

                System.out.println(prompt2 + result);

                System.out.print(prompt3);
                int choice = scanner.nextInt();

                if (choice == 0) {
                    break;
                }
            }
        }
    }

    public static double hornerMethod(double x, int degree, float[] coefs) {
        
        double result = coefs[degree];

        for (int i = degree - 1; i >= 0; i--) {
			result = result + coefs[i] * currX;
			currX = currX * x;
        }

        return result;
    }
}
