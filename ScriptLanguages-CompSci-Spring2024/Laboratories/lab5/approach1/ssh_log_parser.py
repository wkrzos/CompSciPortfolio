from pathlib import Path
from loguru import logger
from ssh_log import LogEntry, MessageType

def read_log_file(file_path: Path):
    # Iterate over each line in the log file, creating a LogEntry object for each.
    for line in file_path.read_text().splitlines():
        log_entry = LogEntry.from_log(line)
        
        # Bind the log entry's context only once for all subsequent log messages.
        context_logger = logger.bind(
            timestamp=log_entry.timestamp,
            hostname=log_entry.hostname,
            app_component=log_entry.app_component,
            pid=log_entry.pid,
            event_description=log_entry.event_description,
            original_log_line=log_entry.original_log_line,
            size=log_entry.byte_size,
        )
        
        # Log the size of the log entry at debug level.
        context_logger.debug(f"Size: {log_entry.byte_size}b")
        
        # Define a mapping from MessageType to logging actions.
        log_actions = {
            MessageType.SUCCESSFUL_LOGIN: context_logger.info,
            MessageType.CONNECTION_CLOSED: context_logger.info,
            MessageType.FAILED_LOGIN: context_logger.warning,
            MessageType.BREAK_IN_ATTEMPT: context_logger.critical,
        }

        # Log the event description with the appropriate level based on the log type.
        if log_entry.type in log_actions:
            log_actions[log_entry.type](f"{log_entry.type.name.replace('_', ' ').capitalize()}: {log_entry.event_description}")
        
        yield log_entry
