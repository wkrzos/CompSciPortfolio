import database.ArrayListToArray;
import database.objects.AdmStaff;
import database.objects.GenStaff;
import database.objects.Person;
import database.objects.ResStaff;
import database.objects.Student;
import database.objects.Course;


import javax.swing.*;
import javax.swing.table.DefaultTableModel;

import java.util.*;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;

public class MainFrame extends JFrame {

    // ArrayList for people
    protected ArrayList<Person> arrayPersons = new ArrayList<Person>();
    protected JList<Person> jListArrayPersons = new JList<Person>(
            arrayPersons.toArray(new Person[arrayPersons.size()]));
    protected ArrayListToArray alta;

    // ArrayList for courses
    protected ArrayList<Course> arrayCourses = new ArrayList<>();
    protected JList<Course> jlistCourses = new JList<Course>(arrayCourses.toArray(new Course[arrayCourses.size()]));

    private ArrayList<Student> participantsAnalizaMatematyczna01;
    private ResStaff resStaff01;
    private AdmStaff admStaff01;
    private Student student01;
    private Student student02;

    HashSet<Person> personHashSet = new HashSet<>();

    /** Initialising Main Frame */
    public MainFrame() {
        createArrays();
        alta = new ArrayListToArray(this);
        alta.arrayListToArray();
        alta.arrayListToArrayCourse();
    }

    public ArrayListToArray getAlta() {
        return alta;
    }

    public void createHashSet() {
        personHashSet.clear();
        personHashSet.addAll(arrayPersons);
        arrayPersons.clear();
        arrayPersons.addAll(personHashSet);

        findDuplicates(arrayPersons);

        alta.arrayListToArray();
    }


    public void findDuplicates(ArrayList<Person> input) {
        Set<Person> duplicates = new HashSet<Person>();

        ArrayList<Integer> indexes = new ArrayList<Integer>();

        for (int i = 0; i < input.size(); i++) {
            for (int j = 1; j < input.size(); j++) {
                if (input.get(i) instanceof GenStaff && input.get(j) instanceof GenStaff){
                    if (input.get(i).getPesel() == input.get(j).getPesel() && i != j) {
                        // duplicate element found
                        duplicates.add(input.get(i));
                        indexes.add(i);
                        indexes.add(j);
                        
                        arrayPersons.remove(i);
                        arrayPersons.remove(j);

                        alta.arrayListToArray();
                        break;
                    }
                } else if (input.get(i) instanceof Student && input.get(j) instanceof Student) {
                    if (((Student) input.get(i)).getNumIndex() == ((Student) input.get(j)).getNumIndex() && i != j) {
                        // duplicate element found
                        duplicates.add(input.get(i));
                        indexes.add(i);
                        indexes.add(j);
                        
                        arrayPersons.remove(i);
                        arrayPersons.remove(j);

                        alta.arrayListToArray();
                        break;
                    }
                } else if (input.get(i) instanceof Student && input.get(j) instanceof GenStaff || input.get(i) instanceof GenStaff && input.get(j) instanceof Student){
                    System.out.println("GenStaff and Student");
                }
            }
        }
    }


    /** Creating the array and adding components to it */
    public void createArrays() {

        // Creating Person entries
        admStaff01 = new AdmStaff("Maciej", "Kalikoli", "11111111111", 34, true, "Nonbinary", 12, 70000, 2, 3);
        resStaff01 = new ResStaff("Helga", "Kalikoli", "11111111111", 57, false, "Genderfluid", 24, 130000, 5,
                45);
        student01 = new Student("Wojciech", "Krzos", "11111111111", 19, true, "Male", null, 276264, 1, null,
                false, true, false, true, false);
        student02 = new Student("Karol", "Powsinoga", "11111111111", 21, true, "Male", null, 276255, 2, null,
                false, true, false, true, false);

        // Adding Persons to the Person array
        arrayPersons.add(admStaff01);
        arrayPersons.add(resStaff01);
        arrayPersons.add(student01);
        arrayPersons.add(student02);

        // Creating array of student for Analiza Matematyczna
        participantsAnalizaMatematyczna01 = new ArrayList<>();
        ArrayList<Student> participantsLogikaDlaInformatykow01 = new ArrayList<>();

        // Adding students
        participantsAnalizaMatematyczna01.add(student01);
        participantsAnalizaMatematyczna01.add(student02);

        participantsLogikaDlaInformatykow01.add(student01);

        // Creating course
        Course analizaMatematyczna01 = new Course(participantsAnalizaMatematyczna01, "Analiza Matematyczna", resStaff01,
                15);
        Course logikaDlaInformatykow01 = new Course(participantsLogikaDlaInformatykow01, "Logika dla Informatyków",
                resStaff01, 10);

        // Adding Courses to ArrayList of all courses
        arrayCourses.add(analizaMatematyczna01);
        arrayCourses.add(logikaDlaInformatykow01);
    }

