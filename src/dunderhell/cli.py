"""CLI interface for dunderhell."""
import ast
import sys

from dunderhell import dunderify


def error(message: str) -> None:
    """Print error message."""
    print(f"\033[31mError:\033[m", message, file=sys.stderr)


def cli() -> int:
    # TODO: use argparse
    filename = sys.argv[1]
    try:
        with open(filename) as file:
            contents = file.read()
    except OSError as exc:
        error(f"Unable to read {filename}: {exc.strerror}")
        return 2

    try:
        tree = ast.parse(contents)
    except ValueError as exc:
        error(f"Unable to parse {filename} as file contains null bytes")
        return 4
    except SyntaxError as exc:
        error(f"Unable to parse {filename}:{exc.lineno}:{exc.offset} - {exc.msg}")
        return 3

    dunderify(tree)
    # TODO: add --in-place flag to write to file
    print(ast.unparse(tree))
    return 0
