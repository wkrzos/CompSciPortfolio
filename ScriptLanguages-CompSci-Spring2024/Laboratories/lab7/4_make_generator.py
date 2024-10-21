def make_generator(f):
    def generator():
        n = 1
        while True:
            yield f(n)
            n += 1
    return generator

def fibonacci(n):
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b

# Use make_generator with fibonacci
fib_gen = make_generator(fibonacci)()
for i, value in zip(range(10), fib_gen):
    print(value)  # First 10 numbers of the series


arithmetic_sequence = lambda n: 2 * n
arithmetic_gen = make_generator(arithmetic_sequence)()
for i, value in zip(range(10), arithmetic_gen):
    print(value)  # (2, 4, 6, ...)

geometric_sequence = lambda n: 3**n
geometric_gen = make_generator(geometric_sequence)()
for i, value in zip(range(10), geometric_gen):
    print(value)  # (3, 9, 27, ...)
