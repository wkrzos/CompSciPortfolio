package gui;

import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import javax.swing.JFrame;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;

import database.ArrayListToArray;
import MainFrame;

public class MainWindow extends JFrame implements ActionListener {
    JPanel panelOne;

    JTable admStaffDisplayedJTable;
    JTable resStaffDisplayedJTable;
    JTable studentsDisplayedJTable;
    JTable coursesDisplayedJTable;

    JScrollPane scrollPaneAdmStaff;
    JScrollPane scrollPaneResStaff;
    JScrollPane scrollPaneStudents;
    JScrollPane scrollPaneCourses;

    JMenuBar menuBar;

    JMenu fileMenu;
    JMenuItem loadFile;
    JMenuItem saveFile;
    JMenuItem refresh;

    JMenu listMenu;
    JMenuItem searchListPerson;
    JMenuItem searchListCourse;
    JMenuItem displayListStudent;
    JMenuItem displayListStaff;
    JMenuItem displayListCourse;
    JMenu listSortMenu;
    JMenuItem sortByName;
    JMenuItem sortBySurnameAndName;
    JMenuItem sortBySurnameAndAge;
    JMenuItem sortByECTSAndName;

    JMenu addMenu;
    JMenuItem addAdmStaff;
    JMenuItem addResStaff;
    JMenuItem addStudent;
    JMenuItem addCourse;

    JMenu removeMenu;
    JMenuItem removeAdmStaff;
    JMenuItem removeResStaff;
    JMenuItem removeStudent;
    JMenuItem removeCourse;
    JMenuItem removeDuplicatePerson;
    JMenuItem removeDuplicateStudents;

    MainFrame mf;

    public MainWindow() {
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setSize(1500, 500);
        this.setLayout(new FlowLayout());
        mf = new MainFrame();
        createPanels();
        createJTables();
        createMenuBar();
    }

    public void createJTables() {
        ArrayListToArray alta = mf.getAlta();

        System.out.println("masd");

        admStaffDisplayedJTable = new JTable(alta.getArrayOfAdmStaff());
        resStaffDisplayedJTable = new JTable(alta.getArrayOfResStaff());
        studentsDisplayedJTable = new JTable(alta.getArrayOfStudents());
        coursesDisplayedJTable = new JTable(alta.getArrayOfCourses());

        scrollPaneAdmStaff = new JScrollPane(admStaffDisplayedJTable);
        scrollPaneResStaff = new JScrollPane(resStaffDisplayedJTable);
        scrollPaneStudents = new JScrollPane(studentsDisplayedJTable);
        scrollPaneCourses = new JScrollPane(coursesDisplayedJTable);

        boolean setFillsViewportHeight = false;
        admStaffDisplayedJTable.setFillsViewportHeight(setFillsViewportHeight);
        resStaffDisplayedJTable.setFillsViewportHeight(setFillsViewportHeight);
        studentsDisplayedJTable.setFillsViewportHeight(setFillsViewportHeight);
        coursesDisplayedJTable.setFillsViewportHeight(setFillsViewportHeight);

        //Test


        //===

        scrollPaneAdmStaff.setVisible(true);
        scrollPaneResStaff.setVisible(true);
        scrollPaneStudents.setVisible(false);
        scrollPaneCourses.setVisible(false);

        panelOne.add(scrollPaneAdmStaff);
        panelOne.add(scrollPaneResStaff);
        panelOne.add(scrollPaneStudents);
        panelOne.add(scrollPaneCourses);
    }

    public void createPanels() {
        panelOne = new JPanel();
        panelOne.setLayout(new FlowLayout());
        this.add(panelOne);
    }

    public void createMenuBar() {
        menuBar = new JMenuBar();

        fileMenu = new JMenu("File");
        listMenu = new JMenu("List");
        listSortMenu = new JMenu("sort");
        addMenu = new JMenu("Add");
        removeMenu = new JMenu("Remove");

        menuBar.add(fileMenu);
        menuBar.add(listMenu);
        menuBar.add(addMenu);
        menuBar.add(removeMenu);

        loadFile = new JMenuItem("load");
        saveFile = new JMenuItem("save");
        refresh = new JMenuItem("refresh");

        searchListPerson = new JMenuItem("search person");
        searchListCourse = new JMenuItem("search course");
        displayListStudent = new JMenuItem("display students");
        displayListStaff = new JMenuItem("display staff");
        displayListCourse = new JMenuItem("display course");
        sortByName = new JMenuItem("person by name");
        sortBySurnameAndName = new JMenuItem("person by surname and name");
        sortBySurnameAndAge = new JMenuItem("person by surname and age");
        sortByECTSAndName = new JMenuItem("courses by ECTS and name of lecturer");

        addAdmStaff = new JMenuItem("administration staff");
        addResStaff = new JMenuItem("research staff");
        addStudent = new JMenuItem("student");
        addCourse = new JMenuItem("course");

        removeAdmStaff = new JMenuItem("administration staff");
        removeResStaff = new JMenuItem("research staff");
        removeStudent = new JMenuItem("student");
        removeCourse = new JMenuItem("course");
        removeDuplicatePerson = new JMenuItem("staff duplicate");
        removeDuplicateStudents = new JMenuItem("student duplicate");

        loadFile.addActionListener(this);
        saveFile.addActionListener(this);
        refresh.addActionListener(this);

        searchListPerson.addActionListener(this);
        searchListCourse.addActionListener(this);
        displayListStudent.addActionListener(this);
        displayListStaff.addActionListener(this);
        displayListCourse.addActionListener(this);
        sortByName.addActionListener(this);
        sortBySurnameAndName.addActionListener(this);
        sortBySurnameAndAge.addActionListener(this);
        sortByECTSAndName.addActionListener(this);

        addAdmStaff.addActionListener(this);
        addResStaff.addActionListener(this);
        addStudent.addActionListener(this);
        addCourse.addActionListener(this);

        removeAdmStaff.addActionListener(this);
        removeResStaff.addActionListener(this);
        removeStudent.addActionListener(this);
        removeCourse.addActionListener(this);
        removeDuplicatePerson.addActionListener(this);
        removeDuplicateStudents.addActionListener(this);

        fileMenu.setMnemonic(KeyEvent.VK_F); // Alt + f
        loadFile.setMnemonic(KeyEvent.VK_L); // l for load
        saveFile.setMnemonic(KeyEvent.VK_S); // s for save

        fileMenu.add(loadFile);
        fileMenu.add(saveFile);
        fileMenu.add(refresh);

        listMenu.add(searchListPerson);
        listMenu.add(searchListCourse);
        listMenu.add(displayListStudent);
        listMenu.add(displayListStaff);
        listMenu.add(displayListCourse);
        listMenu.add(listSortMenu);
        listSortMenu.add(sortByName);
        listSortMenu.add(sortBySurnameAndName);
        listSortMenu.add(sortBySurnameAndAge);
        listSortMenu.add(sortByECTSAndName);

        addMenu.add(addAdmStaff);
        addMenu.add(addResStaff);
        addMenu.add(addStudent);
        addMenu.add(addCourse);

        removeMenu.add(removeAdmStaff);
        removeMenu.add(removeResStaff);
        removeMenu.add(removeStudent);
        removeMenu.add(removeCourse);
        removeMenu.add(removeDuplicatePerson);
        removeMenu.add(removeDuplicateStudents);

        this.setJMenuBar(menuBar);
        this.setVisible(true);
    }

