from graphviz import Digraph

def create_final_erd():
    # Initialize a new directed graph
    dot = Digraph(comment='Final Entity Relationship Diagram', format='png')

    # Define entities with labels
    entities = {
        'Article': 'Artykuł',
        'Type': 'Rodzaj',
        'Employee': 'Pracownik',
        'Order': 'Zamówienie',
        'Client': 'Klient',
        'Invoice': 'Faktura',
        'Supplier': 'Dostawca',
        'Delivery': 'Dostawa',
        'Element': 'Element',
        'Position': 'Pozycja'
    }

    # Add entities to the graph
    for entity, label in entities.items():
        dot.node(entity, label)

    # Define relationships
    relationships = [
        ('Article', 'Type', 'Jest\n(0,N) -> (1,1)'),
        ('Employee', 'Order', 'Realizuje\n(1,1) -> (0,N)'),
        ('Order', 'Client', 'Posiada\n(0,N) -> (1,1)'),
        ('Order', 'Element', 'Zawiera\n(1,1) -> (0,N)'),  # Swapped 'Element' with 'Position'
        ('Element', 'Article', 'Mieści\n(1,1) -> (0,N)'),  # Swapped 'Element' with 'Position'
        ('Order', 'Invoice', 'Obejmuje\n(1,1) -> (0,1)'),
        ('Supplier', 'Delivery', 'Dostarcza\n(1,1) -> (0,N)'),
        ('Delivery', 'Position', 'Komponuje\n(1,1) -> (0,N)'),  # Swapped 'Position' with 'Element'
        ('Position', 'Article', 'Włącza\n(1,1) -> (0,N)')  # Swapped 'Position' with 'Element'
    ]

    # Add relationships to the graph
    for src, dst, label in relationships:
        dot.edge(src, dst, label=label)

    # Render the graph to a file
    dot.render('renders/Final_ERD_Diagram')

    return dot

# Create and display the final ERD
final_erd = create_final_erd()
final_erd
