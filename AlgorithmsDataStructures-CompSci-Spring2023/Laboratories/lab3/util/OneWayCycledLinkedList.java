package util;

public class OneWayCycledLinkedList<E> {

    public class Element {

        private E value;
        private Element next;

        public E getValue() {
            return value;
        }

        public void setValue(E value) {
            this.value = value;
        }

        public Element getNext() {
            return next;
        }

        public void setNext(Element next) {
            this.next = next;
        }

        Element(E data) {
            this.value = data;
        }
    }

    public Element head = null;

    int size = 0;

    public OneWayCycledLinkedList() {

    }

    /** Add to the end of the list */
    public boolean add(E e) {

        Element newElem = new Element(e);

        if (head == null) {
            head = newElem;
            return true;
        }

        Element tail = head;

        while (tail.getNext() != null) {
            tail = tail.getNext();
        }

        tail.setNext(newElem);
        return true;
    }

    /** Insert value e at index */
    public boolean insert(int index, E e) {

        if (index < 0) {
            return false;
        }

        Element newElem = new Element(e);

        if (index == 0) {
            newElem.setNext(head);
            head = newElem;
            return true;
        }

        Element actElem = get(index - 1);
        if (actElem == null) {
            return false;
        }

        newElem.setNext(actElem.getNext());
        actElem.setNext(newElem);

        return true;
    }

    public int indexOf(E value) {
        int pos = 0;
        Element actElem = head;
        while (actElem != null) {
            if (actElem.getValue() == value)
                return pos;
            pos++;
            actElem = actElem.getNext();
        }
        return -1;
    }

    public boolean contains(E value) {
        return indexOf(value) >= 0;
    }

    public Element get(int index) {

        Element actElem = head;

        while (index > 0 && actElem != null) {
            index--;
            actElem = actElem.getNext();
        }

        return actElem;
    }

    public E removePosition(int index) {

        if (head == null)
            return null;

        if (index == 0) {
            E retValue = head.getValue();
            head = head.getNext();
            return retValue;
        }

        Element actElem = get(index - 1);

        if (actElem == null || actElem.getNext() == null)
            return null;

        E retValue = actElem.getNext().getValue();
        actElem.setNext(actElem.getNext().getNext());

        return retValue;
    }

    public E removeFirst() {
        int index = 0;

        if (head == null)
            return null;

        if (index == 0) {
            E retValue = head.getValue();
            head = head.getNext();
            return retValue;
        }

        Element actElem = get(index - 1);

        if (actElem == null || actElem.getNext() == null)
            return null;

        E retValue = actElem.getNext().getValue();
        actElem.setNext(actElem.getNext().getNext());

        return retValue;
    }

    public int size() {

        int pos = 0;
        Element actElem = head;
        while (actElem != null) {
            pos++;
            actElem = actElem.getNext();
        }
        return pos;
    }

    public boolean isEmpty() {
        return head == null;
    }

    public void clear() {
        head = null;
    }

    public void display() {

    }
}
