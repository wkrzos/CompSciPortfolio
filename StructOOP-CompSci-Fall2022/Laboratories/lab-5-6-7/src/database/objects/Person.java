//Osoba
//TODO dodaj stanowiska do AdmStaff, ResStaff, Student

package database.objects;

import java.io.Serializable;

public abstract class Person implements Serializable {

    private static final long serialVersionUID = 00000000;

    private String name;
    private String surname;
    private String pesel;
    private int age;
    private boolean sex; // Defined by characters that are biologically defined
    private String gender; // A cosial construction relating to behaviours and attributes based on labels
                           // of masculinity and femininity; may differ from sex

    /** Default constructor for Person */
    public Person(String name, String surname, String pesel, int age, boolean sex, String gender) {
        this.name = name;
        this.surname = surname;
        this.pesel = pesel;
        this.age = age;
        this.sex = sex;
        this.gender = gender;
    }

    // Getters
    public String getName() {
        return name;
    }

    public String getSurname() {
        return surname;
    }

    public String getPesel() {
        return pesel;
    }

    public int getAge() {
        return age;
    }

    public boolean getSex() {
        return sex;
    }

    public String getGender() {
        return gender;
    }

    /** Command for all getters of Person */
    public void getState() {
        System.out.println("\n_______________________________\nPerson State: " + "\n|Name: " + getName() + " |Surname: "
                + getSurname() + " |Pesel: " + getPesel() + " |Age: " + getAge() + " |Sex: " + getSex() + " |Gender: "
                + getGender());
    }

    // Setters
    public void setName(String name) {
        this.name = name;
    }

    public void setSurname(String surname) {
        this.surname = surname;
    }

    public void setPesel(String pesel) {
        this.pesel = pesel;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public void setSex(boolean sex) {
        this.sex = sex;
    }

    public void setGender(String gender) {
        this.gender = gender;
    }
}