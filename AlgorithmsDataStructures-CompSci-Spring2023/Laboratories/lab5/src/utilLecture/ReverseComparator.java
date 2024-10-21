package utilLecture;

import java.util.Comparator;

public class ReverseComparator<T extends Comparable<? super T>> implements
        Comparator<T> {
    // basic comparator
    private final Comparator<T> _comparator;

    public ReverseComparator(Comparator<T> comparator) {
        _comparator = comparator;
    }

    @Override
    public int compare(T left, T right) {
        return _comparator.compare(right, left);
    }
}