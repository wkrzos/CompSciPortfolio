from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from functools import cached_property
import re

class MessageType(Enum):
    SUCCESSFUL_LOGIN = auto()
    FAILED_LOGIN = auto()
    CONNECTION_CLOSED = auto()
    INVALID_PASSWORD = auto()
    INVALID_USERNAME = auto()
    BREAK_IN_ATTEMPT = auto()
    OTHER = auto()

    def check(self, description: str) -> bool:
        """Determine if the given description matches the MessageType."""
        # This method will be overridden in the LogEntry class with specific checks for each type.
        pass

@dataclass(frozen=True, kw_only=True)
class LogEntry:
    timestamp: str
    hostname: str
    app_component: str
    pid: int
    event_description: str
    original_log_line: str

    _user_pattern = re.compile(
        r"(?:invalid user |Invalid user |Failed password for invalid user |Failed password for |Accepted password for |user=)(?P<username>\w+)"
    )
    _ipv4_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
    _log_pattern = re.compile(
        r"(\w{3} \d{1,2} \d{2}:\d{2}:\d{2}) (\w+) (\w+)\[(\d+)\]: (.+)"
    )

    @cached_property
    def type(self) -> MessageType:
        for message_type in MessageType:
            if message_type.check(self.event_description):
                return message_type
        return MessageType.OTHER

    @cached_property
    def byte_size(self) -> int:
        return len(self.original_log_line.encode("utf-8"))

    @cached_property
    def ipv4(self) -> list[str]:
        return self._ipv4_pattern.findall(self.event_description)

    @cached_property
    def user(self) -> str | None:
        match = self._user_pattern.search(self.event_description)
        return match.group("username") if match else None

    @cached_property
    def timestamp_with_current_year(self) -> datetime:
        return datetime.strptime(f"{datetime.now().year} {self.timestamp}", "%Y %b %d %H:%M:%S")

    @classmethod
    def from_log(cls, log_line: str):
        match = cls._log_pattern.match(log_line)
        if match:
            return cls(
                timestamp=match.group(1),
                hostname=match.group(2),
                app_component=match.group(3),
                pid=int(match.group(4)),
                event_description=match.group(5),
                original_log_line=log_line.strip(),
            )
        else:
            raise ValueError(f"Cannot parse line: {log_line}")

    def __str__(self) -> str:
        return self.original_log_line.strip()

# Each MessageType should have its specific check logic defined.