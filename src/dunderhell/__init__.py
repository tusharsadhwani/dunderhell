import ast
import math
from textwrap import dedent


def dunderify(tree: ast.AST) -> ast.AST:
    """Turn Python code into dunders."""
    visitors = [
        StringVisitor(),
        NumberVisitor(),
        OpVisitor(),
    ]

    for visitor in visitors:
        visitor.visit(tree)

    ast.fix_missing_locations(tree)
    return tree


class StringVisitor(ast.NodeTransformer):
    """
    Converts strings into bunch of `__chr__()` calls.
    Defines a top level `__chr__` if needed.

    Input:
        x = 'foo'
        print(x)

    Output:
        __chr__ = __builtins__.__getattribute__(
            __name__.__reduce__.__name__[6]
            + __name__.__add__.__class__.__name__[3]
            + __name__.__class__.__name__[-1]
        )
        x = __chr__(102) + __chr__(111) + __chr__(111)
        print(x)
    """

    def __init__(self) -> None:
        chr_tree = ast.parse(
            dedent(
                """
                __chr__ = __builtins__.__getattribute__(
                    __name__.__reduce__.__name__[6]
                    + __name__.__add__.__class__.__name__[3]
                    + __name__.__class__.__name__[-1]
                )
                """
            )
        )
        self.chr_definition = chr_tree.body[0]
        self.string_found = False

    @staticmethod
    def create_chr(character: str) -> ast.Call:
        """Creates a `__chr__()` call from a character eg. 'a' -> __chr__(97)."""
        char_number = ord(character)
        return ast.Call(
            func=ast.Name("__chr__"),
            args=[ast.Constant(char_number)],
            keywords=[],
        )

    def visit_Constant(self, node: ast.Constant) -> ast.expr:
        super().generic_visit(node)

        if not isinstance(node.value, str):
            return node

        string = node.value
        self.string_found = True

        # If single character, can return just the one __chr__(N) call
        if len(string) == 1:
            self.create_chr(string)

        # Otherwise we need to create a BinOp tree
        chr_nodes = [self.create_chr(character) for character in string]

        binop_tree = chr_nodes[0]
        for node in chr_nodes[1:]:
            binop_tree = ast.BinOp(binop_tree, ast.Add(), node)

        return binop_tree

    def visit_Module(self, node: ast.Module) -> ast.Module:
        super().generic_visit(node)

        if self.string_found:
            node.body.insert(0, self.chr_definition)

        return node


class NumberVisitor(ast.NodeTransformer):
    """
    Converts numbers into dunders.

    Input:
        print(2 + 2)

    Output:
        print(
            __name__.__len__() // __name__.__len__()
            + __name__.__len__() // __name__.__len__()
            + (
                __name__.__len__() // __name__.__len__()
                + __name__.__len__() // __name__.__len__()
            )
        )
    """

    # TODO


class OpVisitor(ast.NodeTransformer):
    """
    Converts operators into dunders.

    Input:
        foo = 5
        print(-3 + 5*9)

    Output:
        foo = 5
        print((3).__neg__().__add__(foo.__mul__(9)))
    """

    # TODO


def _build_number_under_8(number: int) -> str:
    eight = "__name__.__len__()"

    if number == 0:
        return f"({eight}).__sub__({eight})"

    one = f"({eight}.__floordiv__({eight}))"
    return ".__add__".join([one] * number)


def _build_number(number: int) -> str:
    if number < 8:
        return _build_number_under_8(number)

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
        number_parts.append(_build_number_under_8(remainder))

    return ".__add__".join(number_parts)
