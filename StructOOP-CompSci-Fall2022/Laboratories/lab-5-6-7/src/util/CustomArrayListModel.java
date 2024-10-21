package util;

import javax.swing.*;
import java.util.ArrayList;

public class CustomArrayListModel<E> extends AbstractListModel<E> {

    protected ArrayList<E> list;
 
    public void listModel(ArrayList<E> list) {
        this.list = list;
    }
 
    public void addElement(E element) {
        list.add(element);
        int index = list.size();
        fireContentsChanged(element, index, index);
    }
 
    public void fireDataChanged() {
        int index = list.size();
        fireContentsChanged(list.get(index - 1), index, index);
    }
 
    public int getSize() {
        return list.size();
    }
 
    public E getElementAt(int index) {
        return list.get(index);
    }
}