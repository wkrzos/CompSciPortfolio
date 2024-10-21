package gui;

import logic.*;
import javax.swing.*;
import java.awt.*;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.io.File;
import java.util.ArrayList;
import java.util.Random;

public class GUI extends JFrame {
    private final JPanel panel;
    private final Player player;
    private Settings settingsWindow;
    private final ArrayList<Bullet> bullets = new ArrayList<>();
    private final ArrayList<Enemy> enemies = new ArrayList<>();
    private int direction;
    private int indirectTime = 0;
    private boolean left = false;
    private boolean right = false;
    private boolean isGameRunning = true;
    private Music musicPlayer;

    public GUI() {
        this.setTitle("Space Invaders");
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setSize(600,600);
        this.setResizable(false);
        this.setLocationRelativeTo(null);

        // Main panel
        panel = new JPanel();
        panel.setLayout(null);
        panel.setBackground(Color.BLACK);
        panel.setVisible(true);
        this.add(panel);

        // Settings
        settingsWindow = new Settings();
        settingsWindow.setVisible(false);

        //Music
        musicPlayer = new Music("space.invaders\\sfx\\BITsy.wav");
        musicPlayer.play();

        // Player
        player = new Player(40, 40, 5, panel);
        player.setBounds(280, 470);
        panel.add(player);

        // Enemies
        String[] names = {"enemy.png", "enemyBlue.png", "enemyLightBlue.png", "enemyPurpul.png", "enemyRed.png"};
        int y_enemy = 50;
        for (int i = 0; i < 5; i++){
            int x_enemy = 0;
            for (int j = 0; j < 11; j++) {
                Enemy enemy = new Enemy(30,22,1, panel, names[i]);
                enemy.setBounds(x_enemy, y_enemy);
                enemies.add(enemy);
                panel.add(enemy);
                x_enemy += enemy.getWidth() * 1.5;
            }
            y_enemy += 50;
        }
        direction = -1 * enemies.get(0).getSpeed();

        // Timer
        GameTimer gameTimer = new GameTimer();
        this.add(gameTimer.getTimeLabel(), BorderLayout.NORTH);

        //Font
        try {
            Font pixeloidSansFont = Font.createFont(Font.TRUETYPE_FONT, new File("space.invaders\\Fonts\\pixeloidSans.ttf")).deriveFont(30f);
            Font sevenSegmentsFont = Font.createFont(Font.TRUETYPE_FONT, new File("space.invaders\\Fonts\\sevenSegment.ttf")).deriveFont(30f);
            GraphicsEnvironment ge = GraphicsEnvironment.getLocalGraphicsEnvironment();
            ge.registerFont(pixeloidSansFont);
            ge.registerFont(sevenSegmentsFont);
            gameTimer.getTimeLabel().setFont(sevenSegmentsFont);
        } catch (Exception e) {e.printStackTrace();}

        this.addKeyListener(new KeyListener() {
            @Override
            public void keyTyped(KeyEvent e) {}
            @Override
            public void keyReleased(KeyEvent e) {
                if (e.getKeyCode() == KeyEvent.VK_LEFT || e.getKeyCode() == KeyEvent.VK_A) left = false;
                if (e.getKeyCode() == KeyEvent.VK_RIGHT || e.getKeyCode() == KeyEvent.VK_D) right = false;
            }
            @Override
            public void keyPressed(KeyEvent e) {
                if (isGameRunning){
                    if (e.getKeyCode() == KeyEvent.VK_LEFT || e.getKeyCode() == KeyEvent.VK_A) left = true;
                    if (e.getKeyCode() == KeyEvent.VK_RIGHT || e.getKeyCode() == KeyEvent.VK_D) right = true;

                    if (e.getKeyCode() == KeyEvent.VK_SPACE && player.getReloaded()){
                        bullets.add(player.makeBullet());
                    }

                    if (e.getKeyCode() == KeyEvent.VK_ESCAPE){settingsWindow.setVisible(true);}
                }
            }
        });

        new Thread(() -> {
            try {
                while (isGameRunning) {
                    System.out.println(settingsWindow.isVisible());
                    if (!settingsWindow.isVisible()){
                        player.move(left, right);
                        enemyMove();
                        removeBulletOnBorder();
                        enemyShot((int) (System.currentTimeMillis() - gameTimer.getStartTime()));
                        playerHit();

                        for (int i = 0; i < enemies.size(); i++) {
                            enemyHit(enemies.get(i));
                        }

                        winConditions();
                        panel.revalidate();
                        panel.repaint();
                        Thread.sleep(20);
                    }
                }
            } catch (Exception ex) {
                ex.printStackTrace();
                System.exit(0);
            }
        }).start();
        setVisible(true);
    }
    private void enemyHit(Enemy enemy){
        for (int i = 0; i < bullets.size(); i++) {
            Bullet bullet = bullets.get(i);
            if (bullet.getDirection() == -1 && enemy.isHit(bullet)){
                enemies.remove(enemy);
                bullets.remove(bullet);
            }
        }
    }
    private void playerHit(){
        for (int i = 0; i < bullets.size(); i++) {
            Bullet bullet = bullets.get(i);
            if (bullet.getDirection() == 1 && player.isHit(bullet)){
                isGameRunning = false;
                musicPlayer.stop();
            }
        }
    }

    private void enemyMove(){
        if (enemies.size() != 0){
            int positionLeft = enemies.get(0).getX();
            int positionRight = enemies.get(enemies.size()-1).getX();

            for (int i = 0; i < enemies.size(); i++){
                if (positionLeft > enemies.get(i).getX()){ positionLeft = enemies.get(i).getX();}
                if (positionRight < enemies.get(i).getX()) { positionRight = enemies.get(i).getX();}
            }

            if (positionLeft <= 0){
                direction = enemies.get(0).getSpeed();
            }else if(positionRight >= this.getWidth() - (enemies.get(0).getWidth() * 1.5)){
                direction = -1 * enemies.get(0).getSpeed();
            }

            for (Enemy enemy : enemies) {
                enemy.setBounds(enemy.getX() + direction, enemy.getY());
            }
        }
    }
    private void enemyShot(int shootDelay){
        if ((shootDelay - indirectTime) > 200){
            int chooseShootingEnemy = 0;
            if (enemies.size() > 1)
                chooseShootingEnemy = new Random().nextInt(enemies.size() - 1);

            bullets.add(enemies.get(chooseShootingEnemy).makeBullet());
            indirectTime += (shootDelay - indirectTime);
        }
    }

    private void removeBulletOnBorder() {
        for (int i = 0; i < bullets.size(); i++) {
            bullets.get(i).move();
            if (!(panel.getBounds().intersects(bullets.get(i).getBounds()))) {
                panel.remove(bullets.get(i));
                bullets.remove(bullets.get(i));
            }
        }
    }
    private void winConditions() {
        if (!isGameRunning){
            JLabel label = new JLabel("YOU LOST...");
            label.setFont(new Font( "pixeloidSansFont", Font.BOLD, 22));
            JOptionPane.showMessageDialog(null,label,"NOOB",JOptionPane.WARNING_MESSAGE);

            this.setVisible(false);
            this.dispose();
            new GUI();
        } else if (enemies.size() == 0) {
            JLabel label = new JLabel("YOU WON!");
            label.setFont(new Font("pixeloidSansFont", Font.BOLD, 22));
            JOptionPane.showMessageDialog(null, label, "PRO", JOptionPane.WARNING_MESSAGE);
            this.dispose();
            isGameRunning = false;
        }
    }
}
