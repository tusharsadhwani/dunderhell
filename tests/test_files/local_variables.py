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


print(eval(ast.unparse(ast.parse("1 + 2"))))

# TODO: add test for global and nonlocal
# TODO: add test for overriding builtins
# TODO: add test for overriding builtins in a parent scope
# TODO: add test for listcomps and such as they define a scope
