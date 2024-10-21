
def get_entries_by_addr(log_entries, address):
    """
    Filters log entries by the given IP address or hostname.

    Parameters:
    - log_entries: A list of tuples, each representing a log entry.
    - address: A string representing the IP address or hostname to filter by.

    Returns:
    - A list of tuples representing log entries that match the given address.
    """
    filtered_entries = [entry for entry in log_entries if entry[0] == address]
    return filtered_entries

def get_entries_by_code(log_entries, status_code):
    """
    Filters log entries by HTTP status code.

    Parameters:
    - log_entries: A list of tuples, each representing a log entry.
    - status_code: An integer representing the HTTP status code to filter by.

    Returns:
    - A list of tuples representing log entries with the given status code.
    """
    try:
        code = int(status_code)
        if code < 100 or code > 599:
            raise ValueError("Invalid HTTP status code.")
        return [entry for entry in log_entries if entry[3] == code]
    except ValueError as e:
        print(f"Error: {e}")
        return []

def get_failed_reads(log_entries, combined=False):
    """
    Returns lists of log entries with HTTP status codes 4xx and 5xx.

    Parameters:
    - log_entries: A list of tuples representing log entries.
    - combined: A boolean indicating whether to return a combined list or separate lists.

    Returns:
    - Either two separate lists (4xx and 5xx) or a combined list of tuples, based on the 'combined' parameter.
    """
    client_errors = [entry for entry in log_entries if 400 <= entry[3] < 500]
    server_errors = [entry for entry in log_entries if 500 <= entry[3] < 600]
    
    if combined:
        return client_errors + server_errors
    else:
        return client_errors, server_errors
    
def get_entries_by_extension(log_entries, extension):
    extension = extension.lower()
    return [entry for entry in log_entries if entry[2].lower().endswith(f".{extension}")]