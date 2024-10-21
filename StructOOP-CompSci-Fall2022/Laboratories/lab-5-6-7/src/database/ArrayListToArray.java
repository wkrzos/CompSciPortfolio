package database;

import java.util.ArrayList;

import javax.swing.table.DefaultTableModel;

import database.objects.AdmStaff;
import database.objects.GenStaff;
import database.objects.ResStaff;
import database.objects.Student;
import MainFrame;

public class ArrayListToArray {

    MainFrame mf;

    String columnNamesAdmStaff[] = { "Name", "Surname", "PESEL", "Age", "Sex", "Gender", "Work Experience", "Salary",
            "Job Position", "Overtime" };
    String columnNamesResStaff[] = { "Name", "Surname", "PESEL", "Age", "Sex", "Gender", "Work Experience", "Salary",
            "Job Position", "Publications" };
    String columnNamesStudent[] = { "Name", "Surname", "PESEL", "Age", "Sex", "Gender", "Index", "Year of studies",
            "Courses", "Erasmus", "Undergraduate", "Graduate", "Full time", "Part time" };
    String columnNamesCourses[] = {"Name", "Lecturer", "ECTS", "Participants"};

    DefaultTableModel arrayOfAdmStaff = new DefaultTableModel(columnNamesAdmStaff, 0);
    DefaultTableModel arrayOfResStaff = new DefaultTableModel(columnNamesResStaff, 0);
    DefaultTableModel arrayOfStudents = new DefaultTableModel(columnNamesStudent, 0);
    DefaultTableModel arrayOfCourses = new DefaultTableModel(columnNamesCourses, 0);

    public ArrayListToArray(MainFrame mf) {
        this.mf = mf;
    }

    public void arrayListToArray() {
        // remove all items from table
        for (int i = arrayOfAdmStaff.getRowCount() - 1; i >= 0; i--) {
            arrayOfAdmStaff.removeRow(i);
        }

        for (int i = arrayOfResStaff.getRowCount() - 1; i >= 0; i--) {
            arrayOfResStaff.removeRow(i);
        }

        for (int i = arrayOfStudents.getRowCount() - 1; i >= 0; i--) {
            arrayOfStudents.removeRow(i);
        }

        for (int i = 0; i < mf.getArrayPersons().size(); i++) {
            String name = mf.getArrayPersons().get(i).getName();
            String surname = mf.getArrayPersons().get(i).getSurname();
            String pesel = mf.getArrayPersons().get(i).getPesel();
            int age = mf.getArrayPersons().get(i).getAge();
            boolean sex = mf.getArrayPersons().get(i).getSex();
            String gender = mf.getArrayPersons().get(i).getGender();

            if (mf.getArrayPersons().get(i) instanceof AdmStaff) {
                int workExperience = ((GenStaff) mf.getArrayPersons().get(i)).getWorkExperience();
                int salary = ((GenStaff) mf.getArrayPersons().get(i)).getSalary();
                int jobPosition = ((AdmStaff) mf.getArrayPersons().get(i)).getJobPosition();
                int hoursOfOvertime = ((AdmStaff) mf.getArrayPersons().get(i)).getHoursOfOvertime();

                Object[] admStaff = { name, surname, pesel, age, sex, gender, workExperience, salary, jobPosition,
                        hoursOfOvertime };
                arrayOfAdmStaff.addRow(admStaff);
            } else if (mf.getArrayPersons().get(i) instanceof ResStaff) {
                int workExperience = ((GenStaff) mf.getArrayPersons().get(i)).getWorkExperience();
                int salary = ((GenStaff) mf.getArrayPersons().get(i)).getSalary();
                int jobPosition = ((ResStaff) mf.getArrayPersons().get(i)).getJobPosition();
                int numPublications = ((ResStaff) mf.getArrayPersons().get(i)).getNumPublications();

                Object[] resStaff = { name, surname, pesel, age, sex, gender, workExperience, salary, jobPosition,
                        numPublications };
                arrayOfResStaff.addRow(resStaff);
            } else if (mf.getArrayPersons().get(i) instanceof Student) {
                int numIndex = ((Student) mf.getArrayPersons().get(i)).getNumIndex();
                int yearOfStudies = ((Student) mf.getArrayPersons().get(i)).getYearOfStudies();
                String listCourses = ((Student) mf.getArrayPersons().get(i)).getListCourses();
                boolean erasmus = ((Student) mf.getArrayPersons().get(i)).isErasmus();
                boolean undergraduate = ((Student) mf.getArrayPersons().get(i)).isUndergraduate();
                boolean graduate = ((Student) mf.getArrayPersons().get(i)).isGraduate();
                boolean fullTime = ((Student) mf.getArrayPersons().get(i)).isFullTime();
                boolean partTime = ((Student) mf.getArrayPersons().get(i)).isPartTime();

                Object[] student = { name, surname, pesel, age, sex, gender, numIndex, yearOfStudies, listCourses,
                        erasmus, undergraduate, graduate, fullTime, partTime };
                arrayOfStudents.addRow(student);
            }
        }
    }

    public void arrayListToArrayCourse() {
        for (int i = arrayOfCourses.getRowCount() - 1; i >= 0; i--) {
            arrayOfCourses.removeRow(i);
        }
        
        for (int i = 0; i < mf.getArrayCourses().size(); i++) {
            String name = mf.getArrayCourses().get(i).getCourseName();
            String lecturer = mf.getArrayCourses().get(i).getLecturer().getSurname();
            int ects = mf.getArrayCourses().get(i).getNumECTS();
            ArrayList<Student> participants = mf.getArrayCourses().get(i).getCourseParticipants();

            Object[] course = {name, lecturer, ects, participants};
            arrayOfCourses.addRow(course);
        }
    }

    // Getters and setters
    public DefaultTableModel getArrayOfAdmStaff() {
        return arrayOfAdmStaff;
    }

    public void setArrayOfAdmStaff(DefaultTableModel arrayOfAdmStaff) {
        this.arrayOfAdmStaff = arrayOfAdmStaff;
    }

    public DefaultTableModel getArrayOfResStaff() {
        return arrayOfResStaff;
    }

    public void setArrayOfResStaff(DefaultTableModel arrayOfResStaff) {
        this.arrayOfResStaff = arrayOfResStaff;
    }

    public DefaultTableModel getArrayOfStudents() {
        return arrayOfStudents;
    }

    public void setArrayOfStudents(DefaultTableModel arrayOfStudents) {
        this.arrayOfStudents = arrayOfStudents;
    }

    public DefaultTableModel getArrayOfCourses() {
        return arrayOfCourses;
    }

    public void setArrayOfCourses(DefaultTableModel arrayOfCourses) {
        this.arrayOfCourses = arrayOfCourses;
    }
}