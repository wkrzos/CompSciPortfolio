import re
from datetime import datetime

def parse_apache_log(log_line):
    log_pattern = r'(\S+) - - \[(.*?)\] "(.*?)" (\d{3}) (\d+|-)'
    match = re.match(log_pattern, log_line)
    if match is None:
        raise ValueError("Invalid log line")
    groups = match.groups()
    
    # Convert timestamp to datetime.datetime
    timestamp_format = "%d/%b/%Y:%H:%M:%S %z"
    timestamp = datetime.strptime(groups[1], timestamp_format)
    
    # Convert status code to int and response size to int, handling '-' as 0
    status_code = int(groups[3])
    response_size = int(groups[4]) if groups[4].isdigit() else 0
    
    return (groups[0], timestamp, groups[2], status_code, response_size)

def entry_to_dict(entry):
    return {
        "address": entry[0],
        "timestamp": entry[1],
        "request": entry[2],
        "status_code": entry[3],
        "response_size": entry[4]
    }