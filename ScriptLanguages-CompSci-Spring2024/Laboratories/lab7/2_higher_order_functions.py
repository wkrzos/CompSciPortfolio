# pred: Callable[[int], bool], iterable: Iterable[int]
def forall(pred, iterable):
    return all(pred(item) for item in iterable)

def exists(pred, iterable):
    return any(pred(item) for item in iterable)

# n: int, pred: Callable[[int], bool], iterable: Iterable[int]
def atleast(n, pred, iterable):
    return sum(1 for item in iterable if pred(item)) >= n # The sum of 1's is compared to the minimum number recquried (n), returns a boolean

def atmost(n, pred, iterable):
    return sum(1 for item in iterable if pred(item)) <= n # The sum of 1's is compared to the maximum number recquried (n), returns a boolean

numbers = [1, 2, 3, 4, 5]
is_positive = lambda x: x > 0
print(forall(is_positive, numbers))  # True

numbers = [1, 3, 5, 7, 2]
is_even = lambda x: x % 2 == 0
print(exists(is_even, numbers))  # True

numbers = [5, 10, 15, 20, 25, 1, 2]
greater_than_ten = lambda x: x > 10
print(atleast(3, greater_than_ten, numbers))  # True

numbers = [1, 3, 5, 7, 9, 11, 13]
less_than_five = lambda x: x < 5
print(atmost(2, less_than_five, numbers))  # True
