
class Node(object):
    def __str__(self):
        return self.printTree()

    def accept(self, visitor):
        return visitor.visit(self)


class Program(Node):
    def __init__(self, statements):
        self.statements = statements


class Statements(Node):
    def __init__(self, statement):
        self.statements = [statement]


class If_statement(Node):
    def __init__(self, cond, stat1, stat2=None):
        self.cond = cond
        self.stat1 = stat1
        self.stat2 = stat2


class While(Node):
    def __init__(self, cond, stat):
        self.cond = cond
        self.stat = stat


class For(Node):
    def __init__(self, id, range, stat):
        self.id  = id
        self.range = range
        self.stat = stat


class Print(Node):
    def __init__(self, const):
        self.const = const


class Break(Node):
    def __init__(self):
        pass


class Return(Node):
    def __init__(self, expr):
        self.expr = expr


class Continue(Node):
    def __init__(self):
        pass


class CurlyBracketsStatement:
    def __init__(self, statement):
        self.statement = statement


class Range(Node):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2


class RelExpr(Node):
    def __init__(self, expr1, op, expr2):
        self.expr1 = expr1
        self.op = op
        self.expr2 = expr2


class Assignment(Node):
    def __init__(self, var, op, expr):
        self.var = var
        self.op = op
        self.expr = expr


class Assignment_Op:
    def __init__(self,  op ):
        self.op = op


class BinExpr(Node):
    def __init__(self, expr1, op, expr2):
        self.expr1 = expr1
        self.op = op
        self.expr2 = expr2


class Variable(Node):
    def __init__(self, var):
        self.var = var


class Expressions(Node):
    def __init__(self, expressions):
        self.expressions = [expressions]


class Const(Node):
    def __init__(self, val):
        self.val = val


class RefVar(Node):
    def __init__(self, var, list):
        self.var = var
        self.list = list


class MatrixFunction(Node):
    def __init__(self, type, expr, expr2=None):
        self.type = type
        self.expr = expr
        self.expr2 = expr2


class MatrixOperation(Node):
    def __init__(self, matrix1, op, matrix2):
        self.matrix1 = matrix1
        self.op = op
        self.matrix2 = matrix2


class Matrix(Node):
    def __init__(self, val):
        self.val = val


class MinusMatrix(Node):
    def __init__(self, matrix):
        self.matrix = matrix


class MatrixTransposed(Node):
    def __init__(self, matrix):
        self.matrix = matrix


class Vector(Node):
    def __init__(self, list_expr):
        self.list_expr = [list_expr]


class VectorRow(Node):
    def __init__(self, vector_row):
        self.vector_row1 = [vector_row]


class Error(Node):
    def __init__(self):
        pass