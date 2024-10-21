import datetime
from ipaddress import IPv4Address
from SSHLogEntry import MessageType, OtherSSHLogEntry, SSHAcceptedPassword, SSHErrorLogEntry, SSHLogEntry, SSHRejectedPassword
from SSHLogJournal import SSHLogJournal
from SSHUser import SSHUser

def test_ssh_user():
    print("Testing SSHUser validation...")
    
    # Test valid usernames
    valid_users = [
        SSHUser(username="validuser", last_login=datetime.datetime.now()),
        SSHUser(username="another_valid_user", last_login=None),
        SSHUser(username="user123", last_login=datetime.datetime(2023, 5, 17, 12, 30)),
    ]
    
    # Test invalid usernames
    invalid_users = [
        SSHUser(username="InvalidUser", last_login=None),
        SSHUser(username="123user", last_login=None),
        SSHUser(username="user@domain", last_login=None),
    ]
    
    for user in valid_users:
        assert user.validate(), f"User {user.username} should be valid"
        print(f"User {user.username} is valid")

    for user in invalid_users:
        assert not user.validate(), f"User {user.username} should be invalid"
        print(f"User {user.username} is invalid")

def test_ssh_log_journal():
    print("Testing SSHLogJournal functionalities...")
    
    journal = SSHLogJournal()
    
    # Sample log entries
    logs = [
        "May 17 12:30:00 myhost sshd[12345]: Failed password for invalid user testuser from 192.168.0.1 port 22 ssh2",
        "May 17 12:35:00 myhost sshd[12346]: Accepted password for validuser from 192.168.0.2 port 22 ssh2",
        "May 17 12:40:00 myhost sshd[12347]: error: Could not load host key: /etc/ssh/ssh_host_ed25519_key",
        "May 17 12:45:00 myhost sshd[12348]: Connection closed by 192.168.0.3 port 22"
    ]
    
    for log in logs:
        journal.append(log)
    
    assert len(journal) == 4, "There should be 4 log entries in the journal"
    print("All logs appended successfully.")
    
    # Test log retrieval by index
    assert journal[0].event_description.startswith("Failed password"), "First log entry should be a failed password"
    print("Log retrieval by index works.")
    
    # Test log retrieval by datetime
    current_year = datetime.datetime.now().year
    test_datetime = datetime.datetime.strptime(f"{current_year} May 17 12:35:00", "%Y %b %d %H:%M:%S")
    logs_by_datetime = list(journal[test_datetime])
    assert len(logs_by_datetime) == 1, "There should be 1 log entry with the given datetime"
    print("Log retrieval by datetime works.")
    
    # Test log retrieval by IPv4
    test_ip = IPv4Address("192.168.0.2")
    logs_by_ip = list(journal[test_ip])
    assert len(logs_by_ip) == 1, "There should be 1 log entry with the given IP address"
    print("Log retrieval by IPv4 address works.")
    
def main():
    test_ssh_user()
    test_ssh_log_journal()
    
if __name__ == "__main__":
    main()