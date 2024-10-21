package logic;

import javax.swing.*;

public class Player extends GameObject {
    private boolean reloaded = true;

    public Player(int width, int height, int speed, JPanel panel) {
        super(width, height, speed, panel, "starship.png", -1);
    }

    public Bullet makeBullet(){
        if (reloaded){
            reloading();
            return super.makeBullet();
        }
        return null;
    }
    public void move(boolean left, boolean right){
        int newPositionX = getX();
        if (left)
            newPositionX -= getSpeed();
        else if (right)
            newPositionX += getSpeed();

        if (newPositionX >= 0 && newPositionX <= 545)
            setBounds(newPositionX, getY());
    }
    public boolean getReloaded(){return reloaded;}
    private void reloading(){
        reloaded = false;
        new Thread(() -> {
            try {
                Thread.sleep(700);
                reloaded = true;
            }catch (InterruptedException ignored){};
        }).start();
    }
}
