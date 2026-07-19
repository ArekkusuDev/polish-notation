from typing import final, override


class ASTNode:
    pass


@final
class Assignment(ASTNode):
    def __init__(self, target: "Identifier", value: ASTNode):
        self.target = target
        self.value = value

    @override
    def __repr__(self) -> str:
        return f"Assignment({self.target}, {self.value})"


@final
class BinaryOp(ASTNode):
    def __init__(self, left: ASTNode, op: str, right: ASTNode):
        self.left = left
        self.op = op
        self.right = right

    @override
    def __repr__(self) -> str:
        return f"BinaryOp({self.left}, {self.op}, {self.right})"


@final
class UnaryOp(ASTNode):
    def __init__(self, op: str, operand: ASTNode):
        self.op = op
        self.operand = operand

    @override
    def __repr__(self) -> str:
        return f"UnaryOp({self.op}, {self.operand})"


@final
class Number(ASTNode):
    def __init__(self, value: int | float):
        self.value = value

    @override
    def __repr__(self) -> str:
        return f"Number({self.value})"


@final
class Identifier(ASTNode):
    def __init__(self, name: str):
        self.name = name

    @override
    def __repr__(self) -> str:
        return f"Identifier({self.name})"
