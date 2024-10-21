package Code;

import java.util.*;

public class WojciechKrzos{
    public static void main(String[] args) {  

        //Morse
        Morse m = new Morse();

        System.out.println("_________________________________________________________");
    
        System.out.println(m.letterToMorse(Morse.getWord(), Morse.getLetters(), Morse.getCode())); 
        System.out.println(m.onlyDashes(Morse.getLetters(), Morse.getCode()));

        System.out.println("_________________________________________________________");
    
        //RoadRunners
        ArrayList<RoadRunner> myRoadRunners = new ArrayList<>();

        myRoadRunners.add(new RoadRunner(15, "Bob"));
        myRoadRunners.add(new RoadRunner(45, "Marley"));
        myRoadRunners.add(new RoadRunner(21, "Bobbens"));
        myRoadRunners.add(new RoadRunner(67, "Archie"));
        myRoadRunners.add(new RoadRunner(67, "McMackey"));

        sortArrayOfRoadRunners(myRoadRunners);
        System.out.println("The sorted RoadRunners: ");
        printArrayOfRoadRunners(myRoadRunners);
        findOldestRoadRunner(myRoadRunners); 
        System.out.println("_________________________________________________________");
    
        //Coyote
        ArrayList<RoadRunner> eatenAnimals = new ArrayList<>();
        Coyote c = new Coyote(eatenAnimals, 15, "Coyote");
        c.eatRoadRunner(myRoadRunners.get(0));
        c.eatRoadRunner(myRoadRunners.get(1));

        System.out.println("Eaten RoadRunners are: ");
        printArrayOfRoadRunners(eatenAnimals);
        System.out.println("_________________________________________________________");
    }

    //Methods for RoadRunners
    /**Sort the array */
    public static void sortArrayOfRoadRunners(ArrayList<RoadRunner> list){
        list.sort((o1, o2)->o1.getRoadRunnerName().compareTo(o2.getRoadRunnerName()));
    }

    /**Print the array */
    public static void printArrayOfRoadRunners(ArrayList<RoadRunner> list){
        for(int i = 0; i < list.size(); i++){
            System.out.println(list.get(i).getRoadRunnerName());
        }
    }

    /**Find the oldest RoadRunner */
    public static void findOldestRoadRunner(ArrayList<RoadRunner> list){
        int max = 0;
        int index = 0;
        int k;

        for(int i = 0; i < list.size(); i++) { 
            if(list.get(i).getRoadRunnerAge() > max){

            max = list.get(i).getRoadRunnerAge();
            index = i;
            
            } else if (list.get(i).getRoadRunnerAge() == max) {
                
            k = list.get(index).getRoadRunnerName().compareTo(list.get(i).getRoadRunnerName());

            if(k > 0){
                max = list.get(index).getRoadRunnerAge();  
            } else if (k < 0){
                max = list.get(i).getRoadRunnerAge();
            }

            }
        } 

        System.out.println("The oldest RoadRunner is " + max + " and their name is " + list.get(index).getRoadRunnerName());
    }
}
