package CharacterListGenerator; 

public abstract class Player {
    
    //Class elements
    private float age; 
    private String race; 
    private boolean canSeeInDark;
    private boolean isIntelligent;
    private Equipment eq = null;
    
    /**Default constructor */
    public Player(String race, float age, boolean canSeeInDark, boolean isIntelligent) {
        this.race = race;
        this.age = age;
        this.canSeeInDark = canSeeInDark;
        this.isIntelligent = isIntelligent;
    }

    //Methods getting information______________________________//
    public String getRace() {
        return race;
    }
   
    public float getAge() {
        return age;
    }

    public boolean getSeeInTheDark() {
        return canSeeInDark;
    }

    public boolean getIfIntelligent() {
        return isIntelligent;
    }

    public void getState() {
        System.out.println("\nRace: " + getRace() + "\nAge: " + getAge() + "\nDarkvision: " + getSeeInTheDark() +"\nIntelligence: " + getIfIntelligent());
    }

    //Changing state of the objects


    public void setRace(String race) {
        this.race = race;
    }

    public void setAge(float age) {
        this.age = age;
    }

    public void setSeeInTheDark(boolean canSeeInDark) {
        this.canSeeInDark = canSeeInDark;
    }

    public void setIfIntelligent(boolean isIntelligent) {
        this.isIntelligent = isIntelligent;
    }

    //Education
    public void Education() {
        School.getEducated(this);
    }

    //Equipment
    public void FillEquipment(boolean Sword, boolean Crossbow, float Ammunition) {
        eq = new Equipment(Sword, Crossbow, Ammunition);
    }

    public Equipment getEquipment() {
        return eq;
    }
}