#!/usr/bin/python
import AST
import SymbolTable
# types
INTEGER = 'int'
FLOAT = 'float'
BOOL = 'bool'
STRING = 'string'
VECTOR = 'vector'
MATRIX = 'matrix'

#  operators
arithmetic = ['+', '-', '*', '/']
assign = ['+=', '-=', '*=', '/=']
matrix = ['.+', '.-', '.*', './']
relational = ['>', '>=', '<', '<=', '==', '!=']


class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

    # simpler version of generic_visit, not so general
    # def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)


class Operation(object):
    def __init__(self):
        # key - operator, value - list of first operand, second operand and product
        self.allowed_types = dict()

        for operator in arithmetic + assign:
            self.allowed_types[operator] = [INTEGER, INTEGER, INTEGER]
            self.allowed_types[operator] = [FLOAT, FLOAT, FLOAT]
            self.allowed_types[operator] = [INTEGER, FLOAT, FLOAT]
            self.allowed_types[operator] = [FLOAT, INTEGER, FLOAT]

        for operator in matrix:
            self.allowed_types[operator] = [VECTOR, VECTOR, VECTOR]
            self.allowed_types[operator] = [MATRIX, MATRIX, MATRIX]
            self.allowed_types[operator] = [VECTOR, INTEGER, VECTOR]
            self.allowed_types[operator] = [INTEGER, VECTOR, VECTOR]
            self.allowed_types[operator] = [VECTOR, FLOAT, VECTOR]
            self.allowed_types[operator] = [FLOAT, VECTOR, VECTOR]
            self.allowed_types[operator] = [MATRIX, INTEGER, MATRIX]
            self.allowed_types[operator] = [INTEGER, MATRIX, MATRIX]
            self.allowed_types[operator] = [MATRIX, FLOAT, MATRIX]
            self.allowed_types[operator] = [FLOAT, MATRIX, MATRIX]

        for operator in relational:
            self.allowed_types[operator] = [INTEGER, INTEGER]
            self.allowed_types[operator] = [FLOAT, FLOAT]
            self.allowed_types[operator] = [INTEGER, FLOAT]
            self.allowed_types[operator] = [FLOAT, INTEGER]

    def are_types_correct(self, left_operand, operator, right_operand):
        print(operator)

        if operator in self.allowed_types \
                and left_operand.type in self.allowed_types[operator][0] \
                and right_operand.type in self.allowed_types[operator][1]:
            return True
        else:
            return False

    def get_product_type(self, left_operand, operator, right_operand):
        for operands in self.allowed_types[operator]:
            if operands[0] == left_operand and operands[1] == right_operand:
                return operands[2]

    @staticmethod
    def are_dimensions_correct(left_operand, operator, right_operand):
        if operator == '=':
            return True
        if operator in ['+', '-', '-=', '+='] + matrix:
            if left_operand.dimensions == right_operand.dimensions:
                return True
        if operator == '*':
            if left_operand.dimensions[1] == right_operand.dimensions[0]:
                return True
        if operator == '/':  # assuming A/B == A*B^(-1)
            if left_operand.dimensions[1] == right_operand.dimensions[0] \
                    and right_operand.dimensions[0] == right_operand.dimensions[1]:
                return True
        return False


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.table = SymbolTable.SymbolTable(None, 'Program')
        self.operations = Operation()
        # used to determine whether break or continue is inside any loop
        # indicate number of currently nested loops
        self.inside_loops = 0

    def visit_Program(self, node):
        self.visit(node.statements)

    def visit_Statements(self, node):
        for statement in node.statements:
            self.visit(statement)

    def visit_If_statement(self, node):
        self.visit(node.cond)
        self.visit(node.stat1)
        self.visit(node.stat2)

    def visit_While(self, node):
        self.visit(node.cond)
        self.inside_loops += 1
        self.visit(node.stat)
        self.inside_loops -= 1

    def visit_For(self, node):
        self.visit(node.id)
        self.visit(node.range)
        self.inside_loops += 1
        self.visit(node.stat)
        self.inside_loops -= 1

    def visit_Print(self, node):
        if node.const is not None:
            self.visit(node.const)

    def visit_Break(self, node):
        if self.inside_loops <= 0:
            print("Line {0}: BREAK outside loop function".format(1))

    def visit_Return(self, node):
        if node.expr is not None:
            self.visit(node.expr)

    def visit_Continue(self, node):
        if self.inside_loops <= 0:
            print("Line {0}: CONTINUE outside loop function".format(1))

    def visit_Range(self, node):
        self.visit(node.expr1)
        self.visit(node.expr2)

    def visit_BinExpr(self, node):
        operator = node.op
        left_part = self.visit(node.expr1)
        right_part = self.visit(node.expr2)
        product_type = None
        if self.operations.are_types_correct(left_part, operator, right_part):
            product_type = self.operations.get_product_type(left_part, operator, right_part)
            if product_type is MATRIX:
                if Operation.are_dimensions_correct(left_part, operator, right_part):
                    dimensions = [left_part.dimensions[0], right_part.dimensions[1]]
                    return SymbolTable.MatrixSymbol(None, dimensions)
                else:
                    print(
                        "Line {0}: Wrong dimensions in binary expression: {1} {2} {3}"
                            .format(node.lineno, str(left_part), operator, str(right_part)))
                    return SymbolTable.MatrixSymbol(None, None)
        else:
            print("Line {0}: Types in binary expression are incorrect: {1} {2} {3}"
                    .format(1, str(left_part), operator, str(right_part)))
        return SymbolTable.VariableSymbol(None, product_type)

    def visit_Variable(self, node):
        variable = self.table.get(node.var)
        if variable is None:
            new_variable = SymbolTable.VariableSymbol(node.var, None)
            self.table.put(node.var, new_variable)
            return new_variable
        else:
            return variable

    def visit_Const(self, node):
        return 'int'

    def visit_Expressions(self, node):
        if node.expressions is not None:
            for expression in node.expressions:
                self.visit(expression)

    def visit_Matrix(self, node):
        matrix = self.table.get(node.val)
        if matrix is None:
            new_matrix = SymbolTable.MatrixSymbol(node.val, None)
            self.table.put(node.val, new_matrix)
            return new_matrix
        else:
            return matrix

    def visit_MatrixOperation(self, node):
        type1 = self.table.get(node.matrix1)
        type2 = self.table.get(node.matrix1)
        if type1 != type2:
            print('Error: matrix operation on incompatible types:', type1, type2, 'here:', node.matrix1, node.op, node.matrix2)

    def visit_MatrixFunction(self, node):
        dim1_type = self.visit(node.expr)
        dim2_type = dim1_type
        if node.expr2:
            expr2_type = self.visit(node.expr2)
        if dim1_type != 'int':
            print('Line {}: Matrix initialization with illegal dims type: {}'.format(node.line, dim1_type))
            return 'unknown'
        if dim2_type != 'int':
            print('Line {}: Matrix initialization with illegal dims type: {}'.format(node.line, dim2_type))
            return 'unknown'
        return 'matrix'

    def visit_MinusMatrix(self, node):
        self.visit(node.matrix)

    def visit_MatrixTransposed(self, node):
        self.visit(node.matrix)

    def visit_Assignment(self, node):
        right_part = self.visit(node.expr)
        op = self.visit(node.op)
        if isinstance(node.var, AST.Variable):
            self.table.put(node.var, SymbolTable.VariableSymbol(node.var, right_part, node.expr))
            # if not self.operations.are_types_correct(left_part, op, right_part):
            #     print("Error in assignment visit")
        elif isinstance(node.var, AST.RefVar):
            pass

        else:
            print("error in assignment")

    def visit_Assignment_Op(self, node):
        return node.op

    def visit_RelExpr(self, node):
        left_part = self.visit(node.expr1)
        right_part = self.visit(node.expr2)
        op = node.op

        if not self.operations.are_types_correct(left_part, op, right_part):
            print("Error in rel expr")

    def visit_CurlyBracketsStatement(self, node):
        self.visit(node.statement)


