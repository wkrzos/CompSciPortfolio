// Zespół: 
// Wojciech Krzos <3
// Filip Kubecki <3
// Tymoteusz Lango <3

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.*;

public class GUI implements ActionListener {
    private JFrame frame;
    private JPanel buttonPanel, functionPanel, container;
    public static JButton[][] buttons;
    private JLabel mines;
    private final int size_x, size_y;
    private int numberOfMines;
    private boolean start = true;
    private boolean isFlagging = false;
    private final GameLogic gameLogic;

    public GUI(int size_x, int size_y, int numberOfMines){
        this.size_x = size_x;
        this.size_y = size_y;
        this.numberOfMines = numberOfMines;

        gameLogic = new GameLogic(size_x, size_y, numberOfMines);
        startgui();
    }

    private void startgui(){
        frame = new JFrame();
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);
        frame.setLayout(new BorderLayout());

        container = new JPanel();
        container.setLayout(new BorderLayout());

        functionPanel = new JPanel();
        functionPanel.setVisible(true);
        functionPanel.setLayout(new GridLayout(0, 4));

        //Ilość zaznaczonych min
        mines = new JLabel(Integer.toString(numberOfMines));
        mines.setHorizontalAlignment(JLabel.CENTER);
        functionPanel.add(mines);

        //RESET button
        JButton resetBT = new JButton("RESET");
        functionPanel.add(resetBT);

        //FLAGA button
        JButton flagBT = new JButton("🚩");
        flagBT.addActionListener(this::flagPerformed);
        functionPanel.add(flagBT);

        //Licznik czasu
        JLabel time = new JLabel("0");
        time.setHorizontalAlignment(JLabel.CENTER);
        functionPanel.add(time);

        buttonPanel = new JPanel();
        buttonPanel.setLayout(new GridLayout(size_x, size_y));

        buttons = new JButton[size_x][size_y];
        for (int i = 0; i < size_x; i++) {
            for (int j = 0; j < size_y; j++) {
                buttons[i][j] = new JButton("");
                buttons[i][j].setBackground(Color.WHITE);
                buttons[i][j].addActionListener(this::actionPerformed);
                buttonPanel.add(buttons[i][j]);
            }
        }
        container.add(buttonPanel);
        frame.setSize(500,500);
        frame.add(container, BorderLayout.CENTER);
        frame.add(functionPanel, BorderLayout.PAGE_START);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLocationRelativeTo(null);
        frame.revalidate();
        frame.repaint();
    }

    @Override
    public void actionPerformed(ActionEvent event) {
        String[] idxSplit = event.getSource().toString().substring(21).split(",60x54")[0].strip().split(",");
        int x = (Integer.parseInt(idxSplit[1]) - 2) / 54;
        int y = (Integer.parseInt(idxSplit[0]) - 3) / 60;
        System.out.println(x + " -> " + y);

        if (start){
            gameLogic.randomBoardOfMines();
            // TODO Trzeba dodać sprawdzenie czy wartość początkowa jest miną
            gameLogic.initializeBoardOfNumbers();
            start = false;
        }

        JButton currentButton = buttons[x][y];
        if (isFlagging){
            if (currentButton.getText().equals("🚩")){
                numberOfMines += 1;
                currentButton.setText("");
                currentButton.setEnabled(true);
            }else {
                currentButton.setText("🚩");
                numberOfMines -= 1;
                currentButton.setEnabled(false);
            }
            JLabel minesLB = (JLabel) functionPanel.getComponent(0);
            minesLB.setText(String.valueOf(numberOfMines));
        } else {
            currentButton.setEnabled(false);
            if (gameLogic.getIsMine(x, y)){
                currentButton.setBackground(Color.RED);
            } else {
                int cellID = gameLogic.getCellValue(x, y);
                if (cellID == 0){
                    currentButton.setBackground(Color.GRAY);
                }else {
                    currentButton.setText(String.valueOf(cellID));
                }
            }
        }
    }

    private void flagPerformed(ActionEvent event) {
        JButton flagBT = (JButton) event.getSource();
        isFlagging = !isFlagging;
        if (isFlagging)
            flagBT.setForeground(Color.RED);
        else
            flagBT.setForeground(Color.BLACK);
    }
}
