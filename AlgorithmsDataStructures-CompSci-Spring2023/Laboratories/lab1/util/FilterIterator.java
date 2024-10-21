package util;

import java.util.Iterator;
import src.Predicate;

public class FilterIterator<T> implements Iterator<T> {

	private Iterator<T> iter;
	private Predicate<T> pred;
	private T next = null;
	private boolean hasNextVar = true;

	public FilterIterator(Iterator<T> iter, Predicate<T> pred) {
		super();
		this.iter = iter;
		this.pred = pred;
		nextValid();
	}

	private void nextValid() {
		while (iter.hasNext()) {
			next = iter.next();
			if (pred.accept(next)) {
				return;
			}
		}
		hasNextVar = false;
		next = null;
	}

	@Override
	public boolean hasNext() {
		return hasNextVar;
	}

	@Override
	public T next() {
		T nextValue = next;
		nextValid();
		return nextValue;
	}
}