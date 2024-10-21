//Pracownik Badawczo-Dydaktyczny

package database.objects;

public class ResStaff extends GenStaff {

    private int jobPosition;
    private int numPublications;// Liczba publikacji

    /** Default constructor for Research Staff */
    public ResStaff(String name, String surname, String pesel, int age, boolean sex, String gender, int workExperience,
            int salary, int jobPosition, int numPublications) {
        super(name, surname, pesel, age, sex, gender, workExperience, salary);
        this.jobPosition = jobPosition;
        this.numPublications = numPublications;
    }

    // Methods
    /** Print state if a ResStaff member */
    public void getState() {
        super.getState();
        System.out.println("ResStaff State: " + "\n|Position: " + jobsResStaff(jobPosition)
                + " |Number of publications: " + getNumPublications() + " |Index number: ");
    }

    /** Gets the name of a job position at a given index in ResStaff constructor */
    public String jobsResStaff(int i) {

        String position = " ";
        String[] allJobPositions = { "Asystent", "Adiunkt", "Doktor", "Profesor Nadzwyczajny", "Profesor Zwyczajny",
                "Wykładowca" };

        position = allJobPositions[i];

        return position;
    }

    // Getters
    public int getJobPosition() {
        return jobPosition;
    }

    public int getNumPublications() {
        return numPublications;
    }

    // Setters
    public void setJobPosition(int jobPosition) {
        this.jobPosition = jobPosition;
    }

    public void setNumPublications(int numPublications) {
        this.numPublications = numPublications;
    }
}
