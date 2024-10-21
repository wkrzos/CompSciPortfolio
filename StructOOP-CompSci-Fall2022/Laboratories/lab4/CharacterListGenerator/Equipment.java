package CharacterListGenerator;

public class Equipment {
    
    //Class variables
    private boolean Sword;
    private boolean Crossbow;
    private float Ammunition;

    //Constructor
    public Equipment(boolean Sword, boolean Crossbow, float Ammunition){
        this.Sword = Sword;
        this.Crossbow = Crossbow;
        this.Ammunition = Ammunition;
    }

    //Get Methods
    public boolean getSword(){
        return Sword;
    }

    public boolean getCrossbow(){
        return Crossbow;
    }

    public float getAmmunition(){
        return Ammunition;
    }

    //Print the data
    public void getState() {
        System.out.println("The equipment consists of: " + "\nSword: " + getSword() + "\nCrossbow: " + getCrossbow() + "\nAmmunition: " + getAmmunition() +"\n\n");
    }

    //Setters 
    public void setSword(boolean setSword) {
        this.Sword = setSword;
    }

    public void setCrossbow(boolean setCrossbow) {
        this.Crossbow = setCrossbow;
    }

    public void setAmmunition(float Ammunition) {
        this.Ammunition = Ammunition;
    }
}

