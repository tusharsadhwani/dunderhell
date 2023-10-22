"""CLI interface for dunderhell."""
import ast
import sys

from dunderhell import dunderify


def error(message: str) -> None:
    """Print error message."""
    print(f"\033[31mError:\033[m", message)


def cli() -> None:
    # TODO: use argparse
    filename = sys.argv[1]
    with open(filename) as file:
        contents = file.read()

    try:
        tree = ast.parse(contents)
    except (ValueError, SyntaxError) as exc:
        error(f"Unable to parse {filename}: {exc}")

    dunderified_tree = dunderify(tree)
    # TODO: add --in-place flag to write to file
    print(ast.unparse(dunderified_tree))


if __name__ == "__main__":
    cli()
