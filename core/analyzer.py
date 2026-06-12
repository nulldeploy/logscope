# analyzer.py
from core.parser import parser_output
from collections import Counter
from pathlib import Path
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

def analyze(file: Path):
    parsed = parser_output(file)

    total = len(parsed)
    levels = Counter()
    messages = []

    for item in parsed:
        levels[item.level] += 1

        if item.level == 'ERROR':
            messages.append(item.message)
            c = Counter(messages)
            errors = c.most_common()
    
    return total, levels, errors