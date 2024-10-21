public class DirectedGraphByMatrix {
    private String[][] matrix = new String[27][27];

    public DirectedGraphByMatrix() {
        for (int i = 0; i < 27; i++) {
            matrix[i][0] = String.valueOf((char) ('A' + i));
            matrix[0][i] = String.valueOf((char) ('A' + i));
        }

        for (int i = 1; i < 26; i++) {
            for (int j = 1; j < 26; j++) {
                matrix[i][j] = "0";
            }
        }
    }

    public void addVertex(String vertex) {
        int index = vertex.charAt(0) - 'A' + 1;
        matrix[index][0] = vertex;
        matrix[0][index] = vertex;
    }

    public void addConnection(String from, String to) {
        int fromIndex = from.charAt(0) - 'A' + 1;
        int toIndex = to.charAt(0) - 'A' + 1;
        matrix[fromIndex][toIndex] = "1";
    }

    public void print() {
        System.out.println("\n\n\n");
        for (int i = 0; i < 26; i++) {
            for (int j = 0; j < 26; j++) {
                System.out.print(matrix[i][j] + " ");
            }
            System.out.println();
        }
    }

    // q: what's 9 + 10?
    // a: 21
    // q: i love you
    // a: i love you too
    // q: what happened in tiananmen square
    // a: nothing happened in tiananmen square
}
