public class Test {
    public static void main(String[] args) {
        // Testing ForestComp
        System.out.println("Testing ForestComp:");
        ForestCompression forestCompression = new ForestCompression();
        forestCompression.makeSet(1);
        forestCompression.makeSet(2);
        forestCompression.makeSet(3);
        forestCompression.makeSet(4);
        forestCompression.print();
        forestCompression.union(1, 2);
        forestCompression.print();
        forestCompression.union(2, 3);
        forestCompression.print();
        forestCompression.union(3, 4);
        System.out.println("Compression!");
        forestCompression.compressNode(1);
        forestCompression.print();

        // Testing ForestRank
        System.out.println("\nTesting ForestRank:");
        ForestRanking forestRanking = new ForestRanking();
        forestRanking.makeSet(1);
        forestRanking.makeSet(2);
        forestRanking.makeSet(3);
        forestRanking.print();
        forestRanking.union(1, 2);
        forestRanking.print();
        forestRanking.union(2, 3);
        forestRanking.print();

        // Testing Tab
        System.out.println("\nTesting Tab:");
        Array array = new Array(4);
        array.makeSet(1);
        array.makeSet(2);
        array.makeSet(3);
        array.print();
        array.union(1, 2);
        array.print();
        array.union(2, 3);
        array.print();

        // Testing TabComp
        System.out.println("\nTesting TabComp:");
        ArrayCompression arrayComparison = new ArrayCompression(4);
        arrayComparison.makeSet(1);
        arrayComparison.makeSet(2);
        arrayComparison.makeSet(3);
        arrayComparison.print();
        arrayComparison.union(1, 2);
        arrayComparison.print();
        arrayComparison.union(2, 3);
        arrayComparison.print();
    }
}
