package logic;

import javax.swing.*;

public class Enemy extends GameObject {
    public Enemy(int width, int height, int speed, JPanel panel, String src) {
        super(width, height, speed, panel, src, 1);
    }
}