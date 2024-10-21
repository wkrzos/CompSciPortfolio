def entry_to_dict(entry):
    return {
        "address": entry[0],
        "timestamp": entry[1],
        "request": entry[2],
        "status_code": entry[3],
        "response_size": entry[4]
    }
    
def log_to_dict(log_entries):
    """
    Converts a list of log entry tuples into a dictionary, grouping entries by IP address or domain name.

    Parameters:
    - log_entries: A list of tuples, each representing a log entry.

    Returns:
    - A dictionary with IP addresses or domain names as keys and lists of dictionary-formatted entries as values.
    """
    log_dict = {}
    for entry in log_entries:
        entry_dict = entry_to_dict(entry)
        address = entry_dict["address"]
        if address not in log_dict:
            log_dict[address] = []
        log_dict[address].append(entry_dict)
    return log_dict
    
def get_addrs(entries_dict):
    """
    Extracts IP addresses or domain names from the dictionary keys.

    Parameters:
    - entries_dict: A dictionary with IP addresses or domain names as keys.

    Returns:
    - A list of IP addresses or domain names.
    """
    return list(entries_dict.keys())

def print_dict_entry_dates(entries_dict):
    """
    Prints detailed information for each host from the log entries dictionary, including
    the number of requests, dates of the first and last requests, and the ratio of successful
    requests (status code 200) to the total number of requests.

    Parameters:
    - entries_dict: A dictionary where each key is an IP address or domain name, and the value
                    is a list of dictionaries representing log entries for that host.
    """
    for addr, entries in entries_dict.items():
        # Extract dates and status codes from entries
        dates = [entry['timestamp'] for entry in entries]
        status_codes = [entry['status_code'] for entry in entries]
        
        # Calculate required metrics
        num_requests = len(entries)
        first_request = min(dates) if dates else "N/A"
        last_request = max(dates) if dates else "N/A"
        success_ratio = status_codes.count(200) / num_requests if num_requests > 0 else 0
        
        # Print the gathered information
        print(f"Host: {addr}")
        print(f"  Number of requests: {num_requests}")
        print(f"  Date of first request: {first_request}")
        print(f"  Date of last request: {last_request}")
        print(f"  Ratio of 200 responses: {success_ratio:.2f}")
        print("----------")