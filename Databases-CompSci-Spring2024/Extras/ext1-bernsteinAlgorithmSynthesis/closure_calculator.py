from itertools import product

# Define the functional dependencies
fds = [
    (frozenset('P'), frozenset('GS')),
    (frozenset('GS'), frozenset('P')),
    (frozenset('PI'), frozenset('O')),
    (frozenset('GI'), frozenset('PS')),
    (frozenset('PGS'), frozenset('E')),
    (frozenset('GSI'), frozenset('O'))
]

# Define the attribute set for which we want to find the closure
attribute_set = set('PIOEGS')

# Define a function to compute the closure of a set of attributes
def compute_closure(attribute_set, fds):
    closure = set(attribute_set)
    while True:
        new_attributes = closure.copy()
        for left, right in fds:
            if left <= closure:
                new_attributes |= right
        if new_attributes == closure:
            break
        closure = new_attributes
    return closure

# Calculate the closure for the given attribute set
closure = compute_closure(attribute_set, fds)

closure
