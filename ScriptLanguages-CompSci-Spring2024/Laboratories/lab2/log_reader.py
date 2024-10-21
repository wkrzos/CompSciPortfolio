#log_reader.py
import re
import sys
import json

def parse_apache_log(log_line):
    # Adjusted regular expression pattern to match your log file format
    log_pattern = r'(\S+) - - \[(.*?)\] "(.*?)" (\d{3}) (\d+|-)'
    match = re.match(log_pattern, log_line)
    if match is None:
        raise ValueError("Invalid log line")
    groups = match.groups()
    log_entry = {
        "ip_address_or_hostname": groups[0],  # IP address or hostname
        "timestamp": groups[1],
        "request_line": groups[2],
        "status_code": int(groups[3]),
        "response_size": groups[4] if groups[4].isdigit() else 0,
    }
    return log_entry
        
if __name__ == "__main__":
    # Parse the file
    for line in sys.stdin:
        try:
            parsed_log = parse_apache_log(line)
            print(json.dumps(parsed_log))
        except ValueError as e:
            print(f"Error parsing log line: {e}")