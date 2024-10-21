# count_status_codes.py
import sys
import json

def count_status_codes():
    counts = {"200": 0, "302": 0, "404": 0}
    for line in sys.stdin:
        try:
            log_entry = json.loads(line)
            status_code = str(log_entry["status_code"])
            if status_code in counts:
                counts[status_code] += 1
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}", file=sys.stderr)
    
    for status, count in counts.items():
        print(f"Status code {status}: {count} requests")

if __name__ == "__main__":
    count_status_codes()
