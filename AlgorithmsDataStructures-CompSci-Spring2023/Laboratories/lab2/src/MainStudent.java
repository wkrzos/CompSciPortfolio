//Użyj 3 sposobów używani predykatu: (chyba) interfejs, klasa anonimowa, lambda

package src;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Iterator;
import java.util.Scanner;

import util.Predicate;
import util.ArrayIterator;
import util.FilterIterator;

class Main {

    private static Student[] studentList = new Student[0];
    private static Student[] studentsGradeBelowThree = new Student[0];
    private static Student[] studentsGradeAboveEqualThree = new Student[0];

    public static void main(String[] args) throws FileNotFoundException {
        readStudents("students2.txt");

        System.out.println("======== NEW DEBUG ========");

        System.out.println("\n\nInitial student list________________");
        printStudentList(studentList);

        System.out.println("\n\nStudent list after grade change________________");
        changeAverageGrade(studentList, "123456", 2);
        printStudentList(studentList);

        System.out.println("\n\nGraded lists________________");
        studentListToGradedLists(studentList);
        System.out.println("\n\nGrades below three:");
        printStudentList(studentsGradeBelowThree);
        System.out.println("\n\nGrades equall or above three:");
        printStudentList(studentsGradeAboveEqualThree);

        System.out.println("\n\nStudents above set grade________________");
        printStudentsAboveGrade(studentList, 4);
    }

    private static void readStudents(String fileName) throws FileNotFoundException {

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

                studentList = addToArray(studentList.length, studentList, student);
            }

            fileScanner.close();

        } catch (Exception fileNotFOuException) {
            System.out.println("bonk!");
        }
    }

    private static void printStudentList(Student[] inputList) {

        try {
            ArrayIterator<Student> iter = new ArrayIterator<>(inputList);

            while (iter.hasNext()) {
                iter.next().getState();
            }
        } catch (Exception NullPointerException) {
            System.out.println("None students");
        }
    }

    //Anonymous class for predicate
    private static void changeAverageGrade(Student[] inputList, String index, double grade) {

        Iterator<Student> iter = new ArrayIterator<Student>(inputList);
    
        Predicate<Student> indexFilter = new Predicate<Student>() {
            public boolean accept(Student student) {
                return student.getIndex().equals(index);
            }
        };
        FilterIterator<Student> filterIter = new FilterIterator<Student>(iter, indexFilter);
    
        while (filterIter.hasNext()) {
            filterIter.next().setAverageGrade(grade);
        }
    }

    //Interface for predicate
    private static void studentListToGradedLists(Student inputList[]) {

        Student outputListBelowThree[] = new Student[0];
        Student outputListAboveThree[] = new Student[0];

        Iterator<Student> iter1 = new ArrayIterator<>(inputList);
        Iterator<Student> iter2 = new ArrayIterator<>(inputList);

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
            outputListAboveThree = addToArray(outputListAboveThree.length, outputListAboveThree,
                    filterIterAbove.next());
        }

        while (filterIterBelow.hasNext()) {
            outputListBelowThree = addToArray(outputListBelowThree.length, outputListBelowThree,
                    filterIterBelow.next());
        }

        studentsGradeBelowThree = outputListBelowThree;
        studentsGradeAboveEqualThree = outputListAboveThree;
    }

    //With lambda for predicate
    private static void printStudentsAboveGrade(Student[] inputList, double gradeFilter) {

        Student tempStudentList[] = new Student[0];
    
        Iterator<Student> iter = new ArrayIterator<>(inputList);
    
        Predicate<Student> grade = (student) -> student.getAverageGrade() > gradeFilter;
    
        FilterIterator<Student> filterIterator = new FilterIterator<>(iter, grade);
    
        while (filterIterator.hasNext()) {
            tempStudentList = addToArray(tempStudentList.length, tempStudentList, filterIterator.next());
        }
    
        printStudentList(tempStudentList);
    }

    private static Student[] addToArray(int n, Student inputArray[], Student studentToAdd) {

        int i;

        Student newarr[] = new Student[n + 1];

        for (i = 0; i < n; i++)
            newarr[i] = inputArray[i];

        newarr[n] = studentToAdd;

        return newarr;
    }
}