# #!/usr/bin/python
# import AST
# import SymbolTable
#
# # types
# INTEGER = 'int'
# FLOAT = 'float'
# BOOL = 'bool'
# STRING = 'string'
# VECTOR = 'vector'
# MATRIX = 'matrix'
#
# #  operators
# arithmetic = ['+', '-', '*', '/']
# assign = ['+=', '-=', '*=', '/=']
# matrix = ['.+', '.-', '.*', './']
# relational = ['>', '>=', '<', '<=', '==', '!=']
#
#
# class NodeVisitor(object):
#     def visit(self, node):
#         method = 'visit_' + node.__class__.__name__
#         visitor = getattr(self, method, self.generic_visit)
#         return visitor(node)
#
#     def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
#         if isinstance(node, list):
#             for elem in node:
#                 self.visit(elem)
#         else:
#             for child in node.children:
#                 if isinstance(child, list):
#                     for item in child:
#                         if isinstance(item, AST.Node):
#                             self.visit(item)
#                 elif isinstance(child, AST.Node):
#                     self.visit(child)
#
#     # simpler version of generic_visit, not so general
#     # def generic_visit(self, node):
#     #    for child in node.children:
#     #        self.visit(child)
#
#
# class Operation(object):
#     def __init__(self):
#         # key - operator, value - list of first operand, second operand and product
#         self.allowed_types = dict()
#
#         for operator in arithmetic + assign:
#             self.allowed_types[operator] = [INTEGER, INTEGER, INTEGER]
#             self.allowed_types[operator] = [FLOAT, FLOAT, FLOAT]
#             self.allowed_types[operator] = [INTEGER, FLOAT, FLOAT]
#             self.allowed_types[operator] = [FLOAT, INTEGER, FLOAT]
#
#         for operator in matrix:
#             self.allowed_types[operator] = [VECTOR, VECTOR, VECTOR]
#             self.allowed_types[operator] = [MATRIX, MATRIX, MATRIX]
#             self.allowed_types[operator] = [VECTOR, INTEGER, VECTOR]
#             self.allowed_types[operator] = [INTEGER, VECTOR, VECTOR]
#             self.allowed_types[operator] = [VECTOR, FLOAT, VECTOR]
#             self.allowed_types[operator] = [FLOAT, VECTOR, VECTOR]
#             self.allowed_types[operator] = [MATRIX, INTEGER, MATRIX]
#             self.allowed_types[operator] = [INTEGER, MATRIX, MATRIX]
#             self.allowed_types[operator] = [MATRIX, FLOAT, MATRIX]
#             self.allowed_types[operator] = [FLOAT, MATRIX, MATRIX]
#
#         for operator in relational:
#             self.allowed_types[operator] = [INTEGER, INTEGER]
#             self.allowed_types[operator] = [FLOAT, FLOAT]
#             self.allowed_types[operator] = [INTEGER, FLOAT]
#             self.allowed_types[operator] = [FLOAT, INTEGER]
#
#     def are_types_correct(self, left_operand, operator, right_operand):
#         if operator in self.allowed_types \
#                 and left_operand.type in self.allowed_types[operator][0] \
#                 and right_operand.type in self.allowed_types[operator][1]:
#             return True
#         else:
#             return False
#
#     def get_product_type(self, left_operand, operator, right_operand):
#         for operands in self.allowed_types[operator]:
#             if operands[0] == left_operand and operands[1] == right_operand:
#                 return operands[2]
#
#     @staticmethod
#     def are_dimensions_correct(left_operand, operator, right_operand):
#         if operator == '=':
#             return True
#         if operator in ['+', '-', '-=', '+='] + matrix:
#             if left_operand.dimensions == right_operand.dimensions:
#                 return True
#         if operator == '*':
#             if left_operand.dimensions[1] == right_operand.dimensions[0]:
#                 return True
#         if operator == '/':  # assuming A/B == A*B^(-1)
#             if left_operand.dimensions[1] == right_operand.dimensions[0] \
#                     and right_operand.dimensions[0] == right_operand.dimensions[1]:
#                 return True
#         return False
#
#
# class TypeChecker(NodeVisitor):
#     def __init__(self):
#         self.table = SymbolTable.SymbolTable(None, 'Program')
#         self.operations = Operation()
#         # used to determine whether break or continue is inside any loop
#         # indicate number of currently nested loops
#         self.inside_loops = 0
#
#     def visit_Program(self, node):
#         self.visit(node.statements)
#
#     def visit_Statements(self, node):
#         for statement in node.statements:
#             self.visit(statement)
#
#     def visit_If_statement(self, node):
#         self.visit(node.cond)
#         self.visit(node.stat1)
#         self.visit(node.stat2)
#
#     def visit_While(self, node):
#         self.visit(node.condition)
#         self.inside_loops += 1
#         self.visit(node.stat)
#         self.inside_loops -= 1
#
#     def visit_For(self, node):
#         self.visit(node.id)
#         self.visit(node.range)
#         self.inside_loops += 1
#         self.visit(node.stat)
#         self.inside_loops -= 1
#
#     def visit_Print(self, node):
#         if node.const is not None:
#             self.visit(node.const)
#
#     def visit_Break(self, node):
#         if self.inside_loops <= 0:
#             print("Line {0}: BREAK outside loop function".format(node.lineno))
#
#     def visit_Return(self, node):
#         if node.expr is not None:
#             self.visit(node.expr)
#
#     def visit_Continue(self, node):
#         if self.inside_loops <= 0:
#             print("Line {0}: CONTINUE outside loop function".format(node.lineno))
#
#     def visit_Range(self, node):
#         self.visit(node.expr1)
#         self.visit(node.expr2)
#
#     def visit_BinExpr(self, node):
#         operator = node.op
#         left_part = self.visit(node.expr1)
#         right_part = self.visit(node.expr2)
#         product_type = None
#         if self.operations.are_types_correct(left_part, operator, right_part):
#             product_type = self.operations.get_product_type(left_part, operator, right_part)
#             if product_type is MATRIX:
#                 if Operation.are_dimensions_correct(left_part, operator, right_part):
#                     dimensions = [left_part.dimensions[0], right_part.dimensions[1]]
#                     return SymbolTable.MatrixSymbol(None, dimensions)
#                 else:
#                     print(
#                         "Line {0}: Wrong dimensions in binary expression: {1} {2} {3}"
#                             .format(node.lineno, str(left_part), operator, str(right_part)))
#                     return SymbolTable.MatrixSymbol(None, None)
#         else:
#             print(
#                 "Line {0}: Types in binary expression are incorrect: {1} {2} {3}"
#                     .format(node.lineno, str(left_part), operator, str(right_part)))
#         return SymbolTable.VariableSymbol(None, product_type)
#
#     def visit_Variable(self, node):
#         variable = self.table.get(node.name)
#         if variable is None:
#             new_variable = SymbolTable.VariableSymbol(node.name, None)
#             self.table.put(node.name, new_variable)
#             return new_variable
#         else:
#             return variable
#
#     def visit_Expressions(self, node):
#         if node.expressions is not None:
#             for expression in node.expressions:
#                 self.visit(expression)
#
#
