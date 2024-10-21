# sum_response_size.py
import sys
import json

def sum_response_size():
    total_size = 0
    for line in sys.stdin:
        try:
            log_entry = json.loads(line)
            total_size += int(log_entry["response_size"])
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}", file=sys.stderr)
    print(f"Total data sent to hosts: {total_size / (1024**3):.3f} GB")

if __name__ == "__main__":
    sum_response_size()
