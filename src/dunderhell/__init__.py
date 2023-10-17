import math
import re


def build_number_under_8(number: int) -> str:
    eight = "__name__.__len__()"

    if number == 0:
        return f"({eight}).__sub__({eight})"

    one = f"({eight}.__floordiv__({eight}))"
    return ".__add__".join([one] * number)


def build_number(number: int) -> str:
    if number < 8:
        return build_number_under_8(number)

    eight = "(__name__.__len__())"  # note that it is bracketed now
    number_parts = []
    remainder = number
    while remainder >= 8:
        log = int(math.log(remainder, 8))
        # wrap this in brackets to ensure __mul__ happens before __add__
        power_of_8 = "(" + ".__mul__".join([eight] * log) + ")"
        number_parts.append(power_of_8)
        # we just created this power of 8, subtract to get remainder
        remainder -= 8**log

    # now remainder is under 8.
    if remainder > 0:
        number_parts.append(build_number_under_8(remainder))

    return ".__add__".join(number_parts)


def replace_number_with_dunders(match: re.Match[str]) -> str:
    """Grabs the matched number and dunderifies it."""
    number = int(match.group())
    return build_number(number)
