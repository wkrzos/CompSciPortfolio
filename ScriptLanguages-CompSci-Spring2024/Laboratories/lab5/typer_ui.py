import typer
from typing import Optional
import logging
import sys

from ssh_log_parser import read_log_file, estimate_session_durations, execute_ipv4_extraction, execute_user_extraction, execute_message_type_identification, execute_random_logs, execute_frequent_users_analysis

app = typer.Typer()

def setup_logging(log_level: str):
    logger = logging.getLogger()
    try:
        log_level = log_level.upper()
        logging_level = getattr(logging, log_level)
    except AttributeError:
        typer.echo(f"Invalid log level: {log_level}")
        raise typer.Exit(code=1)
    logger.setLevel(logging_level)

@app.command()
def ipv4s(log_file: str):
    """Extract IPv4 addresses from logs."""
    log_entries = read_log_file(log_file)
    for entry in log_entries:
        typer.echo(execute_ipv4_extraction(entry))

@app.command()
def user(log_file: str):
    """Extract user information from logs."""
    log_entries = read_log_file(log_file)
    for entry in log_entries:
        typer.echo(execute_user_extraction(entry))

@app.command()
def message_type(log_file: str):
    """Classify log messages."""
    log_entries = read_log_file(log_file)
    for entry in log_entries:
        typer.echo(execute_message_type_identification(entry))

@app.command()
def get_random_logs(log_file: str, number: int = 1):
    """Get random log entries for a user."""
    log_entries = read_log_file(log_file)
    for entry in execute_random_logs(log_entries, number):
        typer.echo
