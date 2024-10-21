from graphviz import Graph

def create_custom_labeled_erd_example():
    dot = Graph(comment='Custom Labeled ERD', format='png')
    
    # Set graph direction left-to-right
    dot.attr(rankdir='LR')

    # Define styles for entities and relationships
    dot.attr('node', shape='rectangle')
    dot.node('Employee', 'PRACOWNIK')
    dot.node('Order', 'ZAMOWIENIE')

    dot.attr('node', shape='diamond')
    dot.node('relation', 'Realizuje')

    # Define edges with custom label positions
    dot.edge('Employee', 'relation', taillabel='1,1', labeldistance='1.5', labelangle='30', minlen='2')
    dot.edge('relation', 'Order', headlabel='0,N', labeldistance='1.5', minlen='2')

    # Render the graph to a file
    dot.render('Custom_Labeled_Example_ERD_Diagram')

    return dot

# Create and display the ERD with custom labels
custom_labeled_erd_example = create_custom_labeled_erd_example()
custom_labeled_erd_example
