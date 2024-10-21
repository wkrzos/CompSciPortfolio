package utilLecture;

import java.util.ArrayList;
import java.util.Comparator;

public class CompoundComparator<T> implements Comparator<T> {

    // comparator ArrayList; from the most important to the least important
    private final ArrayList<Object> _comparators = new ArrayList<Object>();

    public void addComparator(Comparator<T> comparator) {
        _comparators.add(comparator);
    }

    @SuppressWarnings("unchecked")
    public int compare(T left, T right) throws ClassCastException {
        int result = 0;
        for (Object obj : _comparators) {
            Comparator<T> comp = (Comparator<T>) obj;
            result = comp.compare(left, right);
            if (result != 0)
                break;
        }
        return result;
    }
}
