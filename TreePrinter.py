# from __future__ import print_function
# # import AST
# # import string
# #
# # def addToClass(cls):
# #
# #     def decorator(func):
# #         setattr(cls,func.__name__,func)
# #         return func
# #     return decorator
# #
# # class TreePrinter:
# #
# #     INDENT = "|  "
# #
# #     @classmethod
# #     def print_indented(cls, str1, indent):
# #         print(TreePrinter.INDENT * indent + str1)
# #
# #     @addToClass(AST.Node)
# #     def printTree(self, indent=0):
# #         raise Exception("printTree not defined in class " + self.__class__.__name__)
# #
# #
# #     @addToClass(AST.Program)
# #     def printTree(self, indent=0):
# #         self.statements.printTree(indent)
# #
# #
# #     @addToClass(AST.Statements)
# #     def printTree(self, indent=0):
# #         for statment in self.statements:
# #             statment.printTree(indent)
# #
# #     @addToClass(AST.Assignment)
# #     def printTree(self, indent=0):
# #         self.op.printTree(indent)
# #         self.var.printTree(indent+1)
# #         self.expr.printTree(indent+1)
# #
# #     @addToClass(AST.Expressions)
# #     def printTree(self, indent=0):
# #         for i in self.expressions:
# #             i.printTree(indent)
# #
# #     @addToClass(AST.Assignment_Op)
# #     def printTree(self, indent):
# #         TreePrinter.print_indented(self.op, indent)
# #
# #
# #     @addToClass(AST.Variable)
# #     def printTree(self, indent=0):
# #         TreePrinter.print_indented(self.var, indent)
# #
# #     @addToClass(AST.Const)
# #     def printTree(self, indent=0):
# #         TreePrinter.print_indented(str(self.val), indent)
# #
# #     @addToClass(AST.BinExpr)
# #     def printTree(self, indent):
# #         TreePrinter.print_indented(self.op, indent)
# #         self.expr1.printTree(indent)
# #         self.expr2.printTree(indent+1)
# #
# #     @addToClass(AST.RelExpr)
# #     def printTree(self, indent=0):
# #         TreePrinter.print_indented(self.op, indent)
# #         self.expr1.printTree(indent)
# #         self.expr2.printTree(indent+1)
# #
# #     @addToClass(AST.CurlyBracketsStatement)
# #     def printTree(self, indent=0):
# #         self.statement.printTree(indent)
# #
# #     @addToClass(AST.MatrixOperation)
# #     def printTree(self, indent=0):
# #         TreePrinter.print_indented(self.op, indent)
# #         self.matrix1.printTree(indent)
# #         self.matrix2.printTree(indent)
# #
# #     @addToClass(AST.MatrixFunction)
# #     def printTree(self, indent=0):
# #         TreePrinter.print_indented(self.type, indent)
# #         self.expr.printTree(indent+1)
# #
# #     @addToClass(AST.MatrixTransposed)
# #     def printTree(self, indent=0):
# #         TreePrinter.print_indented("TRANSPOSE", indent)
# #         self.matrix.printTree(indent)
# #
# #     @addToClass(AST.MinusMatrix)
# #     def printTree(self, indent=0):
# #         TreePrinter.print_indented("MINUS", indent)
# #         self.matrix.printTree(indent)
# #
# #     @addToClass(AST.Matrix)
# #     def printTree(self, indent):
# #         self.val.printTree(indent+1)
# #
# #     @addToClass(AST.If_statement)
# #     def printTree(self, indent=0):
# #         TreePrinter.print_indented("IF", indent)
# #         self.cond.printTree(indent+1)
# #         TreePrinter.print_indented("THEN", indent)
# #         self.stat1.printTree(indent+1)
# #         TreePrinter.print_indented("ELSE", indent)
# #         self.stat2.printTree(indent + 1)
# #         # if self.stat2 is not None:
# #         #     print("DUPPPPPPPPAAAAAAAAAA")
# #         #     TreePrinter.print_indented("ELSE", indent)
# #         #     self.stat2.printTree(indent+1)
# #
# #     @addToClass(AST.While)
# #     def printTree(self, indent=0):
# #         TreePrinter.print_indented("WHILE", indent)
# #         self.cond.printTree(indent+1)
# #         self.stat.printTree(indent+1)
# #
# #
# #     @addToClass(AST.For)
# #     def printTree(self, indent=0):
# #         TreePrinter.print_indented("FOR", indent)
# #         self.id.printTree(indent+1)
# #         self.range.printTree(indent+1)
# #         self.stat.printTree(indent+1)
# #
# #     @addToClass(AST.Range)
# #     def printTree(self, indent=0):
# #         TreePrinter.print_indented("RANGE", indent)
# #         self.expr1.printTree(indent+1)
# #         self.expr2.printTree(indent)
# #
# #     @addToClass(AST.Return)
# #     def printTree(self, indent=0):
# #         TreePrinter.print_indented("RETURN", indent)
# #         self.expr.printTree(indent+1)
# #
# #     @addToClass(AST.Print)
# #     def printTree(self, indent=0):
# #         TreePrinter.print_indented("PRINT", indent)
# #         self.const.printTree(indent+1)
# #
# #     @addToClass(AST.Break)
# #     def printTree(self, indent=0):
# #         TreePrinter.print_indented("BREAK", indent)
# #
# #     @addToClass(AST.Continue)
# #     def printTree(self, indent=0):
# #         TreePrinter.print_indented("CONTINUE", indent)
# #
# #
# #     @addToClass(AST.Expressions)
# #     def printTree(self, indent=0):
# #         for e in self.expressions:
# #             e.printTree(indent)
# #
# #     @addToClass(AST.Vector)
# #     def printTree(self, indent=0):
# #         TreePrinter.print_indented("VECTOR", indent)
# #         for expr in self.list_expr:
# #             expr.printTree(indent+1)
# #
# #     @addToClass(AST.VectorRow)
# #     def printTree(self, indent):
# #         for row in self.vector_row1:
# #             row.printTree(indent)
# #
# #     @addToClass(AST.RefVar)
# #     def printTree(self, indent):
# #         TreePrinter.print_indented("REF", indent)
# #         self.var.printTree(indent + 1)
# #         self.list.printTree(indent+1)
# #
# #     @addToClass(AST.Error)
# #     def printTree(self, indent=0):
# #         pass

