from dataclasses import dataclass
from datetime import datetime
import re

@dataclass(frozen=True)
class SSHUser:
    """
    Represents an SSH user with a username and the timestamp of the last login.

    Attributes:
        username (str): The username of the SSH user.
        last_login (datetime | None): The timestamp of the last login, or None if never logged in.
    """
    username: str
    last_login: datetime | None

    def validate(self) -> bool:
        """
        Validate the username against the allowed SSH username pattern.

        Returns:
            bool: True if the username is valid, False otherwise.
        """
        return re.match(r"^[a-z_][a-z0-9_-]{0,31}$", self.username) is not None
