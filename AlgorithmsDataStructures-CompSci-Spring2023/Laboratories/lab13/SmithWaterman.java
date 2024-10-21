public class SmithWaterman {

    // https://rna.informatik.uni-freiburg.de/Teaching/index.jsp?toolName=Smith-Waterman

    static int[][] matrix;

    public static void main(String[] args) {
        String seq1 = "AGACTACT";
        String seq2 = "TACATAGTA";
        int matchScore = 1;
        int mismatchPenalty = -1;
        int gapPenalty = -1;

        String[] alignment = smithWaterman(seq1, seq2, matchScore, mismatchPenalty, gapPenalty);
        String align1 = alignment[0];
        String align2 = alignment[1];
        String path = alignment[2];
        int score = Integer.parseInt(alignment[3]);

        System.out.println("Alignment:");
        System.out.println(align1);
        System.out.println(align2);
        System.out.println("\nScore: " + score);
        System.out.println("Path: " + path);

        displayMatrix(seq1, seq2, align1, align2);

        // Additional Testing Cases
        String seq3 = "TACGGGCCCGCTAC";
        String seq4 = "TAGCCCTATCGGTCA";
        alignment = smithWaterman(seq3, seq4, matchScore, mismatchPenalty, gapPenalty);
        align1 = alignment[0];
        align2 = alignment[1];
        path = alignment[2];
        score = Integer.parseInt(alignment[3]);

        System.out.println("Alignment:");
        System.out.println(align1);
        System.out.println(align2);
        System.out.println("\nScore: " + score);
        System.out.println("Path: " + path);

        displayMatrix(seq3, seq4, align1, align2);

        // Additional Testing Cases
        gapPenalty = 0;

        String seq5 = "TACGGGCCCGCTAC";
        String seq6 = "TAGCCCTATCGGTCA";
        alignment = smithWaterman(seq5, seq6, matchScore, mismatchPenalty, gapPenalty);
        align1 = alignment[0];
        align2 = alignment[1];
        path = alignment[2];
        score = Integer.parseInt(alignment[3]);

        System.out.println("Alignment:");
        System.out.println(align1);
        System.out.println(align2);
        System.out.println("\nScore: " + score);
        System.out.println("Path: " + path);

        displayMatrix(seq5, seq6, align1, align2);
    }

    public static String[] smithWaterman(String seq1, String seq2, int matchScore, int mismatchPenalty,
            int gapPenalty) {
        // Initialize the scoring matrix
        matrix = new int[seq1.length() + 1][seq2.length() + 1];

        // Fill the scoring matrix
        int maxScore = 0;
        int[] maxPos = new int[2];
        for (int i = 1; i <= seq1.length(); i++) {
            for (int j = 1; j <= seq2.length(); j++) {
                int match = matrix[i - 1][j - 1]
                        + (seq1.charAt(i - 1) == seq2.charAt(j - 1) ? matchScore : mismatchPenalty);
                int delete = matrix[i - 1][j] + gapPenalty;
                int insert = matrix[i][j - 1] + gapPenalty;
                matrix[i][j] = Math.max(0, Math.max(match, Math.max(delete, insert)));

                // Track the position of the maximum score
                if (matrix[i][j] > maxScore) {
                    maxScore = matrix[i][j];
                    maxPos[0] = i;
                    maxPos[1] = j;
                }
            }
        }

        // Traceback to find the alignment
        StringBuilder align1 = new StringBuilder();
        StringBuilder align2 = new StringBuilder();
        StringBuilder path = new StringBuilder();

        int i = maxPos[0];
        int j = maxPos[1];

        while (matrix[i][j] != 0) {
            if (matrix[i][j] == matrix[i - 1][j - 1]
                    + (seq1.charAt(i - 1) == seq2.charAt(j - 1) ? matchScore : mismatchPenalty)) {
                align1.insert(0, seq1.charAt(i - 1));
                align2.insert(0, seq2.charAt(j - 1));
                path.insert(0,
                        "(" + (i - 1) + "," + (j - 1) + ":" + seq1.charAt(i - 1) + "-" + seq2.charAt(j - 1) + ")|");
                i--;
                j--;
            } else if (matrix[i][j] == matrix[i - 1][j] + gapPenalty) {
                align1.insert(0, seq1.charAt(i - 1));
                align2.insert(0, "-");
                path.insert(0, "(" + (i - 1) + "," + j + ":" + seq1.charAt(i - 1) + "--)|");
                i--;
            } else {
                align1.insert(0, "-");
                align2.insert(0, seq2.charAt(j - 1));
                path.insert(0, "(" + i + "," + (j - 1) + ":--" + seq2.charAt(j - 1) + ")|");
                j--;
            }
        }

        return new String[] { align1.toString(), align2.toString(), path.toString(), Integer.toString(maxScore) };
    }

    public static void displayMatrix(String seq1, String seq2, String align1, String align2) {
        int rows = seq1.length() + 1;
        int cols = seq2.length() + 1;

        System.out.println("\nScoring Matrix:");
        System.out.print("     ");

        for (int j = 0; j < cols; j++) {
            if (j > 0) {
                System.out.printf("%5c", seq2.charAt(j - 1));
            } else {
                System.out.print("     ");
            }
        }
        System.out.println();

        for (int i = 0; i < rows; i++) {
            if (i > 0) {
                System.out.printf("%5c", seq1.charAt(i - 1));
            } else {
                System.out.print("      ");
            }
            for (int j = 0; j < cols; j++) {
                System.out.printf("%5d", matrix[i][j]);
            }
            System.out.println();
        }
    }
}
