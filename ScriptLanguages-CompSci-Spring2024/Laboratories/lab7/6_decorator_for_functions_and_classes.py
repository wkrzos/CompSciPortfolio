import logging
from functools import wraps
from time import time

# Configure logging to display the timestamp, severity level, and message
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def log(level='INFO'):
    # This is a decorator factory that takes a logging level as an argument
    def decorator(obj):
        if isinstance(obj, type):
            # This branch is for decorating classes
            class Wrapper(obj):
                # The wrapper class that extends the decorated class
                def __init__(self, *args, **kwargs):
                    # Log the creation of a class instance with its arguments
                    logging.log(getattr(logging, level), f'Creating instance of {obj.__name__} with args={args}, kwargs={kwargs}')
                    super().__init__(*args, **kwargs)  # Call the superclass constructor
            return Wrapper
        else:
            # This branch is for decorating functions
            @wraps(obj)
            def wrapper(*args, **kwargs):
                # Log the call to the function with its arguments
                logging.log(getattr(logging, level), f'Calling {obj.__name__} with args={args}, kwargs={kwargs}')
                start_time = time()  # Record the start time of the function execution
                result = obj(*args, **kwargs)  # Call the original function
                end_time = time()  # Record the end time of the function execution
                # Log the result and the time taken for the function execution
                logging.log(getattr(logging, level), f'Finished {obj.__name__} in {end_time - start_time:.4f} sec with result {result}')
                return result  # Return the result of the function call
            return wrapper
    return decorator

# Example usage of the decorator
@log('DEBUG')  # Apply the logging decorator with DEBUG level to a function
def test_function(a, b):
    return a + b

@log('INFO')  # Apply the logging decorator with INFO level to a class
class TestClass:
    def __init__(self, value):
        self.value = value

# Testing the decorated function and class
test_function(3, 4)  # Should log debug information about the function call
test_instance = TestClass(10)  # Should log info about the class instance creation
