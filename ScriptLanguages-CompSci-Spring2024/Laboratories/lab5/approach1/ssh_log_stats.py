from datetime import datetime
import random
import statistics
from typing import Iterable, Dict, Tuple
from collections import Counter
from ssh_log import LogEntry, MessageType

def get_random_logs_from_random_user(logs: Iterable[LogEntry]) -> list[LogEntry]:
    logs_list = list(logs)  # Convert iterable to list once
    users_logs = [log for log in logs_list if log.user is not None]
    if not users_logs:
        return []

    user = random.choice(users_logs).user
    user_specific_logs = [log for log in users_logs if log.user == user]

    return random.sample(user_specific_logs, random.randint(1, len(user_specific_logs)))

def get_average_duration_and_deviation(logs: Iterable[LogEntry]) -> Tuple[float, float]:
    session_starts: Dict[int, datetime] = {}
    session_durations = []

    for log in logs:
        if "session opened" in log.event_description:
            session_starts[log.pid] = log.timestamp_with_current_year
        elif "session closed" in log.event_description and log.pid in session_starts:
            start_time = session_starts.pop(log.pid, None)
            if start_time:
                duration = (log.timestamp_with_current_year - start_time).total_seconds()
                session_durations.append(duration)

    if session_durations:
        average_duration = statistics.mean(session_durations)
        std_deviation = statistics.stdev(session_durations) if len(session_durations) > 1 else 0.0
        return average_duration, std_deviation
    else:
        return 0.0, 0.0
    

def get_sessions_stats_grouped_by_user(logs: Iterable[LogEntry]) -> Dict[str, Tuple[float, float]]:
    logs_list = list(logs)
    user_logs = filter(lambda log: log.user, logs_list)
    user_stats = {}

    for user, user_specific_logs in group_logs_by_user(user_logs).items():
        user_stats[user] = get_average_duration_and_deviation(user_specific_logs)

    return user_stats

def group_logs_by_user(logs: Iterable[LogEntry]) -> Dict[str, list[LogEntry]]:
    grouped_logs = {}
    for log in logs:
        if log.user not in grouped_logs:
            grouped_logs[log.user] = []
        grouped_logs[log.user].append(log)
    return grouped_logs

def get_most_and_least_frequent_users(logs: Iterable[LogEntry]) -> Tuple[str, str]:
    user_logins = Counter(log.user for log in logs if log.user and log.type == MessageType.SUCCESSFUL_LOGIN)

    if not user_logins:
        return None, None  # No successful logins found

    most_freq_user = user_logins.most_common(1)[0][0]
    least_freq_user = user_logins.most_common()[-1][0]

    return most_freq_user, least_freq_user
