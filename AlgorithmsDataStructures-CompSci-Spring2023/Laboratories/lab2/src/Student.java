package src;

public class Student {
    private String index;
    private String name;
    private String surname;
    private double averageGrade;

    public Student(String index, String name, String surname, double averageGrade) {
        this.index = index;
        this.name = name;
        this.surname = surname;
        this.averageGrade = averageGrade;
    }

    public void getState() {
        System.out.printf("%10s%10s%10s%10s", "\n" + index, surname, name, averageGrade);
    }

    public String getIndex() {
        return index;
    }

    public void setIndex(String index) {
        this.index = index;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getSurname() {
        return surname;
    }

    public void setSurname(String surname) {
        this.surname = surname;
    }

    public double getAverageGrade() {
        return averageGrade;
    }

    public void setAverageGrade(double averageGrade) {
        this.averageGrade = averageGrade;
    }
}
