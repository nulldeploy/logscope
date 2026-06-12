# parser.py
from dataclasses import dataclass
from core.reader import read_file
from pathlib import Path
import re


@dataclass
class LogLine:
    date: str
    time: str
    level: str
    message: str
    raw: str

LOG_PATTERN = re.compile(
    r'(?P<date>\d{4}-\d{2}-\d{2})'
    r'\s+'
    r'(?P<time>\d{2}:\d{2}:\d{2})'
    r'\s+'
    r'(?P<level>ERROR|WARN|INFO)'
    r'\s+'
    r'(?P<message>.*)'
)

def parse_line(raw: str) -> LogLine | None:
    match = LOG_PATTERN.search(raw)

    if not match:
        return None

    return LogLine(
        date=match.group('date'),
        time=match.group('time'),
        level=match.group('level'),
        message=match.group('message'),
        raw=raw
    )

def parser_output(file: Path) -> list[LogLine] | None:
    raw = read_file(file)

    parsed_lines = []
    for line in raw:
        result = parse_line(line)
        if result is None:
            continue
        else:
            parsed_lines.append(result)

    return parsed_lines