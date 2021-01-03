
class SymbolTable:
    class_table = {}
    subroutine_table = {}
    static_counter = int
    field_counter = int
    argument_counter = int
    var_counter = int

    def __init__(self):
        self.static_counter = 0
        self.field_counter = 0
        self.argument_counter = 0
        self.var_counter = 0

    def startSubroutine(self):
        if len(self.subroutine_table) != 0:
            self.subroutine_table.clear()
        self.var_counter = 0
        self.argument_counter = 0

    def define(self, name, type, kind, scope):
        if scope == "class":
            if kind == "static":
                self.class_table[name] = {"type": type, "kind": kind, "idx": self.static_counter}
                self.static_counter +=1
            else:
                self.class_table[name] = {"type": type, "kind": kind, "idx": self.field_counter}
                self.field_counter +=1
        else:
            if kind == "argument":
                self.subroutine_table[name] = {"type": type, "kind": kind, "idx": self.argument_counter}
                self.argument_counter +=1
            else:
                self.subroutine_table[name] = {"type": type, "kind": kind, "idx": self.var_counter}
                self.var_counter +=1

    def varCount(self, kind):
        if kind == "static":
            return self.static_counter
        elif kind == "field":
            return self.field_counter
        elif kind == "argument":
            return self.argument_counter
        else: return self.var_counter

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