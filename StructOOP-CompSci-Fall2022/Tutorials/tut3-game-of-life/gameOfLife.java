import java.util.Random;
import java.io.IOException;

public class gameOfLife {
    final private int x; //height of board
    final private int y; //width of board

    final private boolean[][] board;
    private static int waitFor;

    public gameOfLife(int x, int y){
        this.x = x;
        this.y = y;
        this.board = new boolean[x][y];

        fillWithRand();
    }

    // Dopóki nie stworzymy inputu urzytkownika nie ma co tej funkcji inicjalizować
    private boolean[][] createEmpty(){
        for (int i = 0; i < x; i++) {
            for (int j = 0; j < y; j++) {
                board[i][j] = false;
            }
        }
        return board;
    }

    private void fillWithRand(){
        Random random = new Random();
        for (int i = 0; i < x; i++) {
            for (int j = 0; j < y; j++) {
                board[i][j] = random.nextBoolean();
            }
        }
    }

    //Add clearing console
    public void writeDown(){
        for (int i = 0; i <= y; i++) {
            System.out.print("--");
        }
        System.out.println();
        for (int i = 0; i < x; i++) {
            System.out.print("|");
            for (int j = 0; j < y; j++) {
                if (board[i][j]) System.out.print("■ ");
                else System.out.print("  ");
            }
            System.out.print("|");
            System.out.println();
        }

        for (int i = 0; i <= y; i++) {
            System.out.print("--");
        }
    }

    private int howManyLive(int x1, int y1){
        int suma = 0;
        for (int i = -1; i < 2; i++) {
            for (int j = -1; j < 2; j++) {
                if (j != 0 || i != 0){
                    int x = x1;
                    int y = y1;
                    if (x1+i == -1) x = (board.length);
                    else if(x1+i == board.length) x = -1;

                    if (y1+j == -1) y = (board[0].length);
                    else if(y1+j == board[0].length) y = -1;

                    if (board[x + i][y + j]) suma++;
                }
            }
        }
        return suma;
    }

    public void startGame(){
        boolean[][] future_board = new boolean[x][y];
        for (int i = 0; i < x; i++) {
            for (int j = 0; j < y; j++) {
                int num_of_alive = howManyLive(i, j);
                if (board[i][j]){
                    future_board[i][j] = num_of_alive == 2 || num_of_alive == 3;
                }else {
                    future_board[i][j] = num_of_alive == 3;
                }
            }
        }
        changeArray(future_board);
        writeDown();
    }

    private void changeArray(boolean[][] future_board){
        for (int i = 0; i < x - 1; i++) {
            for (int j = 0; j < y - 1; j++) {
                board[i][j] = future_board[i][j];
            }
        }
    }

    // Jeśli tablica jest pusta to kończy grę
    public boolean is_not_Empty(){
        boolean[][] empty_board = new boolean[x][y];
        if (board == empty_board) return false;
        return true;
    }

    //Clearing the console
    public void clearConsole() throws IOException, InterruptedException {
        waitFor = new ProcessBuilder("cmd", "/c", "cls").inheritIO().start().waitFor();
    }
}
