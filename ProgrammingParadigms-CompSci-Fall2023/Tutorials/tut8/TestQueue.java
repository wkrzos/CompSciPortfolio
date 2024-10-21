package tut8;

public class TestQueue {
    public static void main(String[] args) {
        MyQueue<Integer> queue = new CircularArrayQueue<>(3);

        try {
            queue.enqueue(1);
            queue.enqueue(2);
            queue.enqueue(3);

            // This should throw FullException
            queue.enqueue(4);
        } catch (FullException e) {
            System.out.println(e.getMessage());
        }

        try {
            System.out.println("First element: " + queue.first());
        } catch (EmptyException e) {
            System.out.println(e.getMessage());
        }

        try {
            queue.dequeue();
            queue.dequeue();
            queue.dequeue();

            // This should throw EmptyException
            queue.dequeue();
        } catch (EmptyException e) {
            System.out.println(e.getMessage());
        }
    }
}

