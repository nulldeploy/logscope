# parse.py
from utils.level_styles import LEVEL_STYLES
from core.parser import parser_output
from core.parser import LogLine
from rich.console import Console
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
console = Console()


def get_lines(file: Path):
    list_object = parser_output(file)

    if list_object is None:
        logger.error('Some error, try again...')
        return

    return list_object

def display_logs(list_object: list[LogLine], level: str, grep: str, 
                 tail: int):
    found = False

    if tail:
        list_object = list_object[-tail:]

    for line_object in list_object:
        style = LEVEL_STYLES.get(line_object.level, 'white')

        if level and line_object.level != level:
            continue
        elif grep and grep not in line_object.message:
            continue
        else:
            found = True
            console.print(
                f"[dim]{line_object.date} {line_object.time}[/dim] "
                f"[{style}]{line_object.level:<5}[/{style}] "
                f"{line_object.message}"
            )

    if not found and (grep or level):
        logger.error('No matches founded for: %s', grep)
        return

def run(args) -> None:
    if not args.file.exists() or not args.file.is_file():
        logger.error('File does not exists or it is directory')
        return

    list_object = get_lines(args.file)
    display_logs(list_object, args.level, args.grep, args.tail)
