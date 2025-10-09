from typing import Union


class ASTNode:
    pass


class Assignment(ASTNode):
    def __init__(self, target: "Identifier", value: ASTNode):
        self.target = target
        self.value = value

    def __repr__(self) -> str:
        return f"Assignment({self.target}, {self.value})"


class BinaryOp(ASTNode):
    def __init__(self, left: ASTNode, op: str, right: ASTNode):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self) -> str:
        return f"BinaryOp({self.left}, {self.op}, {self.right})"


class UnaryOp(ASTNode):
    def __init__(self, op: str, operand: ASTNode):
        self.op = op
        self.operand = operand

    def __repr__(self) -> str:
        return f"UnaryOp({self.op}, {self.operand})"


class Number(ASTNode):
    def __init__(self, value: Union[int, float]):
        self.value = value

    def __repr__(self) -> str:
        return f"Number({self.value})"


class Identifier(ASTNode):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self) -> str:
        return f"Identifier({self.name})"
