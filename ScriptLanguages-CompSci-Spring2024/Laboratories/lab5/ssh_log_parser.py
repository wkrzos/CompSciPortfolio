import argparse
from datetime import datetime, timedelta
import re
from collections import Counter
import logging
import statistics
import sys
import random
from typing import List, Tuple, Dict


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # Set to lowest level globally

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.addFilter(lambda record: record.levelno <= logging.WARNING)  # Only pass debug, info, warning to stdout

stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setLevel(logging.ERROR)  # Only pass error, critical to stderr

logger.addHandler(stdout_handler)
logger.addHandler(stderr_handler)

def parse_log_entry(log_entry):
    """
    parse_log_entry parses a single log entry and extracts relevant information.
    :param log_entry: A string representing a single log entry.
    :return: A dictionary containing parsed log information (date, host, message), or None if parsing fails.
    """
    pattern = (r"^(?P<date>[A-Za-z]+\s\d+\s\d+:\d+:\d+) "
               r"(?P<host>\S+) "
               r"sshd\[\d+\]: "
               r"(?P<message>.+)$")
    match = re.match(pattern, log_entry)
    if match:
        return match.groupdict()
    return None

def get_ipv4s_from_log(log_entry_dict):
    """
    get_ipv4s_from_log extracts IPv4 addresses from a log entry dictionary.

    :param log_entry_dict: A dictionary containing parsed log information.
    :return: A list of IPv4 addresses extracted from the log message.
    """
    if log_entry_dict is None:
        return []  # Return an empty list if log_entry_dict is None
    ipv4_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    addresses = re.findall(ipv4_pattern, log_entry_dict.get("message", ""))
    return addresses

def get_user_from_log(log_entry_dict):
    """
    get_user_from_log extracts the user information from a log entry dictionary.

    :param log_entry_dict: A dictionary containing parsed log information.
    :return: The username extracted from the log message, or None if no user information is found.
    """
    if log_entry_dict is None:
        return None  # Return None immediately if log_entry_dict is None
    user_pattern = r"Invalid user (\S+)"
    match = re.search(user_pattern, log_entry_dict.get("message", ""))
    if match:
        return match.group(1)
    return None

def get_message_type(log_entry_dict):
    """
    get_message_type classifies log messages into different types.

    :param log_entry_dict: A dictionary containing parsed log information.
    :return: A string representing the type of log message (e.g., "break-in attempt", "invalid user", etc.).
    """
    if log_entry_dict is None:
        return "other"  # Assume the message type is "other" if log_entry_dict is None
    message = log_entry_dict.get("message", "")
    if "POSSIBLE BREAK-IN ATTEMPT" in message:
        return "break-in attempt"
    elif "Invalid user" in message:
        return "invalid user"
    elif "Failed password" in message:
        return "failed login"
    elif "Connection closed" in message:
        return "connection closed"
    elif "authentication failure" in message:
        return "authentication failure"
    else:
        return "other"

def read_log_file(filepath):
    """
    read_log_file reads log entries from a log file.

    :param filepath: The path to the log file.
    :return: A list of strings, each representing a single log entry.
    """
    log_entries = []
    with open(filepath, 'r') as file:
        for line in file:
            log_entries.append(line.strip())
    return log_entries

def random_log_entries_for_user(log_entries, n=1):
    """
    random_log_entries_for_user randomly selects log entries for a specific user.

    :param log_entries: A list of log entries.
    :param n: Number of log entries to select (default is 1).
    :return: A list of randomly selected log entries for the user.
    """
    users_logs = {}
    for entry in log_entries:
        parsed_entry = parse_log_entry(entry)
        user = get_user_from_log(parsed_entry)
        if user:
            if user not in users_logs:
                users_logs[user] = []
            users_logs[user].append(entry)
    
    if not users_logs:
        return []
    
    random_user = random.choice(list(users_logs.keys()))
    user_logs = users_logs[random_user]
    return random.sample(user_logs, min(n, len(user_logs)))

def estimate_session_durations(logs: List[str]) -> Tuple[float, float]:
    """
    estimate_session_durations calculates the average session duration and standard deviation from log entries.

    :param logs: A list of log entries.
    :return: A tuple containing the average session duration and standard deviation.
    """
    session_starts = {}
    session_durations = []

    for log in logs:
        # Extract timestamp, IP address, and event message
        parts = log.split()
        timestamp_str = " ".join(parts[:3])
        timestamp = datetime.strptime(timestamp_str, "%b %d %H:%M:%S")
        ip_address = parts[-1].strip("[]")
        event_message = " ".join(parts[4:])

        # Check if it's a session start or end
        if "Connection closed by" in event_message:
            start_time = session_starts.pop(ip_address, None)
            if start_time:
                duration = (timestamp - start_time).total_seconds()
                session_durations.append(duration)
        else:
            if ip_address not in session_starts:
                session_starts[ip_address] = timestamp

    if session_durations:
        average_duration = statistics.mean(session_durations)
        std_deviation = statistics.stdev(session_durations) if len(session_durations) > 1 else 0.0
        return average_duration, std_deviation
    else:
        return 0.0, 0.0

