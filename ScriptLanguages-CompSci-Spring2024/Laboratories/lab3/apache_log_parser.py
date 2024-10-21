import sys
import re
from datetime import datetime

from apache_log_dictionaries import get_addrs, log_to_dict, print_dict_entry_dates
from apache_log_filter import get_entries_by_addr, get_entries_by_code, get_entries_by_extension, get_failed_reads
from apache_log_sort import sort_log

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

def read_log():
    log_entries = []
    for line in sys.stdin:
        line = line.strip()
        if line:  # Ensure the line is not empty
            try:
                log_entry = parse_apache_log(line)
                log_entries.append(log_entry)
            except ValueError as e:
                print(f"Error parsing log line: {e}", file=sys.stderr)
    return log_entries
    
def print_entries(entries):
    for entry in entries:
        print(entry)
    print("---------- End of Entries ----------\n")      
    
if __name__ == "__main__":
    
    ### Excersise 1
    # Test the log parsing
    log_entries = read_log()
    print_entries(log_entries)
        
    ### Excersise 2
    # Sort by status code (index 3)
    sorted_log = sort_log(log_entries, 3)
    print_entries(sorted_log)
        
    # Filter by a specific IP address
    address = "unicomp6.unicomp.net"
    entries_by_addr = get_entries_by_addr(log_entries, address)
    print_entries(entries_by_addr)
    
    # Filter by a specfic code
    code = 200
    entries_by_code = get_entries_by_code(log_entries, 200)
    print_entries(entries_by_code)
        
    # Get failed reads
    failed_reads = get_failed_reads(log_entries)
    print_entries(failed_reads)
        
    # Get entries by extension
    extension = "txt"
    entries_by_extension = get_entries_by_extension(log_entries, extension)
    print_entries(entries_by_extension)
    
    ### Exercise 3
    
    # Convert the log entries to a dictionary grouped by IP or domain, with dictionary-formatted entries
    entries_dict = log_to_dict(log_entries)

    # Test get_addrs to extract and print all unique IP addresses or domain names from the log entries
    print("Testing get_addrs")
    addresses = get_addrs(entries_dict)
    print(addresses)
    print("---------- End of get_addrs Test ----------\n")
    
    # Test print_dict_entry_dates to print detailed information for each IP address or domain
    print("Testing print_dict_entry_dates")
    print_dict_entry_dates(entries_dict)
    print("---------- End of print_dict_entry_dates Test ----------\n")