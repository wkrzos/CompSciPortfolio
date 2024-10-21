public class ArrayCompression {

    private int[] array;

    public ArrayCompression(int n) {
        this.array = new int[n];
    }

    /**
     * The method makeSet(int x) sets the value of element x in the array to x. It
     * creates a singleton set with x as the representative element, similar to the
     * previous code.
     */
    public void makeSet(int x) {
        array[x] = x;
    }

    /**
     * The union(int x, int y) method performs the union operation between two sets
     * represented by elements x and y. It finds the representative of the set
     * containing x using the findSet(int x) method and sets the value of that
     * representative to y, effectively merging the two sets, same as the previous
     * code.
     */
    public void union(int x, int y) {
        array[findSet(x)] = y;
    }

    /**
     * The findSet(int x) method returns the representative element of the set that
     * contains element x, but it includes some additional steps compared to the
     * previous code.
     * 
     * First, it checks if array[x] is 0, indicating that x is not part of any set,
     * and returns -1 in that case.
     * 
     * Next, it initializes two temporary variables, tmp and tmp1, with x and 0
     * respectively.
     * 
     * Then, it enters a loop that finds the representative of the set containing x
     * by following the representative links until it reaches an element whose value
     * is equal to its own index. The loop condition is this.array[tmp] != tmp, and
     * in each iteration, tmp is updated to this.array[tmp]. At the end of this
     * loop, tmp will hold the representative element.
     * 
     * After that, it enters another loop that compresses the path from x to the
     * representative element. This loop updates the values in the array to point
     * directly to the representative, improving the efficiency of future findSet
     * operations. Inside the loop, it stores the current value of this.array[x] in
     * tmp1, updates this.array[x] to tmp, and assigns tmp1 to x. This process
     * continues until this.array[x] is equal to x, indicating that x is now
     * directly pointing to the representative.
     * 
     * Finally, it returns the representative element tmp.
     */
    public int findSet(int x) {
        if (array[x] == 0) {
            return -1;
        }

        int tmp1 = x;
        int tmp2 = 0;
        while (this.array[tmp1] != tmp1) {
            tmp1 = this.array[tmp1];
        }
        while (this.array[x] != x) {
            tmp2 = this.array[x];
            this.array[x] = tmp1;
            x = tmp2;
        }
        return tmp1;
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
