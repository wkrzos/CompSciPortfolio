package logic;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.io.File;
import java.io.IOException;

public abstract class GameObject extends JLabel {
    private final int speed, direction;
    private final int bulletSpeed = 5;
    private final int width, height;
    private final JPanel panel;

    public GameObject(int width, int height, int speed, JPanel panel, String src, int direction) {
        this.width = width;
        this.height = height;
        this.speed = speed;
        this.panel = panel;
        this.direction = direction;
        setIcon(setImageIcon(src));
    }

    public Bullet makeBullet() {
        Bullet bullet = new Bullet(getX() + (width / 2) - 1, getY() + direction * height / 2, bulletSpeed, direction);
        panel.add(bullet);
        return bullet;
    }

    public boolean isHit(Bullet bullet) {
        Rectangle r1 = this.getBounds();
        Rectangle r2 = bullet.getBounds();
        if (r1.intersects(r2)) {
            panel.remove(bullet);
            panel.remove(this);
        }
        return r1.intersects(r2);
    }

    @Override
    public int getWidth() {
        return width;
    }

    public int getSpeed() {
        return speed;
    }

    public void setBounds(int positionX, int positionY) {
        super.setBounds(positionX, positionY, width, height);
    }

    private ImageIcon setImageIcon(String src) {
        try {
            Image img = ImageIO.read(new File("space.invaders\\graphic\\" + src));
            return new ImageIcon(img.getScaledInstance(width, height, 1));
        } catch (IOException e) {
            System.out.println("Image not found!");
        }
        return null;
    }
}
