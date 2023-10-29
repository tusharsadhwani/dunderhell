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

# TODO: right now user defined functions, classes are not registered as a Store.
# So function names and invocations are not renamed.
# Also, if you do:
# def any(elems):
#    ...
# print(any([True, False]))
# it will use the builtin any instead of the function any.


# TODO: add test for global and nonlocal
# TODO: add test for overriding builtins
# TODO: add test for overriding builtins in a parent scope
# TODO: add test for listcomps and such as they define a scope
