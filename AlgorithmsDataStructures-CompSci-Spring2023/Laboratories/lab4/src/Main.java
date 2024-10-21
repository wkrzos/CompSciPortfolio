package src;

import util.DoublyLinkedList;
import util.DrowningStack;
import util.FIFOQueue;
import util.StackQueueExtra;
import util.Stack;

public class Main {
    public static void main(String[] args){
        System.out.println("===demo1===");
        demo1();
        System.out.println("===demo2===");
        demo2();
        System.out.println("===demo3===");
        demo3();
        System.out.println("===demo4===");
        demo4();
        System.out.println("===demo5===");
        demo5();
        System.out.println("===demo6===");
        demo6Extra();
    }

    private static void demo1(){

        FIFOQueue<Integer> queue = new FIFOQueue<>();

        queue.enqueue(1);
        queue.enqueue(2);
        queue.enqueue(3);

        System.out.println(queue.dequeue()); // Output: 1
        System.out.println(queue.dequeue()); // Output: 2
        System.out.println(queue.dequeue()); // Output: 3
        System.out.println(queue.isEmpty()); // Output: true
    }

    private static void demo2(){
        Stack<Integer> stack = new Stack<>();

        stack.push(1);
        stack.push(2);
        stack.push(3);

        System.out.println(stack.peek());
        
        System.out.println(stack.pop()); 

        System.out.println(stack.peek());
    }

    private static void demo3(){
        DoublyLinkedList list1 = new DoublyLinkedList();
        DoublyLinkedList list2 = new DoublyLinkedList();
        DoublyLinkedList list3 = new DoublyLinkedList();
        DoublyLinkedList list4 = new DoublyLinkedList();

        list1.addLast(1);
        list1.addLast(2);

        list2.addLast(3);
        list2.addLast(4);
        
        list1.displayList();
        list2.displayList();

        list3 = list1.joinListsAtEnd(list2);
        list4 = list1.joinListsBeforeIndex(list2, 1);

        list3.displayList();
        list4.displayList();
    }

    private static void demo4(){
        DrowningStack<Integer> ds = new DrowningStack<>(3);

        ds.push(1);
        ds.push(2);
        ds.push(3);
        ds.push(4);
        ds.push(5);

        System.out.println(ds.pop());
        System.out.println(ds.pop());
        System.out.println(ds.pop()); 
        //System.out.println(ds.pop()); //This should throw an exception (and it does)
    }

    private static void demo5(){
        PostfixEvaluator pe = new PostfixEvaluator();

        String postfixExpression = pe.readPostfixExpressionFromFile("equat.ion");
        System.out.println("Postfix Expression: " + postfixExpression);

        int result = pe.evaluatePostfixExpression(postfixExpression);
        System.out.println("Result: " + result);
    }

    private static void demo6Extra(){
        StackQueueExtra<Integer> queue = new StackQueueExtra<>();

        queue.enqueue(1);
        queue.enqueue(2);
        queue.enqueue(3);

        System.out.println(queue.peek()); 

        System.out.println(queue.dequeue()); 

        System.out.println(queue.peek()); 
    }
}
