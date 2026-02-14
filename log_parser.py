"""
Log Parser
----------
Parses Apache/Nginx combined log format into structured dictionaries.

Extracted fields:
- ip_address
- timestamp (datetime object)
- method
- url
- status_code
- user_agent
"""

import re
from datetime import datetime


# Combined Log Format Regex
LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) '              # IP Address
    r'\S+ \S+ '                  # Remote logname + user (ignored)
    r'\[(?P<time>.*?)\] '        # Timestamp
    r'"(?P<method>\S+) '         # HTTP Method
    r'(?P<url>\S+) '             # URL
    r'\S+" '                     # Protocol
    r'(?P<status>\d{3}) '        # Status Code
    r'\S+ '                      # Bytes (ignored)
    r'"[^"]*" '                  # Referrer (ignored)
    r'"(?P<agent>[^"]*)"'        # User Agent
)


def parse_timestamp(timestamp_str: str) -> datetime:
    """
    Convert Apache log timestamp into Python datetime.
    Example: 10/Oct/2000:13:55:36 +0000
    """
    return datetime.strptime(timestamp_str, "%d/%b/%Y:%H:%M:%S %z")


def parse_log_line(line: str) -> dict | None:
    """
    Parse a single log line.
    Returns structured dict or None if invalid.
    """
    match = LOG_PATTERN.match(line)
    if not match:
        return None

    try:
        return {
            "ip_address": match.group("ip"),
            "timestamp": parse_timestamp(match.group("time")),
            "method": match.group("method"),
            "url": match.group("url"),
            "status_code": int(match.group("status")),
            "user_agent": match.group("agent")
        }
    except Exception:
        return None


def parse_log_file(file_obj) -> list:
    """
    Parse entire log file.
    Returns list of structured entries.
    """
    parsed_entries = []

    for line in file_obj:
        if isinstance(line, bytes):
            line = line.decode("utf-8", errors="ignore")

        entry = parse_log_line(line.strip())
        if entry:
            parsed_entries.append(entry)

    return parsed_entries
