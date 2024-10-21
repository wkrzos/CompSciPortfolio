from graphviz import Digraph

def create_comprehensive_erd():
    # Create a new directed graph for the ERD using the 'dot' engine for ortho edges
    dot = Digraph(comment='Comprehensive Entity Relationship Diagram', format='png', engine='dot')
    
    # Set graph direction left-to-right
    dot.attr(rankdir='LR')
    #dot.attr(rankdir='TB')
    dot.attr(splines='ortho')

    # Define styles for entities
    dot.attr('node', shape='rectangle', style='filled', color='black', fillcolor='white')
    # Entities with single and double borders
    entities = {
        'Article': ('ARTYKUL', 'double'),
        'Type': ('RODZAJ', 'solid'),
        'Employee': ('PRACOWNIK', 'solid'),  # Double border for emphasis
        'Order': ('ZAMOWIENIE', 'double'),
        'Client': ('KLIENT', 'solid'),
        'Invoice': ('FAKTURA', 'double'),
        'Supplier': ('DOSTAWCA', 'solid'),
        'Delivery': ('DOSTAWA', 'double'),
        'Position': ('POZYCJA', 'double'),
        'Element': ('ELEMENT', 'double')
    }

    for entity, (label, border) in entities.items():
        if border == 'double':
            dot.node(entity, label, peripheries='2')
        else:
            dot.node(entity, label)

    # Define styles for the relationship diamonds
    dot.attr('node', shape='diamond')
    relationships = {
        ('Article', 'Type'): ('Jest', '0,N', '1,1'),
        ('Employee', 'Order'): ('Realizuje', '1,1', '0,N'),
        ('Order', 'Client'): ('Posiada', '0,N', '1,1'),
        ('Order', 'Element'): ('Zawiera', '1,1', '0,N'),
        ('Element', 'Article'): ('Miesci', '0,N', '1,1'),
        ('Order', 'Invoice'): ('Obejmuje', '1,1', '0,1'),
        ('Supplier', 'Delivery'): ('Dostarcza', '1,1', '0,N'),
        ('Delivery', 'Position'): ('Komponuje', '1,1', '0,N'),
        ('Position', 'Article'): ('Ma', '0,N', '1,1')
    }

    # Creating relationship nodes and connecting them with orthogonal edges
    for (entity1, entity2), (relationship, tail_cardinality, head_cardinality) in relationships.items():
        rel_node = f"{entity1}_{entity2}_rel"
        dot.node(rel_node, relationship)
        dot.edge(entity1, rel_node, taillabel=tail_cardinality, labeldistance='2', labelangle='30', dir='none', splines='ortho')
        dot.edge(rel_node, entity2, headlabel=head_cardinality, labeldistance='2', labelangle='-30', dir='none', splines='ortho')

    # Render the graph to a file
    dot.render('renders/Comprehensive_ERD_Diagram')

    return dot

# Generate and display the comprehensive ERD
comprehensive_erd = create_comprehensive_erd()
comprehensive_erd