import datetime
import pytest
from ipaddress import IPv4Address
from SSHLogEntry import SSHLogEntry, SSHRejectedPassword, SSHAcceptedPassword, SSHErrorLogEntry, OtherSSHLogEntry, MessageType
from SSHLogJournal import SSHLogJournal


# Test for verifying the extraction of timestamp
def test_timestamp_extraction():
    log_line = "May 17 12:30:00 myhost sshd[12345]: Failed password for invalid user testuser from 192.168.0.1 port 22 ssh2"
    log_entry = SSHRejectedPassword(log_line)
    current_year = datetime.datetime.now().year
    expected_timestamp = datetime.datetime.strptime(f"{current_year} May 17 12:30:00", "%Y %b %d %H:%M:%S")
    assert log_entry.timestamp_with_current_year == expected_timestamp


# Test for verifying correct IPv4 address extraction
def test_valid_ipv4_extraction():
    log_line = "Dec 10 06:55:48 LabSZ sshd[24200]: Failed password for invalid user webmaster from 173.234.31.186 port 38926 ssh2"
    log_entry = SSHRejectedPassword(log_line)
    assert log_entry.extract_ipv4() == IPv4Address("173.234.31.186")


# Test for verifying invalid IPv4 address extraction
def test_invalid_ipv4_extraction():
    log_line = "Dec 10 06:55:48 LabSZ sshd[24200]: Failed password for invalid user webmaster from 666.777.88.213 port 38926 ssh2"
    log_entry = SSHRejectedPassword(log_line)
    assert log_entry.extract_ipv4() is None


# Test for verifying the absence of IPv4 address
def test_no_ipv4_extraction():
    log_line = "Dec 10 06:55:48 LabSZ sshd[24200]: Failed password for invalid user webmaster from unknown port 38926 ssh2"
    log_entry = SSHRejectedPassword(log_line)
    assert log_entry.extract_ipv4() is None


# Parameterized test for verifying append() method of SSHLogJournal
@pytest.mark.parametrize("log_line, expected_type", [
    ("May 17 12:30:00 myhost sshd[12345]: Failed password for invalid user testuser from 192.168.0.1 port 22 ssh2", SSHRejectedPassword),
    ("May 17 12:35:00 myhost sshd[12346]: Accepted password for validuser from 192.168.0.2 port 22 ssh2", SSHAcceptedPassword),
    ("May 17 12:40:00 myhost sshd[12347]: error: Could not load host key: /etc/ssh/ssh_host_ed25519_key", SSHErrorLogEntry),
    ("May 17 12:45:00 myhost sshd[12348]: Connection closed by 192.168.0.3 port 22", OtherSSHLogEntry),
])
def test_append_method(log_line, expected_type):
    journal = SSHLogJournal()
    journal.append(log_line)
    assert isinstance(journal._ssh_log_entries[-1], expected_type)
