package CharacterListGenerator;

import CharacterListGenerator.*;


public class AllRaces {

    public static void main(String[] args) {
        
        Player [] tabPlayers = new Player[2];

        tabPlayers[0] = new Dwarf("Dwarf 1", 150, true, false);
        tabPlayers[1] = new Elf("Elf 1", 65, true, true);
    
        System.out.println("\n\n");

        //Changing the state of both of them
        ChangeState("Dwarf 1", "Elf 1", tabPlayers);

        //Getting them equipment
        tabPlayers[0].FillEquipment(true, true, 25);
        tabPlayers[1].FillEquipment(false, true, 50);
        
        //Getting them education
        tabPlayers[0].Education();

        //-----------
        for(int i = 0; i < tabPlayers.length; i++) {
            tabPlayers[i].getState();
            (tabPlayers[i].getEquipment()).getState();
        }
    }

    public static void ChangeState(String freeDwarf, String freeElf, Player [] tabPlayers){
        
        for(int i = 0; i < tabPlayers.length; i++) {
            
            if ((tabPlayers[i] instanceof Dwarf) && (tabPlayers[i].getRace().equals(freeDwarf))) {
                ((Dwarf)tabPlayers[i]).setIsSmith(true);
            
            } else {

                if((tabPlayers[i] instanceof Elf) && (tabPlayers[i].getRace().equals(freeElf))){
                    ((Elf)tabPlayers[i]).setIsArcher(true);
                }
            }
        }
    }

}
