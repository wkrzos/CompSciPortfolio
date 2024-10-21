import re
from abc import ABC, abstractmethod
from datetime import datetime
from enum import StrEnum
from functools import cached_property
from ipaddress import IPv4Address, AddressValueError
from typing import Optional

class MessageType(StrEnum):
    """
    Enum to represent different types of SSH messages.
    """
    INVALID_PASSWORD = "invalid password"
    ACCEPTED_PASSWORD = "accepted password"
    ERROR = "error"
    OTHER = "other"

class SSHLogEntry(ABC):
    """
    Abstract base class representing a generic SSH log entry.
    """
    timestamp: str
    hostname: str
    app_component: str
    pid: int
    event_description: str
    _original_log_line: str

    def __init__(self, log_line: str) -> None:
        """
        Initialize the SSHLogEntry with parsed log line details.

        Args:
            log_line (str): The raw log line string.
        """
        self.timestamp, self.hostname, self.app_component, self.pid, self.event_description = self._parse_log_line(log_line)
        self._original_log_line = log_line.strip()

    @staticmethod
    def _parse_log_line(log_line: str) -> tuple[str, str, str, int, str]:
        """
        Parse a log line into its components.

        Args:
            log_line (str): The raw log line string.
        
        Returns:
            tuple: Parsed components of the log line.
        
        Raises:
            ValueError: If the log line does not match the expected format.
        """
        log_pattern = re.compile(
            r"(?P<timestamp>\w{3}\s\d{1,2}\s\d{2}:\d{2}:\d{2})\s"
            r"(?P<hostname>\w+)\s"
            r"(?P<app_component>\w+)\[(?P<pid>\d+)\]:\s"
            r"(?P<event_description>.+)"
        )
        match = log_pattern.match(log_line)
        if not match:
            raise ValueError(f"Cannot parse line: {log_line}")
        return (
            match.group("timestamp"),
            match.group("hostname"),
            match.group("app_component"),
            int(match.group("pid")),
            match.group("event_description")
        )

    def __str__(self) -> str:
        """
        Return the original log line string.

        Returns:
            str: The original log line.
        """
        return self._original_log_line

    def extract_ipv4(self) -> Optional[IPv4Address]:
        """
        Extract the first IPv4 address found in the event description.

        Returns:
            Optional[IPv4Address]: The extracted IPv4 address or None if not found.
        """
        ipv4_pattern = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")
        addresses = ipv4_pattern.findall(self.event_description)
        try:
            return IPv4Address(addresses[0]) if addresses else None
        except AddressValueError:
            return None

    def is_valid_ipv4(self) -> bool:
        """
        Validate if the extracted IPv4 address is valid.

        Returns:
            bool: True if the IPv4 address is valid, False otherwise.
        """
        ipv4 = self.extract_ipv4()
        return ipv4 is not None and 0 <= int(ipv4.exploded.split('.')[0]) <= 255

    @abstractmethod
    def validate(self) -> bool:
        """
        Abstract method to validate the log entry.

        Returns:
            bool: True if the log entry is valid, False otherwise.
        """
        raise NotImplementedError

    @property
    def has_ipv4(self) -> bool:
        """
        Check if the log entry contains an IPv4 address.

        Returns:
            bool: True if an IPv4 address is found, False otherwise.
        """
        return self.extract_ipv4() is not None

    def __lt__(self, other: "SSHLogEntry") -> bool:
        """
        Compare log entries based on their timestamps.

        Args:
            other (SSHLogEntry): Another SSH log entry.
        
        Returns:
            bool: True if this log entry's timestamp is earlier than the other.
        """
        return self.timestamp_with_current_year < other.timestamp_with_current_year

    def __gt__(self, other: "SSHLogEntry") -> bool:
        """
        Compare log entries based on their timestamps.

        Args:
            other (SSHLogEntry): Another SSH log entry.
        
        Returns:
            bool: True if this log entry's timestamp is later than the other.
        """
        return self.timestamp_with_current_year > other.timestamp_with_current_year

    @cached_property
    @abstractmethod
    def type(self) -> MessageType:
        """
        Abstract property to get the type of the log entry.

        Returns:
            MessageType: The type of the log entry.
        """
        pass

    @cached_property
    def timestamp_with_current_year(self) -> datetime:
        """
        Get the timestamp of the log entry with the current year.

        Returns:
            datetime: The timestamp with the current year.
        """
        return datetime.strptime(f"{datetime.now().year} {self.timestamp}", "%Y %b %d %H:%M:%S")


