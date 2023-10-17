"""CLI interface for dunderhell."""
import re
import sys

from dunderhell import replace_number_with_dunders


def cli() -> None:
    filename = sys.argv[1]
    with open(filename) as file:
        contents = file.read()

    # for every match, `replace_number_with_dunders()` will be called
    # and the returned string will be substituted in the string
    new_code = re.sub(r"\d+", replace_number_with_dunders, contents)
    print(new_code)


if __name__ == "__main__":
    cli()
