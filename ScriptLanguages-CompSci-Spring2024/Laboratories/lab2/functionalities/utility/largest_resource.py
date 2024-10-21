# largest_resource.py
import sys
import json

def find_largest_resource():
    largest_size = 0
    largest_resource = None
    for line in sys.stdin:
        try:
            log_entry = json.loads(line)
            size = int(log_entry["response_size"])
            if size > largest_size:
                largest_size = size
                largest_resource = log_entry["request_line"]
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}", file=sys.stderr)
    
    print(f"Largest resource: {largest_resource}, Size: {largest_size} bytes")

if __name__ == "__main__":
    find_largest_resource()
