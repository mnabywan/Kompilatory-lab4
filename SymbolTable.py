#!/usr/bin/python


class Symbol(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Symbol: " + str(self.name)


class VariableSymbol(Symbol):
    def __init__(self, name, type, value=None):
        super().__init__(name)
        self.type = type
        self.value = value #i added it

    def __repr__(self):
        return "Variable symbol: " + str(self.name) + ", type: " + str(self.type)


class MatrixSymbol(VariableSymbol):
    def __init__(self, name, dimensions):
        super().__init__(name, 'matrix')
        self.dimensions = dimensions

    def __repr__(self):
        return str("Matrix symbol: " )#+ str(self.name) + ", dimensions: " + str(self.dimensions))


class SymbolTable(object):
    def __init__(self, parent, name):  # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.table = dict()

    def put(self, name, symbol):  # put variable symbol or fundef under <name> entry
        self.table.update({name: symbol})

    def get(self, name):  # get variable symbol or fundef from <name> entry
        return self.table.get(name, None)

    def getParentScope(self):
        return self.parent

    def pushScope(self, name):
        pass

    def popScope(self):
        pass


