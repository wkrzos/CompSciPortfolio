package logic;

import javax.swing.*;
import java.awt.*;
import java.text.SimpleDateFormat;
import java.util.Timer;
import java.util.TimerTask;

public class GameTimer extends TimerTask {
    private final JLabel timeLabel;
    private final long startTime = System.currentTimeMillis();

    public GameTimer() {
        timeLabel = new JLabel();
        timeLabel.setForeground(Color.GREEN);
        timeLabel.setOpaque(true);
        timeLabel.setBackground(Color.black);
        timeLabel.setHorizontalAlignment(SwingConstants.CENTER);
        timeLabel.setVerticalAlignment(SwingConstants.CENTER);
        timeLabel.setFont(new Font("Arial", Font.BOLD, 20));
        timeLabel.setBounds(0, 350, 100, 50);

        java.util.Timer timer = new Timer();
        timer.schedule(this, 0, 1000);
    }

    @Override
    public void run() {
        SwingUtilities.invokeLater(() -> {
            long elapsedTime = System.currentTimeMillis() - startTime;
            timeLabel.setText(new SimpleDateFormat("mm:ss").format(elapsedTime));
        });
    }
    public long getStartTime() {
        return startTime;
    }
    public JLabel getTimeLabel() {
        return timeLabel;
    }
}