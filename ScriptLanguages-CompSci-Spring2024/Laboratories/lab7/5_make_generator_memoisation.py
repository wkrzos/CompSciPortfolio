from functools import lru_cache

def make_generator_mem(f):
    @lru_cache(None)  # Memoisation with unlimited cache
    def memoized_f(n):
        return f(n)

    def generator():
        n = 1
        while True:
            yield memoized_f(n)
            n += 1

    return generator

def fibonacci_recursive(n):
    if n <= 2:
        return 1
    else:
        return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)

# Utworzenie generatora z memoizacją
fib_gen_mem = make_generator_mem(fibonacci_recursive)()
for i, value in zip(range(10), fib_gen_mem):
    print(value)  # Wypisuje pierwsze 10 liczb Fibonacciego
