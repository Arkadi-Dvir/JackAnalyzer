
class SymbolTable:
    class_table = {}
    subroutine_table = {}
    static_counter = 0
    field_counter = 0
    argument_counter = 0
    var_counter = 0

    def __init__(self):
        print("start")

    def startSubroutine(self):
        if len(self.subroutine_table) != 0:
            self.subroutine_table.clear()

    def define(self, name, type, kind, scope):
        if scope == "class":
            self.class_table[name] = {"type": type, "kind": kind, "idx": 0}
        else:
            self.subroutine_table[name] = {"type": type, "kind": kind, "idx": 0}
        self.varCount(kind)

    def varCount(self, kind):
        if kind == "static":
            self.static_counter += 1
        elif kind == "field":
            self.field_counter += 1
        elif kind == "argument":
            self.argument_counter += 1
        else: self.var_counter += 1

    def kindOf(self, name):
        if name in self.class_table:
            return self.class_table[name]["kind"]
        else: return self.subroutine_table[name]["kind"]

    def typeOf(self, name):
        if name in self.class_table:
            return self.class_table[name]["type"]
        else: return self.subroutine_table[name]["type"]

    def indexOf(self, name):
        if name in self.class_table:
            return self.class_table[name]["idx"]
        else: return self.subroutine_table[name]["idx"]