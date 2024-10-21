package logic;

import javax.swing.*;
import java.awt.*;

public class Bullet extends JLabel {
    private final int x;
    private final int speedOfTheBullet;
    private final int direction;
    private final int width = 5;
    private final int height = 40;

    public Bullet(int x, int y, int speedOfTheBullet, int direction) {
        this.x = x;
        this.speedOfTheBullet = speedOfTheBullet;
        this.direction = direction;

        this.setText("|");
        this.setForeground(Color.RED);
        this.setBounds(x, y, width, height);
    }

    public void move() {
        this.setBounds(x, getY() + (speedOfTheBullet * direction), width, height);
    }

    public int getDirection() {
        return direction;
    }
}
