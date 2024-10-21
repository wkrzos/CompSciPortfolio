//Pracownik Administracyjny

package database.objects;

public class AdmStaff extends GenStaff {

    private int jobPosition;
    private int hoursOfOvertime; // Nadgodziny

    /** Default constructor for Administration Staff */
    public AdmStaff(String name, String surname, String pesel, int age, boolean sex, String gender, int workExperience,
            int salary, int jobPosition, int hoursOfOvertime) {
        super(name, surname, pesel, age, sex, gender, workExperience, salary);
        this.jobPosition = jobPosition;
        this.hoursOfOvertime = hoursOfOvertime;
    }

    // Methods
    /** Print the state of a AdmStaff member */
    public void getState() {
        super.getState();
        System.out.println(
                "AdmStaffState:\n|Position: " + jobsResStaff(jobPosition) + " |Overtime: " + getHoursOfOvertime());
    }

    /** Gets the name of a job position at a given index in AdmStaff constructor */
    public String jobsResStaff(int i) {

        String position = " ";
        String[] allJobPositions = { "Referent", "Specjalista", "Starszy Specjalista" };

        position = allJobPositions[i];

        return position;
    }

    // Getters
    public int getJobPosition() {
        return jobPosition;
    }

    public int getHoursOfOvertime() {
        return hoursOfOvertime;
    }

    // Setters
    public void setJobPosition(int jobPosition) {
        this.jobPosition = jobPosition;
    }

    public void setHoursOfOvertime(int hoursOfOvertime) {
        this.hoursOfOvertime = hoursOfOvertime;
    }
}