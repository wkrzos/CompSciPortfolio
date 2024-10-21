from dataclasses import dataclass
import argparse
from enum import Enum
from pathlib import Path
import sys

from loguru import logger

# Assuming calculate_stats and parse_ssh modules are correctly implemented
from ssh_log_stats import (
    get_average_duration_and_deviation,
    get_most_and_least_frequent_users,
    get_random_logs_from_random_user,
    get_sessions_stats_grouped_by_user,
)
from ssh_log_parser import read_log_file

class Command(Enum):
    IPV4S = "ipv4s"
    USER = "user"
    MESSAGE_TYPE = "message_type"
    GET_RANDOM_LOGS = "get_random_logs"
    STATS = "stats"
    MOST_AND_LEAST_FREQUENT_USERS = "most_and_least_frequent_users"

@dataclass
class CommandLineArgs:
    logfile: Path
    command: Command
    log_level: str = "INFO"
    group_by_user: bool = False

def main():
    parser = argparse.ArgumentParser(description="SSH Log Analyzer")
    parser.add_argument("logfile", type=Path, help="Path to the SSH log file")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="Set the logging level", default="INFO")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for cmd in Command:
        cmd_parser = subparsers.add_parser(cmd.value, help=f"{cmd.value} operation")
        if cmd == Command.STATS:
            cmd_parser.add_argument("--group-by-user", action="store_true", help="Group the stats by user", default=False)
    
    args = parser.parse_args()

    # Setup logging based on provided log level
    logger.remove()
    logger.add(sys.stderr, level=args.log_level)
    logger.add("logs.log", level="DEBUG", serialize=True)

    logs = read_log_file(args.logfile)

    if args.command:
        execute_command(args, logs)

def execute_command(args, logs):
    match Command(args.command):
        case Command.IPV4S:
            print_ipv4s(logs)
        case Command.USER:
            print_users(logs)
        case Command.MESSAGE_TYPE:
            print_message_types(logs)
        case Command.GET_RANDOM_LOGS:
            print_random_logs(logs)
        case Command.MOST_AND_LEAST_FREQUENT_USERS:
            print_most_and_least_frequent_users(logs)
        case Command.STATS:
            print_stats(logs, args.group_by_user)

# Implement the functions for each case to handle the specific logic.
# Example:
def print_ipv4s(logs):
    for log in logs:
        print(log.ipv4)
        
def print_users(logs):
    seen_users = set()
    for log in logs:
        if log.user and log.user not in seen_users:
            print(log.user)
            seen_users.add(log.user)
            
def print_message_types(logs):
    for log in logs:
        print(log.type.name)  # Assuming type is an Enum and .name gets the Enum member name.

def print_random_logs(logs):
    random_logs = get_random_logs_from_random_user(logs)
    for log in random_logs:
        print(log)

def print_most_and_least_frequent_users(logs):
    most_frequent, least_frequent = get_most_and_least_frequent_users(logs)
    print(f"Most frequent user: {most_frequent}")
    print(f"Least frequent user: {least_frequent}")
    
def print_stats(logs, group_by_user):
    if group_by_user:
        user_stats = get_sessions_stats_grouped_by_user(logs)
        for user, (avg, dev) in user_stats.items():
            print(f"{user}: Average Session Duration = {avg:.2f} seconds, Standard Deviation = {dev:.2f} seconds")
    else:
        avg, dev = get_average_duration_and_deviation(logs)
        print(f"Overall: Average Session Duration = {avg:.2f} seconds, Standard Deviation = {dev:.2f} seconds")


# Similarly implement other functions like print_users, print_message_types, etc.

if __name__ == "__main__":
    main()
