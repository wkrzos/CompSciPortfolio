import util.HashTable;

public class Excercise3Test {
    public static void testEx3() {
        HashTable<String, Integer> hashtable = new HashTable<>(8);
        hashtable.put("Alice", 1);
        hashtable.put("Bob", 2);
        hashtable.put("Charlie", 3);
        hashtable.put("Dave", 4);
        hashtable.put("Eve", 5);
        hashtable.dump(); // wyświetla pełną tablicę łącznie z pustymi miejscami

        System.out.println("Size: " + hashtable.size());
        System.out.println("isEmpty: " + hashtable.isEmpty());
        System.out.println("containsKey(\"Bob\"): " + hashtable.containsKey("Bob"));
        System.out.println("containsKey(\"Frank\"): " + hashtable.containsKey("Frank"));
        System.out.println("get(\"Charlie\"): " + hashtable.get("Charlie"));

        hashtable.put("Dave", 6);
        hashtable.put("Frank", 7);
        hashtable.dump(); // wyświetla pełną tablicę łącznie z pustymi miejscami

        System.out.println("Size: " + hashtable.size());
        System.out.println("isEmpty: " + hashtable.isEmpty());
        System.out.println("containsKey(\"Bob\"): " + hashtable.containsKey("Bob"));
        System.out.println("containsKey(\"Frank\"): " + hashtable.containsKey("Frank"));
        System.out.println("get(\"Dave\"): " + hashtable.get("Dave"));
    }
}
