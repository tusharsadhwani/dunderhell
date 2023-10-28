import ast

class SomeVisitor(ast.NodeVisitor):
    ...

def dunderify(__tree__: ast.AST) -> None:
    __visitors__ = [SomeVisitor()]
    for __visitor__ in __visitors__:
        __visitor__.visit(__tree__)
    ast.fix_missing_locations(__tree__)
