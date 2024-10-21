import test.DijkstraTest;
import test.KruskalTest;
import test.PrimTest;

public class MainClass{
    public static void main(String[] args){
        KruskalTest.run();
        PrimTest.run();
        DijkstraTest.run();
    }
}