package Code;

public class RoadRunner{

    private int roadRunnerAge;
    private String roadRunnerName;

    /**Constructor for a RoadRunner */
    public RoadRunner(int age, String name){
        this.roadRunnerAge = age;
        this.roadRunnerName = name;
    }

    //Getters and Setters
    public int getRoadRunnerAge() {
        return roadRunnerAge;
    }

    public void setRoadRunnerAge(int roadRunnerAge) {
        this.roadRunnerAge = roadRunnerAge;
    }

    public String getRoadRunnerName() {
        return roadRunnerName;
    }

    public void setRoadRunnerName(String roadRunnerName) {
        this.roadRunnerName = roadRunnerName;
    }
}