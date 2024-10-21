package CharacterListGenerator;

import CharacterListGenerator.Player;

public class Elf extends Player {

    private boolean isArcher; //Is the character an archer?
    
    //Constructor
    public Elf(String race, float age, boolean canSeeInDark, boolean isIntelligent) {
        super(race, age, canSeeInDark, isIntelligent);
        this.isArcher = isArcher;
    }
    
    //Class methods
    public String CanRead() {
        if(getIfIntelligent()) return "Can read!";
        else return "Cannot read!";
    }

    public String IsRude(boolean T) {
        if(T) return "They might punch you!";
        else return "They are calm... for now...";
    }

    //Get and set
    public boolean getIsArcher(){
        return this.isArcher;
    }

    public void getState(){
        System.out.println("______________________________________\n" + "This is an Elf ");
        
        super.getState();

        System.out.println("Are they an archer: " + this.isArcher + "\n");
    }

    public void setIsArcher(boolean isArcher) {
        this.isArcher = isArcher;
    }
}
