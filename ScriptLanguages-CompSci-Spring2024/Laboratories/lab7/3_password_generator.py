import random
import string

class PasswordGenerator:
    def __init__(self, length, charset=string.ascii_letters + string.digits, count=1):
        self.length = length  # The length of each password
        self.charset = charset  # The set of allowed characters
        self.count = count  # The number of passwords to generate
        self.generated_count = 0  # Tracks how many passwords have been generated

    # Makes PasswordGenerator an iterable
    def __iter__(self):
        return self

    # Defines how to produce the next item in the iteration; generates a new password
    def __next__(self):
        if self.generated_count >= self.count:
            raise StopIteration  # Stops iteration if the desired number of passwords have been generated
        self.generated_count += 1  # Increments the count of generated passwords
        # Generates a random password by selecting 'length' characters from 'charset'
        return ''.join(random.choice(self.charset) for _ in range(self.length))

# Generate 5, 8-character passwords
password_gen = PasswordGenerator(8, count=5)

print(next(password_gen))
print(next(password_gen))

for password in password_gen:
    print(password)