    /** Display Students */
    public void displayStudents() {
        for (int i = 0; i < arrayPersons.size(); i++) {
            if (arrayPersons.get(i) instanceof Student) {
                arrayPersons.get(i).getState();
            }
        }
    }

    /** Display Staff */
    public void displayStaff() {
        for (int i = 0; i < arrayPersons.size(); i++) {
            if (arrayPersons.get(i) instanceof ResStaff) {
                arrayPersons.get(i).getState();
            }
            if (arrayPersons.get(i) instanceof AdmStaff) {
                arrayPersons.get(i).getState();
            }
        }
    }

    /** Display Courses */
    public void displayCourses() {
        for (int i = 0; i < arrayCourses.size(); i++) {
            arrayCourses.get(i).getState();
        }
    }

    /** Search for a Person class object */
    public Person searchPersons() {

        String personName = JOptionPane.showInputDialog(this, "Enter person name to search for: ");

        arrayPersons.sort((o1, o2) -> o1.getName().compareTo(o2.getName()));

        Comparator<Person> c = new Comparator<>() {
            public int compare(Person u1, Person u2) {
                return u1.getName().compareTo(u2.getName());
            }
        };

        int foundIndex = Collections.binarySearch(arrayPersons, new Student(personName, null, null, 0, false, null,
                null, 0, 0, null, false, false, false, false, false), c);

        if (foundIndex >= 0) {
            jListArrayPersons.setSelectedIndex(foundIndex);
            arrayPersons.get(foundIndex).getState();
        } else {
            JOptionPane.showMessageDialog(this, "Could not find the person " + personName);
        }

        JOptionPane.showMessageDialog(this, "The person is: " + " \n|Name: " + arrayPersons.get(foundIndex).getName()
                + " \n|Surname: " + arrayPersons.get(foundIndex).getSurname() + " \n|Pesel: "
                + arrayPersons.get(foundIndex).getPesel() + " \n|Sex: " + arrayPersons.get(foundIndex).getSex());
        return arrayPersons.get(foundIndex);
    }

    public Course searchCourse() {
        String courseName = JOptionPane.showInputDialog(this, "Enter course name to search for: ");

        arrayCourses.sort((o1, o2) -> o1.getCourseName().compareTo(o2.getCourseName()));

        Comparator<Course> c = new Comparator<>() {
            public int compare(Course u1, Course u2) {
                return u1.getCourseName().compareTo(u2.getCourseName());
            }
        };

        int foundIndex = Collections.binarySearch(arrayCourses,
                new Course(participantsAnalizaMatematyczna01, courseName, resStaff01, 0), c);

        if (foundIndex >= 0) {
            jlistCourses.setSelectedIndex(foundIndex);
            arrayCourses.get(foundIndex).getState();
        } else {
            JOptionPane.showMessageDialog(this, "Could not find the course " + courseName);
        }

        JOptionPane.showMessageDialog(this,
                "The course is: " + " \n|Name: " + arrayCourses.get(foundIndex).getCourseName() + " \n|Lecturer: "
                        + arrayCourses.get(foundIndex).getLecturer().getSurname() + " \n|ECTS: "
                        + arrayCourses.get(foundIndex).getNumECTS() + " \n|Participants: "
                        + arrayCourses.get(foundIndex).getCourseParticipants());
        return arrayCourses.get(foundIndex);
    }

