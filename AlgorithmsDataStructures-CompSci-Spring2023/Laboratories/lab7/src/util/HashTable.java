package util;

/**
 * This code is a Java implementation of a hash table, a data structure that
 * allows efficient access, insertion, and deletion of key-value pairs.
 * <p>
 * The class is parameterized with two generic types, K and V, representing the
 * types of keys and values, respectively. The hash table itself is implemented
 * as an array of HashEntry objects, which are defined as a private nested class
 * within the HashTable class.
 * <p>
 * The class has the following public methods:
 * <p>
 * HashTable(int initialCapacity): Constructor that initializes the hash table
 * with a specified initial capacity.
 * <p>
 * V get(K key): Returns the value associated with a given key in the hash
 * table, or null if the key is not present.
 * <p>
 * void put(K key, V value): Inserts a key-value pair into the hash table.
 * <p>
 * boolean containsKey(K key): Returns true if the hash table contains a given
 * key, false otherwise.
 * <p>
 * int size(): Returns the number of key-value pairs in the hash table.
 * <p>
 * boolean isEmpty(): Returns true if the hash table is empty, false otherwise.
 * <p>
 * void resize(): Increases the capacity of the hash table to accommodate more
 * key-value pairs.
 * <p>
 * void dump(): Prints the contents of the hash table to the console.
 * <p>
 * The get, put, and containsKey methods use a hash function to compute the
 * index of the array slot where the key-value pair should be stored or looked
 * up. In the case of collisions (i.e., multiple keys that hash to the same
 * index), the implementation uses linear probing, quadratic probing, or double
 * hashing to find an available slot.
 * <p>
 * The resize method doubles the capacity of the array and rehashes all the
 * key-value pairs to distribute them evenly among the new slots. This operation
 * is necessary to prevent the hash table from becoming too full and degrading
 * performance.
 * <p>
 * The dump method is a debugging utility that prints the contents of the hash
 * table in a human-readable format.
 */

public class HashTable<K, V> {
    private int capacity;
    private int size;
    private HashEntry<K, V>[] table;

    public HashTable(int initialCapacity) {
        this.capacity = initialCapacity;
        this.size = 0;
        this.table = new HashEntry[capacity];
    }

    public V get(K key) {
        int index = hashFunction(key);
        int i = 0;
        while (table[index] != null && !table[index].getKey().equals(key) && i < capacity) {
            i++;
            index = probeSequence(key, i);
        }
        if (table[index] != null && table[index].getKey().equals(key)) {
            return table[index].getValue();
        } else {
            return null;
        }
    }

    public void put(K key, V value) {
        if ((size + 1) * 1.0 / capacity >= 0.75) {
            resize();
        }
        int index = hashFunction(key);
        int i = 0;
        while (table[index] != null && !table[index].getKey().equals(key) && i < capacity) {
            i++;
            index = probeSequence(key, i);
        }
        if (table[index] == null) {
            table[index] = new HashEntry<>(key, value);
            size++;
        } else {
            table[index].setValue(value);
        }
    }

    public boolean containsKey(K key) {
        int index = hashFunction(key);
        int i = 0;
        while (table[index] != null && !table[index].getKey().equals(key) && i < capacity) {
            i++;
            index = probeSequence(key, i);
        }
        return table[index] != null && table[index].getKey().equals(key);
    }

    public int size() {
        return size;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    public void resize() {
        int newCapacity = capacity * 2;
        HashEntry<K, V>[] newTable = new HashEntry[newCapacity];
        
        for (int i = 0; i < capacity; i++) {
            if (table[i] != null) {
                int index = hashFunction(table[i].getKey());
                int j = 0;
                while (newTable[index] != null && j < newCapacity) {
                    j++;
                    index = probeSequence(table[i].getKey(), j);
                }
                newTable[index] = table[i];
            }
        }
        capacity = newCapacity;
        table = newTable;
    }

    public void dump() {
        for (int i = 0; i < capacity; i++) {
            if (table[i] == null) {
                System.out.println("[" + i + "]: null");
            } else {
                System.out.println("[" + i + "]: " + table[i].getKey() + " => " + table[i].getValue());
            }
        }
    }

    private int hashFunction(K key) {
        // funkcja haszująca dla klucza
        return Math.abs(key.hashCode() % capacity);
    }

    private int probeSequence(K key, int i) {
        // sekwencja próbkowania dla adresowania otwartego liniowego
        // return (hashFunction(key) + i) % capacity;

        // sekwencja próbkowania dla adresowania otwartego kwadratowego
        // return (hashFunction(key) + i * i) % private int probeSequence(K key, int i)
        // {
        // sekwencja próbkowania dla adresowania otwartego liniowego
        // return (hashFunction(key) + i) % capacity;

        // sekwencja próbkowania dla adresowania otwartego kwadratowego
        // return (hashFunction(key) + i * i) % capacity;

        // sekwencja próbkowania dla podwójnego haszowania
        int h1 = hashFunction(key);
        int h2 = 1 + Math.abs(key.hashCode() % (capacity - 1));
        return (h1 + i * h2) % capacity;
    }

    private static class HashEntry<K, V> {
        private K key;
        private V value;

        public HashEntry(K key, V value) {
            this.key = key;
            this.value = value;
        }

        public K getKey() {
            return key;
        }

        public V getValue() {
            return value;
        }

        public void setValue(V value) {
            this.value = value;
        }
    }
}
