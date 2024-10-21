package gui;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.security.Key;
import java.util.ArrayList;
import java.util.List;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.SwingConstants;
import javax.swing.border.Border;

public class Settings extends JFrame {
	private static final long serialVersionUID = 1L;
	private JPanel panel;
	private JLabel title;
	private JLabel volume;
	private JLabel difficulty;
	private JLabel music;
	private JTextField volumeField;
	private JTextField difficultyField;
	private JTextField musicField;
	private JButton save;
	private JButton load;
	private JButton exit;
	private List<String> settings;
	private File file;
	private FileOutputStream fos;
	private ObjectOutputStream oos;
	private FileInputStream fis;
	private ObjectInputStream ois;

	public Settings() {
		super("Settings");
		setSize(400, 300);
		setLocationRelativeTo(null);
		setResizable(false);
		setLayout(new BorderLayout());
		setBackground(Color.WHITE);

		panel = new JPanel();
		panel.setBackground(Color.WHITE);
		panel.setLayout(new GridLayout(5, 2));
		panel.setPreferredSize(new Dimension(400, 300));

		title = new JLabel("Settings", SwingConstants.CENTER);
		title.setFont(new Font("Arial", Font.BOLD, 20));

		volume = new JLabel("Volume: ");
		difficulty = new JLabel("Difficulty: ");
		music = new JLabel("Music: ");

		volumeField = new JTextField();
		difficultyField = new JTextField();
		musicField = new JTextField();

		save = new JButton("Save");
		load = new JButton("Load");
		exit = new JButton("Close \nsettings");

		settings = new ArrayList<String>();
		file = new File("settings.txt");
		save.addActionListener(e -> saveSettings());
		load.addActionListener(e -> loadSettings());
		exit.addActionListener(e -> this.setVisible(false));

		Border border = BorderFactory.createLineBorder(Color.BLACK, 2);
		volumeField.setBorder(border);
		difficultyField.setBorder(border);
		musicField.setBorder(border);
		panel.add(volume);
		panel.add(volumeField);
		panel.add(difficulty);
		panel.add(difficultyField);
		panel.add(music);
		panel.add(musicField);
		panel.add(save);
		panel.add(load);
		panel.add(exit);
		add(title, BorderLayout.NORTH);
		add(panel, BorderLayout.CENTER);
		setVisible(false);
	}

	public void saveSettings() {
		settings.add(volumeField.getText());
		settings.add(difficultyField.getText());
		settings.add(musicField.getText());
		try {
			fos = new FileOutputStream(file);
			oos = new ObjectOutputStream(fos);
			oos.writeObject(settings);
			oos.close();
			fos.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public void loadSettings() {
		try {
			fis = new FileInputStream(file);
			ois = new ObjectInputStream(fis);
			settings = (List<String>) ois.readObject();
			ois.close();
			fis.close();
			volumeField.setText(settings.get(0));
			difficultyField.setText(settings.get(1));
			musicField.setText(settings.get(2));
		} catch (IOException | ClassNotFoundException e) {
			e.printStackTrace();
		}
	}
}
