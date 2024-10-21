import util.OneWayCycledLinkedList;

public class JosephusAlgorithm {

    public void execute(OneWayCycledLinkedList<Integer> inputList, int step, int numberOfPeople) {

        // populate the list
        for (int i = 1; i <= numberOfPeople; i++) {
            inputList.add(i);
        }

        // perform the algorithm
        int position = 0;

        while (inputList.size() > 1) {

            position = (position + step - 1) % inputList.size();
            int removed = inputList.removePosition(position);
            System.out.println("Removed position: " + removed);
        }

        System.out.println("Survivor: " + inputList.get(0).getValue());
    }
}