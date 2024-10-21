# filter_friday_requests.py
import sys
import json
from datetime import datetime

def filter_friday_requests():
    for line in sys.stdin:
        try:
            log_entry = json.loads(line)
            timestamp = datetime.strptime(log_entry["timestamp"], "%d/%b/%Y:%H:%M:%S %z")
            if timestamp.weekday() == 4:  # Monday is 0 and Sunday is 6
                print(json.dumps(log_entry))
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}", file=sys.stderr)

if __name__ == "__main__":
    filter_friday_requests()
