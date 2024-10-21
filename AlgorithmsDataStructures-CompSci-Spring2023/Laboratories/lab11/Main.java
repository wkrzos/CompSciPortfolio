import test.DirectedGraphListTest;
import test.DirectedGraphMatrixTest;
import test.UnidirectedGraphMatrixTest;
import test.UnidirectedGraphListTest;

public class Main{
    public static void main(String[] args) {
        DirectedGraphMatrixTest test1 = new DirectedGraphMatrixTest();
        test1.run();

        UnidirectedGraphMatrixTest test2 = new UnidirectedGraphMatrixTest();
        test2.run();

        DirectedGraphListTest test3 = new DirectedGraphListTest();
        test3.run();

        UnidirectedGraphListTest test4 = new UnidirectedGraphListTest();
        test4.run();
    }
}