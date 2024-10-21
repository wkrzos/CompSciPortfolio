# filter_status_200.py
import sys
import json

def filter_status_code_200():
    for line in sys.stdin:
        try:
            log_entry = json.loads(line)
            if log_entry["status_code"] == 200:
                print(json.dumps(log_entry))
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}", file=sys.stderr)

if __name__ == "__main__":
    filter_status_code_200()
