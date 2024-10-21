package util.graph_by_matrix;

public interface GraphMatrix {
    public void addVertex();
    public void addConnection(int from, int to);
    public void addEdge(int from, int to);
    public void print();
}
