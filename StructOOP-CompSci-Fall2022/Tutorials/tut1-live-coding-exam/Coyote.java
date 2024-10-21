package Code;

import java.util.*;

public class Coyote {
    
    private ArrayList<RoadRunner> eatenAnimals = new ArrayList<>();

    private int age;
    private String name;

    /**Constructor for the Coyote */
    public Coyote(ArrayList<RoadRunner> eatenAnimals, int age, String name) {
        this.eatenAnimals = eatenAnimals;
        this.age = age;
        this.name = name;
    }

    /**Eat a RoadRunner method */
    public void eatRoadRunner(RoadRunner rr){
        eatenAnimals.add(rr);
    }

    //Getters and setters
    public ArrayList<RoadRunner> getEatenAnimals() {
        return eatenAnimals;
    }
    public void setEatenAnimals(ArrayList<RoadRunner> eatenAnimals) {
        this.eatenAnimals = eatenAnimals;
    }
    public int getAge() {
        return age;
    }
    public void setAge(int age) {
        this.age = age;
    }
    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
}
