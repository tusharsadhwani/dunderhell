import ast
import math
from textwrap import dedent
from typing import Sequence, Type


def dunderify(tree: ast.AST) -> None:
    """Turn Python code into dunders."""
    visitors = [
        StringVisitor(),
        NumberVisitor(),
        OpVisitor(),
    ]

    for visitor in visitors:
        visitor.visit(tree)

    ast.fix_missing_locations(tree)


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
        return make_binop(ast.Add(), chr_nodes)

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

    # __name__.__len__() == 8
    eight = ast.Call(
        func=ast.Attribute(ast.Name(id="__name__"), attr="__len__"),
        args=[],
        keywords=[],
    )
    # eight // eight == 1
    one = ast.BinOp(eight, ast.FloorDiv(), eight)
    # eight - eight == 0
    zero = ast.BinOp(eight, ast.Sub(), eight)

    @classmethod
    def build_number_under_8(cls, number: int) -> ast.expr:
        if number == 0:
            return cls.zero

        return make_binop(ast.Add(), [cls.one] * number)

    @classmethod
    def build_number(cls, number: int) -> ast.expr:
        if number < 8:
            return cls.build_number_under_8(number)

        number_parts: list[ast.expr] = []
        remainder = number
        while remainder >= 8:
            log_8 = int(math.log(remainder, 8))
            # Create a power of 8 by doing 8*8*8*..., `log_8` times
            eight_tree = make_binop(ast.Mult(), [cls.eight] * log_8)
            number_parts.append(eight_tree)
            # we just created this power of 8, subtract to get remainder
            remainder -= 8**log_8

        # now remainder is under 8.
        if remainder > 0:
            number_parts.append(cls.build_number_under_8(remainder))

        # Now we need to add all the parts together
        return make_binop(ast.Add(), number_parts)

    def visit_Constant(self, node: ast.Constant) -> ast.expr:
        super().generic_visit(node)

        if not isinstance(node.value, int):
            return node

        number = node.value
        return self.build_number(number)


class OpVisitor(ast.NodeTransformer):
    """
    Converts unary, binary and comparison operators into dunders.
    AST node mapping created from `stdlib/_ast.pyi` in typeshed.

    `is` and `is not` are not supported, those are in `IsVisitor`.
    Boolean operators are also not supported, those are in `BoolVisitor`.

    Input:
        foo = 5
        print(-3 + 5*9)

    Output:
        foo = 5
        print((3).__neg__().__add__(foo.__mul__(9)))
    """

    bin_op_map: dict[Type[ast.operator], str] = {
        ast.Add: "__add__",
        ast.BitAnd: "__and__",
        ast.BitOr: "__or__",
        ast.BitXor: "__xor__",
        ast.Div: "__div__",
        ast.FloorDiv: "__floordiv__",
        ast.LShift: "__lshift__",
        ast.Mod: "__mod__",
        ast.Mult: "__mul__",
        ast.MatMult: "__matmul__",
        ast.Pow: "__pow__",
        ast.RShift: "__rshift__",
        ast.Sub: "__sub__",
    }

    # TODO: `not` has to be special cased. Put that in `BoolVisitor`.
    unary_op_map: dict[Type[ast.unaryop], str] = {
        ast.Invert: "__invert__",
        ast.UAdd: "__pos__",
        ast.USub: "__neg__",
    }

    # TODO: `is` and `is not` have to be special cased turning `x is y` into
    # `id(x) == id(y)`, and put in a visitor that runs before `OpVisitor`.
    cmp_op_map: dict[Type[ast.cmpop], str] = {
        ast.Eq: "__eq__",
        ast.Gt: "__gt__",
        ast.GtE: "__ge__",
        ast.In: "__contains__",
        ast.Lt: "__lt__",
        ast.LtE: "__le__",
        ast.NotEq: "__ne__",
        ast.NotIn: "__contains__",  # is special cased in the visitor
    }

    @staticmethod
    def call_method(node: ast.expr, method: str, args: Sequence[ast.expr]) -> ast.Call:
        """
        Wraps given expression in a method call.
        eg. if `method` is '__add__', returns `<node>.__add__(*args)`.

        One edge case: returns BoolOp nodes if comparisons have multiple operators.
        eg. `x < y < z` returns `x.__lt__(y) and y.__lt__(z)`.
        """
        return ast.Call(
            func=ast.Attribute(node, attr=method),
            args=args,
            keywords=[],
        )

    def visit_UnaryOp(self, node: ast.UnaryOp) -> ast.expr:
        super().generic_visit(node)
        if isinstance(node.op, ast.Not):
            # These can't be turned into a dunder directly.
            return node

        dunder_name = self.unary_op_map[type(node.op)]
        return self.call_method(node.operand, dunder_name, args=[])

    def visit_BinOp(self, node: ast.BinOp) -> ast.expr:
        super().generic_visit(node)

        dunder_name = self.bin_op_map[type(node.op)]
        return self.call_method(node.left, dunder_name, args=[node.right])

    def visit_Compare(self, node: ast.Compare) -> ast.expr:
        super().generic_visit(node)

        if any(isinstance(op, (ast.Is, ast.IsNot)) for op in node.ops):
            # These can't be turned into a dunder directly.
            # If you're using `IsVisitor` before `OpVisitor`, this should never be hit.
            return node

        parts: list[ast.expr] = []
        # Create `(a<b), (b<c), (c<d), ...` etc. in `parts`
        for op, (idx, right) in zip(node.ops, enumerate(node.comparators), strict=True):
            if idx == 0:
                left = node.left
            else:
                left = node.comparators[idx - 1]

            op_type = type(op)
            dunder_name = self.cmp_op_map[op_type]
            if op_type in (ast.In, ast.NotIn):
                # `in` and `not in` have reversed semantics
                comparison: ast.expr = self.call_method(right, dunder_name, args=[left])
                # `not in` must be wrapped in `not`.
                if op_type == ast.NotIn:
                    comparison = ast.UnaryOp(ast.Not(), comparison)
            else:
                comparison = self.call_method(left, dunder_name, args=[right])

            parts.append(comparison)

        # Return `(a<b) and (b<c) and (c<d) and ...`
        return ast.BoolOp(ast.And(), parts)


def make_binop(op: ast.operator, exprs: Sequence[ast.expr]) -> ast.expr:
    """
    Builds a BinOp tree joining the `exprs` with the given `op`.
    For eg. if `op` is `ast.Add()`, returns AST node for `expr1 + expr2 + ...`.
    """
    expr_tree, *exprs = exprs
    for expr in exprs:
        expr_tree = ast.BinOp(expr_tree, op, expr)

    return expr_tree
