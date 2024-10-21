from graphviz import Graph

def create_custom_labeled_erd(entity1, label1, entity2, label2, relationship, cardinality1, cardinality2, border1='solid', border2='solid'):
    dot = Graph(comment='Custom Labeled ERD', format='png')
    
    # Set graph direction left-to-right and define the fixed size
    dot.attr(rankdir='LR', size="6,1!", ratio='fill', bgcolor='transparent')  # Zmniejszono wysokość do 1.5 cala

    # Define styles for entities based on the border parameters
    dot.attr('node', shape='rectangle', style='filled', color='black', fillcolor='white')
    if border1 == 'double':
        dot.node(entity1, label1, peripheries='2')
    else:
        dot.node(entity1, label1)

    if border2 == 'double':
        dot.node(entity2, label2, peripheries='2')
    else:
        dot.node(entity2, label2)

    # Define styles for the relationship
    dot.attr('node', shape='diamond')
    dot.node('relation', relationship)

    # Define edges with custom label positions and minimum length
    dot.edge(entity1, 'relation', taillabel=cardinality1, labeldistance='1.5', labelangle='30', minlen='1')
    dot.edge('relation', entity2, headlabel=cardinality2, labeldistance='1.5', minlen='1')

    # Render the graph to a file
    output_filename = f"renders/relationships/{entity1}_{entity2}_{relationship}_ERD_Diagram"
    dot.render(output_filename)

    return dot

# Example of using the function with adjusted sizes
relationship_example = create_custom_labeled_erd(
    'Employee', 'PRACOWNIK', 'Order', 'ZAMOWIENIE', 'Realizuje', '1,1', '0,N', border1='double', border2='solid'
)
relationship_example
