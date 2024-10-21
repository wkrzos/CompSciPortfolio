from single_relationship_graph_generator import create_custom_labeled_erd

# Define relationships to be generated, including border styles for entities
relationships = [
    ('Article', 'ARTYKUL', 'Type', 'RODZAJ', 'Jest', '0,N', '1,1', 'double', 'solid'),
    ('Employee', 'PRACOWNIK', 'Order', 'ZAMOWIENIE', 'Realizuje', '1,1', '0,N', 'solid', 'double'),
    ('Order', 'ZAMOWIENIE', 'Client', 'KLIENT', 'Posiada', '0,N', '1,1', 'double', 'solid'),
    ('Order', 'ZAMOWIENIE', 'Element', 'ELEMENT', 'Zawiera', '1,1', '0,N', 'double', 'double'),
    ('Position', 'POZYCJA', 'Article', 'ARTYKUL', 'Ma', '0,N', '1,1', 'double', 'double'),
    ('Order', 'ZAMOWIENIE', 'Invoice', 'FAKTURA', 'Obejmuje', '1,1', '0,1', 'double', 'double'),
    ('Supplier', 'DOSTAWCA', 'Delivery', 'DOSTAWA', 'Dostarcza', '1,1', '0,N', 'solid', 'double'),
    ('Delivery', 'DOSTAWA', 'Position', 'POZYCJA', 'Komponuje', '1,1', '0,N', 'double', 'double'),
    ('Element', 'ELEMENT', 'Article', 'ARTYKUL', 'Miesci', '0,N', '1,1', 'double', 'double')
]

# Generate ERD for each relationship
erds = []
for entity1, label1, entity2, label2, relationship, cardinality1, cardinality2, border1, border2 in relationships:
    erd = create_custom_labeled_erd(entity1, label1, entity2, label2, relationship, cardinality1, cardinality2, border1, border2)
    erds.append(erd)
