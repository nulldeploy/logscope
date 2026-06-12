# reader.py
from pathlib import Path

def read_file(file: Path) -> list[str]:
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return lines