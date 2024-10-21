# filter_polish_requests.py
import sys
import json

def filter_polish_requests():
    for line in sys.stdin:
        try:
            log_entry = json.loads(line)
            if log_entry["ip_address_or_hostname"].endswith('.pl'):
                print(json.dumps(log_entry))
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}", file=sys.stderr)

if __name__ == "__main__":
    filter_polish_requests()
