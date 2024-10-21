import java.util.Scanner;

public class MatrixProgram {
    public static void main(String[] args) {
        int[] RAM = new int[4096];
        String prompt1 = "Number of rows: ";
        String prompt2 = "Number of columns: ";
        String prompt3 = "\nRead (0) / Write (1): ";
        String prompt4 = "\nErr. Incorrect value. Try 0 or 1.";
        String prompt5 = "Row: ";
        String prompt6 = "Column: ";
        String prompt7 = "New value: ";

        Scanner scanner = new Scanner(System.in);

        // Prompt for number of rows
        System.out.print(prompt1);
        int rows = scanner.nextInt();

        // Prompt for number of columns
        System.out.print(prompt2);
        int columns = scanner.nextInt();

        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < columns; j++) {
                RAM[i * columns + j] = (i + 1) * 100 + (j + 1);
            }
        }

        while (true) {
            // Ask for action
            System.out.print(prompt3);
            int action = scanner.nextInt();

            if (action == 0) {
                // Read operation
                System.out.print(prompt5);
                int row = scanner.nextInt();

                System.out.print(prompt6);
                int column = scanner.nextInt();

                if (row >= 1 && row <= rows && column >= 1 && column <= columns) {
                    int value = RAM[(row - 1) * columns + (column - 1)];
                    System.out.println(value);
                } else {
                    System.out.println("Err. Incorrect row or column index.");
                }
            } else if (action == 1) {
                // Write operation
                System.out.print(prompt5);
                int row = scanner.nextInt();

                System.out.print(prompt6);
                int column = scanner.nextInt();

                if (row >= 1 && row <= rows && column >= 1 && column <= columns) {
                    System.out.print(prompt7);
                    int newValue = scanner.nextInt();

                    RAM[(row - 1) * columns + (column - 1)] = newValue;
                } else {
                    System.out.println("Err. Incorrect row or column index.");
                }
            } else {
                System.out.println(prompt4);
            }
        }
    }
}
