from datetime import datetime
import re

def parse_apache_log(log_line):
    log_pattern = r'(\S+) - - \[(.*?)\] "(.*?)" (\d{3}) (\d+|-)'
    match = re.match(log_pattern, log_line)
    if match is None:
        raise ValueError("Invalid log line")
    groups = match.groups()

    timestamp_format = "%d/%b/%Y:%H:%M:%S %z"
    timestamp = datetime.strptime(groups[1], timestamp_format)
    method, resource = groups[2].split(' ')[0], groups[2].split(' ')[1]

    status_code = int(groups[3])
    response_size = int(groups[4]) if groups[4].isdigit() else 0

    return {
        'remote_host': groups[0],
        'date': timestamp.strftime('%Y-%m-%d'),
        'time': timestamp.strftime('%H:%M:%S'),
        'timezone': timestamp.strftime('%z'),
        'method': method,
        'resource': resource,
        'status_code': status_code,
        'response_size': response_size
    }

def read_log_file(file_path):
    with open(file_path, 'r') as file:
        log_entries = [parse_apache_log(line.strip()) for line in file if line.strip()]
    return log_entries
