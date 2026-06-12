# logscope.py
import argparse
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def setup_logging(verbose: bool):
    level = logging.DEBUG if verbose else logging.INFO 
    logging.basicConfig(
        level=level,
        format='%(asctime)s  %(levelname)-8s  %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='LogScope DevOps script',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--verbose', '-v', action='store_true')

    subparsers = parser.add_subparsers(dest='command', metavar='COMMAND')
    subparsers.required = True

    p = subparsers.add_parser('parse')
    p.add_argument('--file', '-f', type=Path)
    p.add_argument('--level', '-l', choices=['ERROR', 'WARN', 'INFO'])
    p.add_argument('--grep', '-g', type=str)
    p.add_argument('--tail', '-t', type=int)

    p = subparsers.add_parser('stats')
    p.add_argument('--file', '-f', type=Path)

    p = subparsers.add_parser('serve')

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()

    setup_logging(args.verbose)

    if args.command == 'parse':
        from cli.parse import run
        run(args)
    elif args.command == 'stats':
        from cli.stats import run
        run(args)
    elif args.command == 'serve':
        from cli.serve import run
        run(args)

if __name__ == '__main__':
    main()
