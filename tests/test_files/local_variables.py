import ast


class SomeVisitor(ast.NodeVisitor):
    ...


def dunderify(tree: ast.AST) -> None:
    visitors = [
        SomeVisitor(),
    ]

    for visitor in visitors:
        visitor.visit(tree)

    ast.fix_missing_locations(tree)


# TODO: add test for global and nonlocal
# TODO: add test for listcomps and such
