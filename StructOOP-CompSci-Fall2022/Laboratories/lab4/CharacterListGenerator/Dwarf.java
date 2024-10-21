package CharacterListGenerator;

import CharacterListGenerator.Player;

public class Dwarf extends Player {

    private boolean isSmith; //Is the character a smith?
    
    //Constructor
    public Dwarf(String race, float age, boolean canSeeInDark, boolean isIntelligent) {
        super(race, age, canSeeInDark, isIntelligent);
        this.isSmith = isSmith;
    }
    
    //Class methods
    public String CanRead() {
        if(getIfIntelligent()) return "Can read!";
        else return "Cannot read!";
    }

    public String IsAngry(boolean T) {
        if(T) return "They might punch you!";
        else return "They are calm... for now...";
    }

    //Get and set
    public boolean getIsSmith(){
        return this.isSmith;
    }

    public void getState(){
        System.out.println("______________________________________\n" + "This is a Dwarf ");
        super.getState();

        System.out.println("Are they a smith: " + this.isSmith + "\n");
    }

    public void setIsSmith(boolean isSmith) {
        this.isSmith = isSmith;
    }
}
