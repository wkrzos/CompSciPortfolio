package util;

public class Stack<E>{
    private class Node {
        private E value;
        private Node next;

        public Node(E value, Node next){
            this.value = value;
            this.next = next;
        }

        public E getValue(){
            return this.value;
        }

        public void setValue(E value){
            this.value = value;
        }

        public Node getNext() {
            return next;
        }

        public void setNext(Node next) {
            this.next = next;
        }
    }

    Node head = null;

    public E pop(){
        if(head == null){
            throw new RuntimeException("List is empty");
        }

        E value = head.getValue();
        head = head.getNext();
        return value;
    }

    public void push(E data){
        Node newNode = new Node(data, null);

        if(head == null){
            head = newNode;
        } else {
            newNode.setNext(head);
            head = newNode;
        }
    }

    public E peek(){
        if(head == null){
            throw new RuntimeException("List is empty");
        }
        return head.getValue();
    }

    public boolean isEmpty(){
        return head == null;
    }  
}