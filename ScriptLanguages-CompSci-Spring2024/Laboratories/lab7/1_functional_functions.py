def acronym(words: list[str]) -> str:
    return ''.join(word[0].upper() for word in words)

""" def acronym(list_of_strings: list[str]) -> str:
    return ''.join(map(lambda s: s[0].upper(), filter(bool, list_of_strings))) """

print(acronym(["Ale", "Bajer", "co nie?"]))

def median(numbers: list[float]) -> float:
    sorted_numbers = sorted(numbers)
    l = len(sorted_numbers)
    mid = l // 2 # Floor division, rounds down to the nearest integer
    return sorted_numbers[mid] if l % 2 != 0 else (sorted_numbers[mid - 1] + sorted_numbers[mid]) / 2

print(median([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))

def root(x: float, epsilon=0.1) -> float:
    def helper(guess):
        next_guess = (guess + x / guess) / 2.0
        return next_guess if abs(next_guess**2 - x) < epsilon else helper(next_guess)
    return helper(x / 2.0)

print(root(9))
print(root(9, 0.0001))

""" def make_alpha_dict(s: str) -> dict:
    words = s.split()
    alpha_dict = {}

    for word in words:
        for char in word:
            if char.isalpha():
                if char not in alpha_dict:
                    alpha_dict[char] = [word]
                elif word not in alpha_dict[char]:
                    alpha_dict[char].append(word)

    return alpha_dict """
    
def make_alpha_dict(string: str) -> dict:
    words = string.split()
    is_alpha = lambda x: x.isalpha()
    
    # Create a dictionary comprehension:
    # 1. First, filter the input string to include only alphabetic characters using the defined lambda function.
    # 2. Convert this filtered set of characters into a set to eliminate duplicates.
    # 3. For each unique alphabetic character in the set, map it to a list of words that contain this character.
    return {char: [word for word in words if char in word] for char in set(filter(is_alpha, string))}


print(make_alpha_dict("on i ona"))
print(make_alpha_dict("ala ma kota a kot ma ale"))

""" def flatten(lst: list) -> list:
    flat_list = []
    for item in lst:
        if isinstance(item, (list, tuple)):  # Check if the item is a list or a tuple
            flat_list.extend(flatten(item))  # Recursively flatten and extend the flat list
        else:
            flat_list.append(item)  # Append the non-list item to the flat list
    return flat_list """
    
def flatten(nested_list: list) -> list:
    # Takes an item and recursively flattens it if it is a list or tuple
    def helper(item):
        # Check if the item is a list or tuple
        if isinstance(item, (list, tuple)):
            # If the item is a list or tuple, iterate over its elements
            # For each element, recursively apply the helper function to flatten it
            return [element for sublist in item for element in helper(sublist)]
        else:
            # If the item is neither a list nor a tuple, return it wrapped in a list
            return [item]
    
    # Use a list comprehension to process each item in the main list
    # For each item, apply the helper function and iterate over the resulting flattened elements
    return [element for item in nested_list for element in helper(item)]


print(flatten([1, [2, 3], [[4, 5], 6]]))
print(flatten([1, [2, 3], (4, [5, 6], 7), [[8, 9], 10]]))