class SSHPasswordAttemptLogEntry(SSHLogEntry):
    """
    Class representing an SSH log entry for password attempts.
    """
    def __init__(self, log_line: str):
        """
        Initialize the SSHPasswordAttemptLogEntry with the parsed user.

        Args:
            log_line (str): The raw log line string.
        """
        super().__init__(log_line)
        self.user: str = self._extract_user(self.event_description)

    @staticmethod
    def _extract_user(event_description: str) -> str:
        """
        Extract the username from the event description.

        Args:
            event_description (str): The event description string.
        
        Returns:
            str: The extracted username.
        
        Raises:
            ValueError: If the username cannot be extracted.
        """
        user_pattern = re.compile(
            r"(invalid user |Invalid user |Failed password for invalid user |Failed password for |Accepted password for |user=)(?P<username>\w+)"
        )
        match = user_pattern.search(event_description)
        if not match:
            raise ValueError(f"Cannot extract user from event description: {event_description}")
        return match.group("username")

    def validate(self) -> bool:
        """
        Validate the log entry by matching it against the expected pattern and extracted user.

        Returns:
            bool: True if the log entry is valid, False otherwise.
        """
        match = re.compile(
            r"(?P<timestamp>\w{3}\s\d{1,2}\s\d{2}:\d{2}:\d{2})\s"
            r"(?P<hostname>\w+)\s"
            r"(?P<app_component>\w+)\[(?P<pid>\d+)\]:\s"
            r"(?P<event_description>.+)"
        ).match(self._original_log_line)
        user_match = re.compile(
            r"(invalid user |Invalid user |Failed password for invalid user |Failed password for |Accepted password for |user=)(?P<username>\w+)"
        ).search(self.event_description)
        
        if not match or not user_match:
            return False
        
        return all([
            match,
            user_match,
            self.app_component == match.group("app_component"),
            str(self.pid) == match.group("pid"),
            self.event_description == match.group("event_description"),
            self.hostname == match.group("hostname"),
            self.timestamp == match.group("timestamp"),
            self.user == user_match.group("username"),
        ])

class SSHRejectedPassword(SSHPasswordAttemptLogEntry):
    """
    Class representing an SSH log entry for a rejected password attempt.
    """
    @cached_property
    def type(self) -> MessageType:
        """
        Get the type of the log entry.

        Returns:
            MessageType: The type of the log entry (invalid password).
        """
        return MessageType.INVALID_PASSWORD

class SSHAcceptedPassword(SSHPasswordAttemptLogEntry):
    """
    Class representing an SSH log entry for an accepted password attempt.
    """
    @cached_property
    def type(self) -> MessageType:
        """
        Get the type of the log entry.

        Returns:
            MessageType: The type of the log entry (accepted password).
        """
        return MessageType.ACCEPTED_PASSWORD

class SSHErrorLogEntry(SSHLogEntry):
    """
    Class representing an SSH log entry for an error.
    """
    def validate(self) -> bool:
        """
        Validate the log entry by matching it against the expected pattern.

        Returns:
            bool: True if the log entry is valid, False otherwise.
        """
        match = re.compile(
            r"(?P<timestamp>\w{3}\s\d{1,2}\s\d{2}:\d{2}:\d{2})\s"
            r"(?P<hostname>\w+)\s"
            r"(?P<app_component>\w+)\[(?P<pid>\d+)\]:\s"
            r"(?P<event_description>.+)"
        ).match(self._original_log_line)
        
        if not match:
            return False
        
        return all([
            match,
            self.app_component == match.group("app_component"),
            str(self.pid) == match.group("pid"),
            self.event_description == match.group("event_description"),
            self.hostname == match.group("hostname"),
            self.timestamp == match.group("timestamp"),
        ])

    @cached_property
    def type(self) -> MessageType:
        """
        Get the type of the log entry.

        Returns:
            MessageType: The type of the log entry (error).
        """
        return MessageType.ERROR

class OtherSSHLogEntry(SSHLogEntry):
    """
    Class representing any other type of SSH log entry.
    """
    def validate(self) -> bool:
        """
        Validate the log entry by matching it against the expected pattern.

        Returns:
            bool: True if the log entry is valid, False otherwise.
        """
        log_pattern = re.compile(
            r"(?P<timestamp>\w{3}\s\d{1,2}\s\d{2}:\d{2}:\d{2})\s"
            r"(?P<hostname>\w+)\s"
            r"(?P<app_component>\w+)\[(?P<pid>\d+)\]:\s"
            r"(?P<event_description>.+)"
        )
        match = log_pattern.match(self._original_log_line)
        if not match:
            return False

        return all([
            self.app_component == match.group("app_component"),
            str(self.pid) == match.group("pid"),
            self.event_description == match.group("event_description"),
            self.hostname == match.group("hostname"),
            self.timestamp == match.group("timestamp"),
        ])

    @cached_property
    def type(self) -> MessageType:
        """
        Get the type of the log entry.

        Returns:
            MessageType: The type of the log entry (other).
        """
        return MessageType.OTHER