    // Adding new Person class objects to arrayPersons
    /** Add a new Student to the arrayPersons */
    public void addStudent() {

        String personName = JOptionPane.showInputDialog(this, "Enter name");
        String personSurname = JOptionPane.showInputDialog(this, "Enter surname");
        String personPesel = JOptionPane.showInputDialog(this, "Enter pesel");
        String personAgeString = JOptionPane.showInputDialog(this, "Enter age");
        int personAgeInt = Integer.parseInt(personAgeString);
        String personSexString = JOptionPane.showInputDialog(this, "Enter sex (true/false)");
        boolean personSexBoolean = Boolean.parseBoolean(personSexString);
        String personGenderString = JOptionPane.showInputDialog(this, "Enter gender");

        if (personName != null) {
            arrayPersons.add(new Student(personName, personSurname, personPesel, personAgeInt, personSexBoolean,
                    personSexString, null, personAgeInt, personAgeInt, personGenderString, personSexBoolean,
                    personSexBoolean, personSexBoolean, personSexBoolean, personSexBoolean));
        }

        Object[] student = { personName, personSurname, personPesel, personAgeInt, personSexBoolean, personSexString,
                null, personAgeInt, personAgeInt, personGenderString, personSexBoolean, personSexBoolean,
                personSexBoolean, personSexBoolean, personSexBoolean };

        DefaultTableModel table = alta.getArrayOfStudents();
        table.addRow(student);
        alta.arrayListToArray();
        table.fireTableDataChanged();
        alta.setArrayOfStudents(table);
    }

    public void addAdmStaff() {

        String personName = JOptionPane.showInputDialog(this, "Enter name");
        String personSurname = JOptionPane.showInputDialog(this, "Enter surname");
        String personPesel = JOptionPane.showInputDialog(this, "Enter pesel");
        String personAgeString = JOptionPane.showInputDialog(this, "Enter age");
        int personAgeInt = Integer.parseInt(personAgeString);
        String personSexString = JOptionPane.showInputDialog(this, "Enter sex (true/false)");
        boolean personSexBoolean = Boolean.parseBoolean(personSexString);
        String personGenderString = JOptionPane.showInputDialog(this, "Enter gender");

        if (personName != null) {
            arrayPersons.add(new AdmStaff(personName, personSurname, personPesel, personAgeInt, personSexBoolean,
                    personGenderString, 0, 0, 0, 0));
        }

        alta.arrayListToArray();

    }

    public void addResStaff() {
        String personName = JOptionPane.showInputDialog(this, "Enter name");
        String personSurname = JOptionPane.showInputDialog(this, "Enter surname");
        String personPesel = JOptionPane.showInputDialog(this, "Enter pesel");
        String personAgeString = JOptionPane.showInputDialog(this, "Enter age");
        int personAgeInt = Integer.parseInt(personAgeString);
        String personSexString = JOptionPane.showInputDialog(this, "Enter sex (true/false)");
        boolean personSexBoolean = Boolean.parseBoolean(personSexString);
        String personGenderString = JOptionPane.showInputDialog(this, "Enter gender");

        if (personName != null) {
            arrayPersons.add(new ResStaff(personName, personSurname, personPesel, personAgeInt, personSexBoolean,
                    personGenderString, 0, 0, 0, 0));
        }
        alta.arrayListToArray();
    }

    public void addCourse() {
        String courseName = JOptionPane.showInputDialog(this, "Enter course name");
        String numECTSString = JOptionPane.showInputDialog(this, "Enter ECTS");
        int numECTSSInt = Integer.parseInt(numECTSString);
        Person person = searchPersons();
        ResStaff resStaff = new ResStaff(numECTSString, numECTSString, numECTSString, numECTSSInt,
                rootPaneCheckingEnabled, numECTSString, numECTSSInt, numECTSSInt, numECTSSInt, numECTSSInt);

        if (person instanceof ResStaff) {
            resStaff = (ResStaff) person;
        } else {
            JOptionPane.showMessageDialog(this, "Person not found or is not a part of research staff");
        }

        if (courseName != null) {
            arrayCourses.add(new Course(participantsAnalizaMatematyczna01, courseName, resStaff, numECTSSInt));
        }

        alta.arrayListToArrayCourse();
    }

