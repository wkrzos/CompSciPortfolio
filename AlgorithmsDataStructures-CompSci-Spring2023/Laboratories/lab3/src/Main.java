import util.OneWayCycledLinkedList;
import util.OneWayLinkedList;

class Main {

    private static OneWayCycledLinkedList<Integer> list1 = new OneWayCycledLinkedList<>();
    private static OneWayLinkedList<Integer> list2 = new OneWayLinkedList<>();

    public static void main(String[] args) {
        System.out.println("========EX1.1=======");
        demoOneWayCycledLinkedList();
        System.out.println("========EX1.2=======");
        demoJosephusAlgorithm();

        System.out.println("========EX2=======");
        demoOneWayLinkedList();
    }

    private static void demoOneWayCycledLinkedList(){
        OneWayCycledLinkedList<Integer> temp = new OneWayCycledLinkedList<>();

        temp.add(1);
        temp.add(2);
        temp.add(3);

        temp.insert(1, 10);

        System.out.println(temp.indexOf(10)); 

        System.out.println(temp.contains(1));

        System.out.println(temp.removeFirst());

        System.out.println(temp.contains(1));

        System.out.println(temp.size());

        System.out.println(temp.isEmpty());
    }

    private static void demoJosephusAlgorithm() {
        JosephusAlgorithm jp = new JosephusAlgorithm();
        jp.execute(list1, 2, 5);
    }

    private static void demoOneWayLinkedList() {
        list2.insert(list2, 1);
        list2.insert(list2, 7);
        list2.insert(list2, 21);
        list2.insert(list2, 9);
        list2.insert(list2, 5);
        list2.insert(list2, 15);


        list2.printList(list2);
        System.out.println();
        list2.printListReverse(list2);

        OneWayLinkedList<Integer> temp = list2.copy(list2);
        temp.printList(temp);

        System.out.println("\nSize: " + list2.size());

        System.out.println("Sum of keys: " + list2.sumOfKeys(list2.head));
    }
}
