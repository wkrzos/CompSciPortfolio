import datetime
from ipaddress import IPv4Address
from typing import Union, Iterator, Callable
from SSHLogEntry import MessageType, OtherSSHLogEntry, SSHAcceptedPassword, SSHErrorLogEntry, SSHLogEntry, SSHRejectedPassword

class SSHLogJournal:
    def __init__(self):
        """
        Initialize the SSHLogJournal with an empty list of SSH log entries.
        """
        self._ssh_log_entries: list[SSHLogEntry] = []

    def __getitem__(self, key: Union[int, slice, datetime.datetime, IPv4Address]) -> Union[SSHLogEntry, list[SSHLogEntry], Iterator[SSHLogEntry]]:
        """
        Retrieve log entries based on different types of keys.

        Args:
            key (Union[int, slice, datetime.datetime, IPv4Address]): The key used to retrieve log entries.
        
        Returns:
            Union[SSHLogEntry, list[SSHLogEntry], Iterator[SSHLogEntry]]: The log entry or entries matching the key.
        
        Raises:
            TypeError: If the key type is invalid.
        """
        if isinstance(key, (int, slice)):
            return self._ssh_log_entries[key]
        elif isinstance(key, datetime.datetime):
            return (
                log
                for log in self._ssh_log_entries
                if log.timestamp_with_current_year == key
            )
        elif isinstance(key, IPv4Address):
            return (
                log
                for log in self._ssh_log_entries
                if log.has_ipv4 and log.extract_ipv4() == key
            )
        else:
            raise TypeError("Invalid key type")

    def __len__(self) -> int:
        """
        Get the number of log entries.

        Returns:
            int: The number of log entries.
        """
        return len(self._ssh_log_entries)

    def __iter__(self) -> Iterator[SSHLogEntry]:
        """
        Get an iterator over the log entries.

        Returns:
            Iterator[SSHLogEntry]: An iterator over the log entries.
        """
        return iter(self._ssh_log_entries)

    def __contains__(self, value: SSHLogEntry) -> bool:
        """
        Check if a log entry is in the list of log entries.

        Args:
            value (SSHLogEntry): The log entry to check.
        
        Returns:
            bool: True if the log entry is in the list, False otherwise.
        """
        return value in self._ssh_log_entries

    def filter(self, predicate: Callable[[SSHLogEntry], bool]) -> Iterator[SSHLogEntry]:
        """
        Filter log entries based on a predicate function.

        Args:
            predicate (Callable[[SSHLogEntry], bool]): The function to filter log entries.
        
        Returns:
            Iterator[SSHLogEntry]: An iterator over the filtered log entries.
        """
        return filter(predicate, self._ssh_log_entries)

    def append(self, log: str) -> None:
        """
        Add a new log entry to the list after validation.

        Args:
            log (str): The log entry as a string.
        
        Raises:
            ValueError: If the log entry is invalid.
        """
        ssh_entry = self._create_ssh_entry(log)

        if not ssh_entry.validate():
            raise ValueError(f"Invalid log entry: {log}")

        self._ssh_log_entries.append(ssh_entry)

    @staticmethod
    def _create_ssh_entry(log: str) -> SSHLogEntry:
        """
        Create a specific type of SSH log entry based on the log string.

        Args:
            log (str): The log entry as a string.
        
        Returns:
            SSHLogEntry: The specific SSH log entry instance.
        """
        if "Failed password for invalid user" in log:
            return SSHRejectedPassword(log)
        elif "Accepted password for" in log:
            return SSHAcceptedPassword(log)
        elif "error" in log:
            return SSHErrorLogEntry(log)
        else:
            return OtherSSHLogEntry(log)

    def get_logs_by_type(self, message_type: MessageType) -> list[SSHLogEntry]:
        """
        Retrieve log entries of a specific message type.

        Args:
            message_type (MessageType): The type of messages to retrieve.
        
        Returns:
            list[SSHLogEntry]: A list of log entries of the specified type.
        """
        return [log for log in self._ssh_log_entries if log.type == message_type]