    /** Remove a Person class object from the arrayPersons */
    public void removePersonFromArrayList() {
        arrayPersons.remove(searchPersons());
        alta.arrayListToArray();
    }

    /** Remove a Course class object from the arrayCourses */
    public void removeCourseFromArrayList() {

        arrayCourses.remove(searchCourse());
        alta.arrayListToArray();
    }

    /** Save a list of Person class objects from arrayPersons */
    public void savePersonToFile() {
        try (ObjectOutputStream so = new ObjectOutputStream(new FileOutputStream("list.person"))) {
            for (int i = 0; i < arrayPersons.size(); i++) {
                so.writeObject(arrayPersons.get(i));
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /** Read list.person add add to arrayPersons */
    public void readPersonFile() {

        boolean cont = true;
        try {
            try (ObjectInputStream so = new ObjectInputStream(new FileInputStream("person.list"))) {
                while (cont) {
                    Student obj = null;
                    try {
                        obj = (Student) so.readObject();
                    } catch (ClassNotFoundException e) {
                        e.printStackTrace();
                    }
                    if (obj != null)
                        arrayPersons.add(obj);
                    else
                        cont = false;
                }
            }
        } catch (FileNotFoundException e) {

        } catch (IOException e) {

        }

        System.out.println(arrayPersons);
    }

    // Sorting arrayPersons by various variables
    /** Sorting arrayPersons by Name of Person class objects */
    public void sortByName() {
        arrayPersons.sort((o1, o2) -> o1.getName().compareTo(o2.getName()));

        Comparator<Person> c = new Comparator<>() {
            public int compare(Person u1, Person u2) {
                return u1.getName().compareTo(u2.getName());
            }
        };

        alta.arrayListToArray();
    }

    /** Sorting arrayPersons by surname and name of Person class objects */
    public void sortBySurnameAndName() {
        arrayPersons.sort((o1, o2) -> (o1.getSurname() + o1.getSurname()).compareTo(o2.getSurname() + o2.getName()));

        Comparator<Person> c = new Comparator<>() {
            public int compare(Person u1, Person u2) {
                return (u1.getSurname() + u1.getName()).compareTo(u2.getSurname() + u2.getName());
            }
        };

        alta.arrayListToArray();
    }

    /** Sorting arrayPersons by surname and age of Person class objects */
    public void sortBySurnameAndAge() {
        arrayPersons.sort((o1, o2) -> (o1.getSurname() + o1.getAge()).compareTo(o2.getSurname() + o2.getAge()));

        Comparator<Person> c = new Comparator<>() {
            public int compare(Person u1, Person u2) {
                return (u1.getSurname() + u1.getAge()).compareTo(u2.getSurname() + u2.getAge());
            }
        };

        alta.arrayListToArray();
    }

    // Sorting arrayCourses
    /** Sorting arrayCourses by number of ECTS points and lecturer's Surname */
    public void sortByECTSAndSurname() {
        arrayCourses.sort((o1, o2) -> (o1.getNumECTS() + o1.getLecturer().getName())
                .compareTo(o2.getNumECTS() + o2.getLecturer().getName()));

        Comparator<Course> c = new Comparator<>() {
            public int compare(Course c1, Course c2) {
                return (c1.getNumECTS() + c1.getLecturer().getSurname())
                        .compareTo(c2.getNumECTS() + c2.getLecturer().getSurname());
            }
        };

        alta.arrayListToArrayCourse();
    }

    // Getters and setters
    public ArrayList<Person> getArrayPersons() {
        return arrayPersons;
    }

    public ArrayList<Course> getArrayCourses() {
        return arrayCourses;
    }
}
