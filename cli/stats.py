# stats.py
from utils.level_styles import LEVEL_STYLES
from core.analyzer import analyze
from rich.console import Console
from rich.table import Table

console = Console()

def display_stats(stats):
    total, levels, errors = stats
    
    console.print(f'\n[bold]Total lines:[/bold] {total}\n')

    levels_table = Table(title='Log Levels')
    levels_table.add_column('Level', justify='left')
    levels_table.add_column('Count', justify='right')
    
    for level, count in levels.items():
        style = LEVEL_STYLES.get(level, 'white')
        levels_table.add_row(f'[{style}]{level}[/{style}]', str(count))
    
    console.print(levels_table)

    errors_table = Table(title='Top Errors')
    errors_table.add_column('Count', justify='right', style='bold red')
    errors_table.add_column('Message', justify='left')
    
    for message, count in errors:
        errors_table.add_row(str(count), message)
    
    console.print(errors_table)

def run(args) -> None:
    stats = analyze(args.file)
    display_stats(stats)