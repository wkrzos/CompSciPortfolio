//Pracownik Uczelni

package database.objects;

public abstract class GenStaff extends Person {

    private int workExperience; // Staż pracy
    private int salary;

    /** Default constructor for General Staff */
    public GenStaff(String name, String surname, String pesel, int age, boolean sex, String gender, int workExperience,
            int salary) {
        super(name, surname, pesel, age, sex, gender);
        this.workExperience = workExperience;
        this.salary = salary;
    }

    // Methods
    /** Print the state of a GenStaff member */
    public void getState() {
        super.getState();
        System.out.println("GenStaffState:\n|Work experience: " + getWorkExperience() + " |Salary: " + getSalary());
    }

    // Getters
    public int getWorkExperience() {
        return workExperience;
    }

    public int getSalary() {
        return salary;
    }

    // Setters
    public void setWorkExperience(int workExperience) {
        this.workExperience = workExperience;
    }

    public void setSalary(int salary) {
        this.salary = salary;
    }
}