def identify_frequent_users(log_entries):
    """
    identify_frequent_users identifies the most and least frequent users from log entries.

    :param log_entries: A list of log entries.
    :return: A tuple containing the most frequent user and the least frequent user.
    """
    user_counts = Counter(get_user_from_log(parse_log_entry(entry)) for entry in log_entries if get_user_from_log(parse_log_entry(entry)))
    if not user_counts:
        return None, None
    
    most_frequent = user_counts.most_common(1)[0][0]
    least_frequent = user_counts.most_common()[-1][0]
    return most_frequent, least_frequent

def detect_brute_force(log_entries: List[str], max_interval_seconds: int, single_user: bool) -> List[Dict]:
    
    """
    detect_brute_force detects brute force attacks from log entries.

    :param log_entries: A list of log entries.
    :param max_interval_seconds: The maximum time interval allowed between login attempts.
    :param single_user: A boolean indicating whether to consider only single-user attacks.
    :return: A list of dictionaries, each representing a detected brute force attempt.
    """
    
    log_pattern = re.compile(r"(?P<timestamp>\w{3}\s+\d+\s+\d+:\d+:\d+)\s.*?: Failed password for( invalid user)? (?P<user>\S+) from (?P<ip>\S+)")
    
    failed_attempts = {}
    brute_force_attempts = []

    for entry in log_entries:
        match = log_pattern.search(entry)
        if match:
            data = match.groupdict()
            timestamp = datetime.strptime(data["timestamp"], "%b %d %H:%M:%S")
            ip = data["ip"]
            user = data["user"]
            
            # Initialize or update the tracking of failed attempts from this IP
            if ip not in failed_attempts or (timestamp - failed_attempts[ip]["last_attempt"]).total_seconds() > max_interval_seconds:
                failed_attempts[ip] = {"start_time": timestamp, "last_attempt": timestamp, "users": {user}, "count": 1}
            else:
                failed_attempts[ip]["last_attempt"] = timestamp
                failed_attempts[ip]["users"].add(user)
                failed_attempts[ip]["count"] += 1

                # Check if this is considered a brute-force attempt
                is_single_user_attack = single_user and len(failed_attempts[ip]["users"]) == 1
                if (not single_user or is_single_user_attack) and failed_attempts[ip]["count"] > 3:  # Arbitrary threshold of attempts
                    brute_force_attempts.append({
                        "start_time": failed_attempts[ip]["start_time"].strftime("%b %d %H:%M:%S"),
                        "ip": ip,
                        "user": user if single_user else "multiple",
                        "attempt_count": failed_attempts[ip]["count"]
                    })
                    # Reset the tracking for this IP after logging the brute-force attempt
                    del failed_attempts[ip]

    return brute_force_attempts

def execute_cli(args):
    """
    execute_cli executes actions based on command-line interface commands.

    :param args: Parsed command-line arguments.
    """
    try:
        # Configure logging based on the provided log level
        log_level = getattr(logging, args.log_level.upper(), None)
        if log_level is None:
            raise ValueError(f"Invalid log level: {args.log_level}")
        logging.getLogger().setLevel(log_level)
        
        log_entries = read_log_file(args.log_file)

        if args.command == "ipv4s":
            for entry in log_entries:
                print(get_ipv4s_from_log(parse_log_entry(entry)))
        elif args.command == "user":
            for entry in log_entries:
                print(get_user_from_log(parse_log_entry(entry)))
        elif args.command == "message_type":
            for entry in log_entries:
                print(get_message_type(parse_log_entry(entry)))
        elif args.command == "get_random_logs":
            if args.number < 1:
                raise ValueError("Number of log entries must be at least 1.")
            random_entries = random_log_entries_for_user(log_entries, args.number)
            for entry in random_entries:
                print(entry)
        elif args.command == "most_and_least_frequent_users":
            most_frequent, least_frequent = identify_frequent_users(log_entries)
            if most_frequent and least_frequent:
                print(f"Most Frequent User: {most_frequent}\nLeast Frequent User: {least_frequent}")
            else:
                print("No users found in log entries.")
        else:
            raise ValueError(f"Unknown command: {args.command}")
    except ValueError as e:
        logging.error(str(e))
        sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

def setup_cli():
    """
    setup_cli sets up the command-line interface with argument parsing and subcommands.
    :return: An ArgumentParser object.
    """
    parser = argparse.ArgumentParser(description="SSH Log Analysis Tool")
    parser.add_argument("log_file", help="Location of the SSH log file", type=str)
    parser.add_argument("-l", "--log_level", help="Minimum logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)", type=str, choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="INFO")

    subparsers = parser.add_subparsers(help="Sub-command help", dest="command")

    parser_ipv4s = subparsers.add_parser("ipv4s", help="Extract IPv4 addresses from logs")
    parser_user = subparsers.add_parser("user", help="Extract user information from logs")
    parser_message_type = subparsers.add_parser("message_type", help="Classify log messages")

    parser_random_logs = subparsers.add_parser("get_random_logs", help="Get random log entries for a user")
    parser_random_logs.add_argument("-n", "--number", help="Number of log entries to analyze", type=int, default=1)

    parser_most_least_frequent = subparsers.add_parser("most_and_least_frequent_users", help="Identify most and least frequent users")

    return parser

if __name__ == "__main__":
    parser = setup_cli()
    args = parser.parse_args()
    execute_cli(args)