package src;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.Scanner;

import util.FilterIterator;

class Main {
    private static ArrayList<Student> studentList = new ArrayList<>();
    private static ArrayList<Student> studentsGradeBelowThree = new ArrayList<>();
    private static ArrayList<Student> studentsGradeAboveEqualThree = new ArrayList<>();

    public static void main(String[] args) throws FileNotFoundException {
        readStudents("students2.txt");
        System.out.println("__________Test__________");
        printStudentList(studentList);

        changeStudentAverageGrade(studentList, "123456", 2.5);
        printStudentList(studentList);

        studentListToGradedLists(studentList, studentsGradeBelowThree, studentsGradeAboveEqualThree);

        System.out.println("\n|Graded lists");
        System.out.println("\nGrades below three:");
        printStudentList(studentsGradeBelowThree);
        System.out.println("\nGrades equall or above three");
        printStudentList(studentsGradeAboveEqualThree);

        printStudentsAboveGrade(studentList, 4);
    }

    public static void readStudents(String fileName) throws FileNotFoundException {

        try {
            String[] readObject;
            File obj = new File(fileName);
            Scanner fileScanner = new Scanner(obj);
    
            fileScanner.nextLine();
            fileScanner.nextLine();
    
            while (fileScanner.hasNextLine()) {
                String data = fileScanner.nextLine();
                readObject = data.split(" ");
    
                String tempIndex = readObject[2].replace("(", "");
                String index = tempIndex.replace(")", "");
    
                double averageGrade = (Double.parseDouble(readObject[3]) + Double.parseDouble(readObject[4])) / 2;
    
                Student student = new Student(index, readObject[1], readObject[0], averageGrade);
    
                studentList.add(student);
            }
    
            fileScanner.close();
            
        } catch (Exception fileNotFOuException) {
            System.out.println("bonk!");
        }
    }

    private static void printStudentList(ArrayList<Student> inputList) {
        System.out.println("\nStudent list:");

        Iterator<Student> iter = inputList.iterator();

        while (iter.hasNext()) {
            iter.next().getState();
        }
    }

    private static void changeStudentAverageGrade(ArrayList<Student> inputList, String index, double averageGrade) {
        System.out.println("\n|Chagned grade:");

        Iterator<Student> iter = inputList.iterator();
        Predicate<Student> indexFilter = new Predicate<Student>() {
            public boolean accept(Student student) {
                return student.getIndex().equals(index);
            }
        };

        FilterIterator<Student> filterIter = new FilterIterator<>(iter, indexFilter);

        while (filterIter.hasNext()) {
            filterIter.next().setAverageGrade(averageGrade);
        }
    }

    private static void studentListToGradedLists(ArrayList<Student> inputList, ArrayList<Student> outputListBelowThree,
            ArrayList<Student> outputListAboveThree) {

        Iterator<Student> iter1 = inputList.iterator();
        Iterator<Student> iter2 = inputList.iterator();

        Predicate<Student> preAbove = new Predicate<Student>() {
            @Override
            public boolean accept(Student student) {
                return student.getAverageGrade() >= 3;
            }
        };

        Predicate<Student> preBelow = new Predicate<Student>() {
            @Override
            public boolean accept(Student student) {
                return student.getAverageGrade() < 3;
            }
        };

        FilterIterator<Student> filterIterAbove = new FilterIterator<>(iter1, preAbove);
        FilterIterator<Student> filterIterBelow = new FilterIterator<>(iter2, preBelow);

        while (filterIterAbove.hasNext()) {
            outputListAboveThree.add(filterIterAbove.next());
        }

        while (filterIterBelow.hasNext()) {
            outputListBelowThree.add(filterIterBelow.next());
        }

        studentsGradeBelowThree = outputListBelowThree;
        studentsGradeAboveEqualThree = outputListAboveThree;
    }

    private static void printStudentsAboveGrade(ArrayList<Student> inputList, double gradeFilter) {
        System.out.println("\n|Students above " + gradeFilter + ": ");

        ArrayList<Student> tempStudentList = new ArrayList<>();

        Iterator<Student> iter = inputList.iterator();
        Predicate<Student> grade = new Predicate<Student>() {
            @Override
            public boolean accept(Student student) {
                return student.getAverageGrade() > gradeFilter;
            }
        };
        FilterIterator<Student> filterIterator = new FilterIterator<>(iter, grade);

        while (filterIterator.hasNext()) {
            tempStudentList.add(filterIterator.next());
        }

        printStudentList(tempStudentList);
    }
}