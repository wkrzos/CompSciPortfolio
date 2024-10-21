

package database.objects;

import java.util.*;

import database.objects.ResStaff;
import database.objects.Student;

public class Course {

    private ArrayList<Student> courseParticipants = new ArrayList<>(); // Participants of the course
    private String courseName; // Nazwa kursu
    private ResStaff lecturer;
    private int numECTS; // Punkty ECTS

    /** Default constructor for Courses */
    public Course(ArrayList<Student> courseParticipants, String courseName, ResStaff lecturer,
            int numECTS) {
        this.courseParticipants = courseParticipants;
        this.courseName = courseName;
        this.lecturer = lecturer;
        this.numECTS = numECTS;
    }

    // Methods
    public String getNameOfParticipants(ArrayList<Student> courseParticipants) {
        String nameOfParticipants = "";

        for (int i = 0; i < this.courseParticipants.size(); i++) {
            nameOfParticipants += courseParticipants.get(i).getName();
            nameOfParticipants += " ";
            nameOfParticipants += courseParticipants.get(i).getSurname();
            nameOfParticipants += ", ";
        }

        return nameOfParticipants;
    }

    public void getState() {
        System.out.println("\n_______________________________\nCourse state:\n|Course name: " + getCourseName()
                + " |Lecturer: " + lecturer.getName() + " |ECTS: " + getNumECTS() + "|Participants: "
                + getNameOfParticipants(courseParticipants));
    }

    // Getters and setters
    public ArrayList<Student> getCourseParticipants() {
        return courseParticipants;
    }

    public void setCourseParticipants(ArrayList<Student> courseParticipants) {
        this.courseParticipants = courseParticipants;
    }

    public String getCourseName() {
        return courseName;
    }

    public void setCourseName(String courseName) {
        this.courseName = courseName;
    }

    public ResStaff getLecturer() {
        return lecturer;
    }

    public void setLecturer(ResStaff lecturer) {
        this.lecturer = lecturer;
    }

    public int getNumECTS() {
        return numECTS;
    }

    public void setNumECTS(int numECTS) {
        this.numECTS = numECTS;
    }
}