from __future__ import print_function
import AST
import string

def addToClass(cls):

    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator

class TreePrinter:

    INDENT = "|  "

    @classmethod
    def print_indented(cls, str1, indent=0):
        print(TreePrinter.INDENT * indent + str1)

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)


    @addToClass(AST.Program)
    def printTree(self, indent=0):
        self.statements.printTree(indent)


    @addToClass(AST.Statements)
    def printTree(self, indent=0):
        for statement in self.statements:
            statement.printTree(indent)

    @addToClass(AST.Assignment)
    def printTree(self, indent=0):
        self.op.printTree(indent)
        self.var.printTree(indent+1)
        self.expr.printTree(indent+1)

    @addToClass(AST.Expressions)
    def printTree(self, indent=0):
        for i in self.expressions:
            i.printTree(indent)

    @addToClass(AST.Assignment_Op)
    def printTree(self, indent=0):
        TreePrinter.print_indented(self.op, indent)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        TreePrinter.print_indented(self.var, indent)

    @addToClass(AST.Const)
    def printTree(self, indent=0):
        TreePrinter.print_indented(str(self.val), indent)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        TreePrinter.print_indented(self.op, indent)
        self.expr1.printTree(indent+1)
        self.expr2.printTree(indent+1)

    @addToClass(AST.RelExpr)
    def printTree(self, indent=0):
        TreePrinter.print_indented(self.op, indent)
        self.expr1.printTree(indent+1)
        self.expr2.printTree(indent+1)

    @addToClass(AST.CurlyBracketsStatement)
    def printTree(self, indent=0):
        self.statement.printTree(indent)

    @addToClass(AST.MatrixOperation)
    def printTree(self, indent=0):
        TreePrinter.print_indented(self.op, indent)
        self.matrix1.printTree(indent+1)
        self.matrix2.printTree(indent+1)

    @addToClass(AST.MatrixFunction)
    def printTree(self, indent=0):
        TreePrinter.print_indented(self.type, indent)
        self.expr.printTree(indent+1)

    @addToClass(AST.MatrixTransposed)
    def printTree(self, indent=0):
        TreePrinter.print_indented("TRANSPOSE", indent)
        self.matrix.printTree(indent+1)

    @addToClass(AST.MinusMatrix)
    def printTree(self, indent=0):
        TreePrinter.print_indented("MINUS", indent)
        self.matrix.printTree(indent+1)

    @addToClass(AST.Matrix)
    def printTree(self, indent=0):
        self.val.printTree(indent)

    @addToClass(AST.If_statement)
    def printTree(self, indent=0):
        TreePrinter.print_indented("IF", indent)
        self.cond.printTree(indent+1)
        TreePrinter.print_indented("THEN", indent)
        self.stat1.printTree(indent+1)
        if self.stat2:
            TreePrinter.print_indented("ELSE", indent)
            self.stat2.printTree(indent+1)

    @addToClass(AST.While)
    def printTree(self, indent=0):
        TreePrinter.print_indented("WHILE", indent)
        self.cond.printTree(indent+1)
        self.stat.printTree(indent+1)


    @addToClass(AST.For)
    def printTree(self, indent=0):
        TreePrinter.print_indented("FOR", indent)
        self.id.printTree(indent+1)
        self.range.printTree(indent+1)
        self.stat.printTree(indent+1)

    @addToClass(AST.Range)
    def printTree(self, indent=0):
        TreePrinter.print_indented("RANGE", indent)
        self.expr1.printTree(indent+1)
        self.expr2.printTree(indent+1)

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        TreePrinter.print_indented("RETURN", indent)
        self.expr.printTree(indent+1)

    @addToClass(AST.Print)
    def printTree(self, indent=0):
        TreePrinter.print_indented("PRINT", indent)
        self.const.printTree(indent+1)

    @addToClass(AST.Break)
    def printTree(self, indent=0):
        TreePrinter.print_indented("BREAK", indent)

    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        TreePrinter.print_indented("CONTINUE", indent)


    @addToClass(AST.Expressions)
    def printTree(self, indent=0):
        for e in self.expressions:
            e.printTree(indent)

    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        TreePrinter.print_indented("VECTOR", indent)
        for expr in self.list_expr:
            expr.printTree(indent+1)

    @addToClass(AST.VectorRow)
    def printTree(self, indent=0):
        for row in self.vector_row1:
            row.printTree(indent)

    @addToClass(AST.RefVar)
    def printTree(self, indent=0):
        TreePrinter.print_indented("REF", indent)
        self.var.printTree(indent+1)
        self.list.printTree(indent+1)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass