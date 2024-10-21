public class Array {
    private int[] array;

    public Array(int n) {
        this.array = new int[n];
    }

    /**
     * The method makeSet(int x) sets the value of element x in the array to x. It
     * effectively creates a singleton set with x as the representative element.
     */
    public void makeSet(int x) {
        this.array[x] = x;
    }

    /**
     * The union(int x, int y) method performs the union operation between two sets
     * represented by elements x and y. It finds the representative of the set
     * containing x using the findSet(int x) method and then sets the value of that
     * representative to y, effectively merging the two sets.
     */
    public void union(int x, int y) {
        int val = findSet(x);
        this.array[val] = y;
    }

    /**
     * The findSet(int x) method returns the representative element of the set that
     * contains element x. It traverses the array starting from x until it reaches
     * an element whose value is equal to its own index, indicating that it is the
     * representative. If the value of array[x] is 0, it means that x is not part of
     * any set, and the method returns -1.
     */
    public int findSet(int x) {
        if (array[x] == 0) {
            return -1;
        }
        while (array[x] != x) {
            x = array[x];
        }
        return x;
    }

    public void print() {
        System.out.println("Printing");
        for (int i = 1; i < array.length; i++) {
            if (array[i] == 0) {
                continue;
            }
            int temp = i;
            while (array[temp] != temp) {
                System.out.print(temp + " ");
                temp = array[temp];
            }
            System.out.print(temp);
            System.out.println();
        }
    }
}