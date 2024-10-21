package gui;

import java.io.File;
import java.io.IOException;
import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.Clip;
import javax.sound.sampled.LineUnavailableException;
import javax.sound.sampled.UnsupportedAudioFileException;

public class Music {
    private Clip clip;
    private String filePath;

    public Music(String filePath) {
        this.filePath = filePath;
    }

    public void play() {
        try {
            File file = new File(filePath);
            if (file.exists()) {
                AudioInputStream sound = AudioSystem.getAudioInputStream(file);
                clip = AudioSystem.getClip();
                clip.open(sound);
                clip.start();
            } else {
                throw new RuntimeException("Sound: file not found: " + filePath);
            }
        } catch (UnsupportedAudioFileException | IOException | LineUnavailableException e) {
            e.printStackTrace();
        }
    }

    public void stop() {
        if (clip.isRunning())
            clip.stop();
    }

    public void loop() {
        try {
            File file = new File(filePath);
            if (file.exists()) {
                AudioInputStream sound = AudioSystem.getAudioInputStream(file);
                clip = AudioSystem.getClip();
                clip.open(sound);
                clip.loop(Clip.LOOP_CONTINUOUSLY);
            } else {
                throw new RuntimeException("Sound: file not found: " + filePath);
            }
        } catch (UnsupportedAudioFileException | IOException | LineUnavailableException e) {
            e.printStackTrace();
        }
    }

    public void resume() {
        if (clip != null)
            clip.start();
    }

    public void reset() {
        clip.setFramePosition(0);
    }
}
