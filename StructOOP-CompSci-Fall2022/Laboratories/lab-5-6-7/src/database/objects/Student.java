//Student

package database.objects;

import database.objects.Course;

public class Student extends Person {

    Course co; // Aggregation
    private int numIndex; // Numer indeksu
    private int yearOfStudies; // Rok studiów
    private String listCourses; // TODO What variable should I use? List of classes?
    private boolean erasmus, undergraduate, graduate, fullTime, partTime; // Erasmus, 1-stopnia, 2-stopnia, Stacjonarne,
                                                                          // Niestacjonarne

    /** Default constructor for Student */
    public Student(String name, String surname, String pesel, int age, boolean sex, String gender, Course co,
            int numIndex, int yearOfStudies, String listCourses, boolean erasmus, boolean undergraduate,
            boolean graduate, boolean fullTime, boolean partTime) {
        super(name, surname, pesel, age, sex, gender);
        this.co = co;
        this.numIndex = numIndex;
        this.yearOfStudies = yearOfStudies;
        this.listCourses = listCourses;
        this.erasmus = erasmus;
        this.undergraduate = undergraduate;
        this.graduate = graduate;
        this.fullTime = fullTime;
        this.partTime = partTime;
    }

    // Getters
    public Course getCo() {
        return co;
    }

    public int getNumIndex() {
        return numIndex;
    }

    public int getYearOfStudies() {
        return yearOfStudies;
    }

    public String getListCourses() {
        return listCourses;
    }

    public boolean isErasmus() {
        return erasmus;
    }

    public boolean isUndergraduate() {
        return undergraduate;
    }

    public boolean isGraduate() {
        return graduate;
    }

    public boolean isFullTime() {
        return fullTime;
    }

    public boolean isPartTime() {
        return partTime;
    }

    /** Command for all getters of Student */
    public void getState() {
        super.getState(); // Refers to Person
        System.out.println("Student State: " + "\n|Courses: " + getCo() + " |Index: " + getNumIndex()
                + " |Year of studies: " + getYearOfStudies() + " |List of courses: " + getListCourses() + " |Erasmus: "
                + isErasmus() + " |Full time: " + isFullTime() + " |Part time: " + isPartTime() + " |Graduate: "
                + isGraduate() + " |Undergraduate: " + isGraduate()); // Refers to Student

    }

    // Setters
    public void setCo(Course co) {
        this.co = co;
    }

    public void setNumIndex(int numIndex) {
        this.numIndex = numIndex;
    }

    public void setYearOfStudies(int yearOfStudies) {
        this.yearOfStudies = yearOfStudies;
    }

    public void setListCourses(String listCourses) {
        this.listCourses = listCourses;
    }

    public void setErasmus(boolean erasmus) {
        this.erasmus = erasmus;
    }

    public void setUndergraduate(boolean undergraduate) {
        this.undergraduate = undergraduate;
    }

    public void setGraduate(boolean graduate) {
        this.graduate = graduate;
    }

    public void setFullTime(boolean fullTime) {
        this.fullTime = fullTime;
    }

    public void setPartTime(boolean partTime) {
        this.partTime = partTime;
    }
}
