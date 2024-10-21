import javax.swing.SwingUtilities;

import gui.MainWindow;

public class Main {

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                // new ArrayListToArray();
                // new MainFrame();
                new MainWindow().setVisible(true);
            }
        });
    }
}