    public void refreshGUI() {
        this.repaint();
        this.revalidate();
        panelOne.repaint();
        panelOne.revalidate();
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        // File menu
        if (e.getSource() == loadFile) {
            mf.readPersonFile();
            JOptionPane.showMessageDialog(this, "File loaded!");
        }
        if (e.getSource() == saveFile) {
            mf.savePersonToFile();
            JOptionPane.showMessageDialog(this, "File saved!");
        }
        if (e.getSource() == refresh) {
            refreshGUI();
            JOptionPane.showMessageDialog(this, "GUI refreshed.");
        }

        // List menu
        if (e.getSource() == searchListPerson) {
            mf.searchPersons();
        }
        if (e.getSource() == searchListCourse) {
            mf.searchCourse();
        }
        if (e.getSource() == displayListStudent) {
            mf.displayStudents();
            scrollPaneAdmStaff.setVisible(false);
            scrollPaneResStaff.setVisible(false);
            scrollPaneStudents.setVisible(true);
            scrollPaneCourses.setVisible(false);
            refreshGUI();
        }
        if (e.getSource() == displayListStaff) {
            mf.displayStaff();
            scrollPaneAdmStaff.setVisible(true);
            scrollPaneResStaff.setVisible(true);
            scrollPaneStudents.setVisible(false);
            scrollPaneCourses.setVisible(false);
            refreshGUI();
        }
        if (e.getSource() == displayListCourse) {
            mf.displayCourses();
            scrollPaneAdmStaff.setVisible(false);
            scrollPaneResStaff.setVisible(false);
            scrollPaneStudents.setVisible(false);
            scrollPaneCourses.setVisible(true);
            refreshGUI();
        }
        if (e.getSource() == sortByName) {
            mf.sortByName();
            JOptionPane.showMessageDialog(this, "Sorted!");
        }
        if (e.getSource() == sortBySurnameAndName) {
            mf.sortBySurnameAndName();
            JOptionPane.showMessageDialog(this, "Sorted!");
        }
        if (e.getSource() == sortBySurnameAndAge) {
            mf.sortBySurnameAndAge();
            JOptionPane.showMessageDialog(this, "Sorted!");
        }
        if (e.getSource() == sortByECTSAndName) {
            mf.sortByECTSAndSurname();
            JOptionPane.showMessageDialog(this, "Sorted!");
        }

        // Add menu
        if (e.getSource() == addAdmStaff) {
            mf.addAdmStaff();
            JOptionPane.showMessageDialog(this, "Administration staff added!");
        }
        if (e.getSource() == addResStaff) {
            mf.addResStaff();
            JOptionPane.showMessageDialog(this, "Research staff added!");
        }
        if (e.getSource() == addStudent) {
            mf.addStudent();
            JOptionPane.showMessageDialog(this, "Student added!");
        }
        if (e.getSource() == addCourse) {
            mf.addCourse();
            JOptionPane.showMessageDialog(this, "Course added!");
        }

        // Remove menu
        if (e.getSource() == removeAdmStaff) {
            mf.removePersonFromArrayList();
            JOptionPane.showMessageDialog(this, "Person removed.");
        }
        if (e.getSource() == removeResStaff) {
            mf.removePersonFromArrayList();
            JOptionPane.showMessageDialog(this, "Person removed.");
        }
        if (e.getSource() == removeStudent) {
            mf.removePersonFromArrayList();
            JOptionPane.showMessageDialog(this, "Person removed.");
        }
        if (e.getSource() == removeCourse) {
            mf.removeCourseFromArrayList();
            JOptionPane.showMessageDialog(this, "Course removed.");
        }
        if (e.getSource() == removeDuplicatePerson) {
            mf.createHashSet();
            JOptionPane.showMessageDialog(this, "Staff duplicates removed.");
            refreshGUI();
        }
        if (e.getSource() == removeDuplicateStudents) {
            mf.createHashSet();
            JOptionPane.showMessageDialog(this, "Student duplicates removed.");
            refreshGUI();
        }
    }
}