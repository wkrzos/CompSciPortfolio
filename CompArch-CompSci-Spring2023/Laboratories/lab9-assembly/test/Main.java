import java.util.Scanner;
import java.util.Locale;
import java.util.InputMismatchException;

public class Main { 
	static float[] coefs = new float[]{2.3f, 3.45f, 7.67f, 5.32f};
	static int degree = 3;
	static String enter_number_msg = "Please enter a number: ";
    static String result_msg = "Result: ";
    static String continue_msg = "\nDo you want to continue? (y) ";
	static Scanner scanner = new Scanner(System.in).useLocale(Locale.US);
	
	public static void main(String[] args) {
		System.out.print(enter_number_msg);
		double x = scanner.nextDouble();
		double value = evalPoly(coefs, degree, x);
		System.out.print(result_msg + value);
		System.out.print(continue_msg);
		int c = scanner.next().charAt(0); 
		if (c == 'y' || c == 'Y') {
			System.out.println();
			main(args);
		}
	}
	
	private static double evalPoly(float[] coefs, int degree, double x) {
		double result = coefs[degree];
		double currentX = x;
		int i = degree - 1;
		for (; i >= 0; i--) {
			result = result + coefs[i] * currentX;
			currentX = currentX * x;
		}
		return result;
	}
}
