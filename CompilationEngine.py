import JackTokenizer
import SymbolTable
import sys
import os
SPACE = "  "
TYPE = {"int" , "char" , "boolean", "Array"}
STATEMENTS = {"if", "let", "while", "do", "return"}
OP = {"+" : "+", "-" : "-", "*" : "*", "/" : "/", "&" : "&amp;", "|" : "|", "<" : "&lt;", ">" : "&gt;", "=" : "="}
UN_OP = {"-", "~"}
KEY_CONST = {"true", "false", "null", "this"}
class CompilationEngine:
    tokens = JackTokenizer
    my_file_string = str
    taber = str
    className = str
    subRoutineName = str
    cur_scope = str
    cur_kind = str
    cur_type = str
    sym_table = SymbolTable
    def __init__(self, tokens_type):
        self.tokens = tokens_type
        self.sym_table = SymbolTable.SymbolTable()

    def compileClass(self):
        if self.tokens.getToken() == "class":
            self.my_file_string = "<class>\n"
            self.taber = SPACE
            self.my_file_string = self.my_file_string+ self.taber + "<" + self.tokens.tokenType() + "> " + self.tokens.getToken() +\
                                  " </" + self.tokens.tokenType() + ">" + "\n"
            self.tokens.advance()
            if self.tokens.tokenType() == "identifier":
                self.className = self.tokens.getToken()
                self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " +\
                                      self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                self.tokens.advance()
            else: return False
            if self.tokens.getToken() == '{':
                self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                      self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                self.tokens.advance()
            else: return False
            classVarDecIndicator = self.compileClassVarDec()
            subroutineDecIndicator = self.compileSubroutineDec()
            if classVarDecIndicator or subroutineDecIndicator:
                if self.tokens.getToken() == "}":
                    self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                          self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                else: return False
            else: return False
        else: return False
        self.my_file_string = self.my_file_string + "</class>\n"


    def compileClassVarDec(self):
        self.cur_scope = "class"
        if self.tokens.getToken() == "field" or self.tokens.getToken() == "static":

            while self.tokens.getToken() == "field" or self.tokens.getToken() == "static":
                self.cur_kind = self.tokens.getToken()
                self.my_file_string = self.my_file_string + self.taber + "<classVarDec>\n"
                self.taber = self.taber + SPACE
                self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                self.tokens.advance()
                if self.tokens.getToken() in TYPE or self.tokens.getToken() == self.className \
                        or self.tokens.tokenType() == "identifier":
                    self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                          self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                    self.cur_type = self.tokens.getToken()
                    self.tokens.advance()
                else: return False
                if self.tokens.tokenType() == "identifier":
                    self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                          self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                    self.sym_table.define(self.tokens.getToken(), self.cur_type, self.cur_kind, self.cur_scope)
                    self.tokens.advance()
                else: return False
                while self.tokens.getToken() != ";":
                    self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                          self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                    if self.tokens.tokenType() != "symbol":
                        self.sym_table.define(self.tokens.getToken(), self.cur_type, self.cur_kind, self.cur_scope)
                    self.tokens.advance()
                self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                      self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                self.tokens.advance()
                self.taber = self.taber[0:-2]
                self.my_file_string = self.my_file_string + self.taber + "</classVarDec>\n"
            print(self.cur_scope)
            for i in self.sym_table.class_table.keys():
                print("Name: " + i, end=", ")
                print("Type: " + self.sym_table.class_table[i]["type"], end=", ")
                print("Kind: " + self.sym_table.class_table[i]["kind"], end=", ")
                print("Index: ", end="")
                print(self.sym_table.class_table[i]["idx"])
            return True
        else: return False

    def compileSubroutineDec(self):
        if not self.tokens.getToken() == "constructor" and not self.tokens.getToken() == "function" \
                and not self.tokens.getToken() == "method":
            return False
        while self.tokens.getToken() == "constructor" or self.tokens.getToken() == "function" \
            or self.tokens.getToken() == "method":
            self.my_file_string = self.my_file_string + self.taber + "<subroutineDec>\n"
            self.taber = self.taber + SPACE
            self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
            self.tokens.advance()
            if self.tokens.getToken() == "void" or self.tokens.getToken() in TYPE or\
                            self.tokens.getToken() == self.className:
                self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                      self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
            else: return False
            self.tokens.advance()
            if self.tokens.tokenType() == "identifier":
                self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                        self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                self.subRoutineName = self.tokens.getToken()
                self.cur_scope = self.tokens.getToken()
                self.sym_table.startSubroutine()
            else: return False
            self.tokens.advance()
            if self.tokens.getToken() == "(":
                    self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                          self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
            else: return False
            self.tokens.advance()
            if not self.compileParameterList():
                return False
            if self.tokens.getToken() == ")":
                    self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                          self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
            else: return False
            self.tokens.advance()
            if not self.compileSubroutineBody():
                return False
            self.taber = self.taber[0:-2]
            self.my_file_string = self.my_file_string + self.taber + "</subroutineDec>\n"
            print(self.cur_scope)
            for i in self.sym_table.subroutine_table.keys():
                print("Name: " + i, end=", ")
                print("Type: " + self.sym_table.subroutine_table[i]["type"], end=", ")
                print("Kind: " + self.sym_table.subroutine_table[i]["kind"], end=", ")
                print("Index: ", end="")
                print(self.sym_table.subroutine_table[i]["idx"])
        return True

    def compileParameterList(self):
        self.my_file_string = self.my_file_string + self.taber +"<parameterList>\n"
        if self.tokens.getToken() in TYPE:
            self.cur_kind = "argument"
            self.taber = self.taber + "  "
            while self.tokens.getToken() in TYPE:
                if self.tokens.getToken() in TYPE:
                    self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                          self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                    self.cur_type = self.tokens.getToken()
                    self.tokens.advance()
                if self.tokens.tokenType() == "identifier":
                    self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                          self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                    self.sym_table.define(self.tokens.getToken(), self.cur_type, self.cur_kind, self.cur_scope)
                    self.tokens.advance()
                else: return False
                if self.tokens.getToken() == ",":
                    self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                          self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                    self.tokens.advance()
                    continue
                elif self.tokens.getToken() == ")":
                    self.taber = self.taber[0:-2]
                    self.my_file_string = self.my_file_string + self.taber + "</parameterList>\n"
                    return True
                else: return False
        elif self.tokens.getToken() == ")":
            self.my_file_string = self.my_file_string + self.taber + "</parameterList>\n"
            return True
        else: return False

    def compileSubroutineBody(self):
        self.my_file_string = self.my_file_string + self.taber + "<subroutineBody>\n"
        if self.tokens.getToken() == '{':
            self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
            self.tokens.advance()
        else: return False
        if not self.compileVarDec(): # To add space to taber
            return False
        if not self.compileStatements():  # To add space to taber
            return False
        if self.tokens.getToken() == '}':
            self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
            self.tokens.advance()
        else: return False
        self.my_file_string = self.my_file_string + self.taber + "</subroutineBody>\n"
        return True

    def compileVarDec(self):
        if self.tokens.getToken() == "var":
            self.cur_scope = self.subRoutineName
            self.cur_kind = self.tokens.getToken()
            while self.tokens.getToken() == "var":
                self.my_file_string = self.my_file_string + self.taber + "<varDec>\n"
                self.taber = self.taber + "  "
                self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                      self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                self.tokens.advance()
                if self.tokens.getToken() in TYPE or self.tokens.getToken() == self.className\
                        or self.tokens.tokenType() == "identifier":
                    self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                          self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                    self.cur_type = self.tokens.getToken()
                    self.tokens.advance()
                else: return False
                if self.tokens.tokenType() == "identifier":
                    self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                          self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                    self.sym_table.define(self.tokens.getToken(), self.cur_type, self.cur_kind, self.cur_scope)
                    self.tokens.advance()
                else: return False
                while self.tokens.getToken() != ";":
                    if self.tokens.getToken() == ",":
                        self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                              self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                        self.tokens.advance()
                    else: return False
                    if self.tokens.tokenType() == "identifier":
                        self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                              self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                        self.sym_table.define(self.tokens.getToken(), self.cur_type, self.cur_kind, self.cur_scope)
                        self.tokens.advance()
                    else: return False
                self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                      self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                self.tokens.advance()
                self.taber = self.taber[0:-2]
                self.my_file_string = self.my_file_string + self.taber + "</varDec>\n"

            return True
        else: return True


    def compileStatements(self):
        self.my_file_string = self.my_file_string + self.taber + "<statements>\n"
        self.taber = self.taber + "  "
        while self.tokens.getToken() in STATEMENTS:
            if not self.compileIf():
                return False
            if not self.compileLet():
                return False
            if not self.compileWhile():
                return False
            if not self.compileDo():
                return False
            if not self.compileReturn():
                return False
        self.taber = self.taber[0:-2]
        self.my_file_string = self.my_file_string + self.taber + "</statements>\n"
        return True

    def compileLet(self):
        if self.tokens.getToken() == "let":
            self.my_file_string = self.my_file_string + self.taber + "<letStatement>\n"
            self.taber = self.taber + "  "
            self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
            self.tokens.advance()
        else: return True
        if self.tokens.tokenType() == "identifier":
            self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
            self.tokens.advance()
        else: return False
        if self.tokens.getToken() == "[":
            self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
            self.tokens.advance()
            if not self.compileExpression():
                return False
            if self.tokens.getToken() == "]":
                self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                      self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                self.tokens.advance()
            else: return False
        if self.tokens.getToken() == "=":
            self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
            self.tokens.advance()
        else: return False
        if not self.compileExpression():
            return False
        if self.tokens.getToken() == ";":
            self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
            self.tokens.advance()

        self.taber = self.taber[0:-2]
        self.my_file_string = self.my_file_string + self.taber + "</letStatement>\n"
        return True

    def compileIf(self):
        if self.tokens.getToken() == "if":
            self.my_file_string = self.my_file_string + self.taber + "<ifStatement>\n"
            self.taber = self.taber + "  "
            self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
            self.tokens.advance()
        else: return True
        if self.tokens.getToken() == "(":
            self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
            self.tokens.advance()
        else: return False
        if not self.compileExpression():
            return False
        if self.tokens.getToken() == ")":
            self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
            self.tokens.advance()
        else: return False
        if self.tokens.getToken() == "{":
            self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
            self.tokens.advance()
        else: return False
        if not self.compileStatements():
            return False
        if self.tokens.getToken() == "}":
            self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
            self.tokens.advance()
        else: return False
        if self.tokens.getToken() == "else":
            self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
            self.tokens.advance()
            if self.tokens.getToken() == "{":
                self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                      self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                self.tokens.advance()
            else: return False
            if not self.compileStatements():
                return False
            if self.tokens.getToken() == "}":
                self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                      self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                self.tokens.advance()
            else: return False
        else:
            self.taber = self.taber[0:-2]
            self.my_file_string = self.my_file_string + self.taber + "</ifStatement>\n"
            return True
        self.taber = self.taber[0:-2]
        self.my_file_string = self.my_file_string + self.taber + "</ifStatement>\n"
        return True

    def compileWhile(self):
        if self.tokens.getToken() == "while":
            self.my_file_string = self.my_file_string + self.taber + "<whileStatement>\n"
            self.taber = self.taber + "  "
            self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
            self.tokens.advance()
            if self.tokens.getToken() == "(":
                self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                      self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                self.tokens.advance()
            if not self.compileExpression():
                return False
            if self.tokens.getToken() == ")":
                self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                      self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                self.tokens.advance()
            else: return False
            if self.tokens.getToken() == "{":
                self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                      self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                self.tokens.advance()
                if not self.compileStatements():
                    return False
                if self.tokens.getToken() == "}":
                    self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                          self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                    self.tokens.advance()
                else: return False
            else: return False
            self.taber = self.taber[0:-2]
            self.my_file_string = self.my_file_string + self.taber + "</whileStatement>\n"
            return True
        else: return True

    def compileDo(self):
        if self.tokens.getToken() == "do":
            self.my_file_string = self.my_file_string + self.taber + "<doStatement>\n"
            self.taber = self.taber + "  "
            self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
            self.tokens.advance()
            if not self.compileSubroutineCall():
                return False
            if self.tokens.getToken() == ";":
                self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                      self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                self.tokens.advance()
            else: return False
            self.taber = self.taber[0:-2]
            self.my_file_string = self.my_file_string + self.taber + "</doStatement>\n"
            return True
        else: return True

    def compileReturn(self):
        if self.tokens.getToken() == "return":
            self.my_file_string = self.my_file_string + self.taber + "<returnStatement>\n"
            self.taber = self.taber + "  "
            self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
            self.tokens.advance()
            if self.tokens.getToken() != ";" and not self.compileExpression():
                return False
            if self.tokens.getToken() == ";":
                self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                      self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                self.tokens.advance()
            else: return False
            self.taber = self.taber[0:-2]
            self.my_file_string = self.my_file_string + self.taber + "</returnStatement>\n"
            return True
        else: return True

    def compileExpression(self):
        self.my_file_string = self.my_file_string + self.taber + "<expression>\n"
        self.taber = self.taber + "  "
        if not self.compileTerm():
            return False
        while self.tokens.getToken() in OP:
            self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  OP[self.tokens.getToken()] + " </" + self.tokens.tokenType() + ">" + "\n"
            self.tokens.advance()
            if not self.compileTerm():
                return False
        self.taber = self.taber[0:-2]
        self.my_file_string = self.my_file_string + self.taber + "</expression>\n"
        return True

    def compileTerm(self):
        termIndicator = 0
        self.my_file_string = self.my_file_string + self.taber + "<term>\n"
        self.taber = self.taber + "  "
        if self.tokens.tokenType() == "integerConstant" or self.tokens.tokenType() == "stringConstant" \
                or self.tokens.getToken() in KEY_CONST:
            termIndicator = 1
            self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
            self.tokens.advance()
        elif self.tokens.tokenType() == "identifier" and self.tokens.getToken() != self.subRoutineName and \
                self.tokens.peek() != ".":
            termIndicator = 1
            self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
            self.tokens.advance()
            if self.tokens.getToken() == "[":
                self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                      self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                self.tokens.advance()
                if not self.compileExpression():
                    return False
                if self.tokens.getToken() == "]":
                    self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                          self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                    self.tokens.advance()
                else: return False
        elif self.tokens.getToken() == self.subRoutineName or self.tokens.tokenType() == "identifier":
            termIndicator = 1
            if not self.compileSubroutineCall():
                return False
        elif self.tokens.getToken() == "(":
            termIndicator = 1
            self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
            self.tokens.advance()
            if not self.compileExpression():
                return False
            if self.tokens.getToken() == ")":
                self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                      self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                self.tokens.advance()
            else: return False
        elif self.tokens.getToken() in UN_OP:
            termIndicator = 1
            self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
            self.tokens.advance()
            if not self.compileTerm():
                return False
        if termIndicator == 0:
            return False
        self.taber = self.taber[0:-2]
        self.my_file_string = self.my_file_string + self.taber + "</term>\n"
        return True

    def compileExpressionList(self):
        self.my_file_string = self.my_file_string + self.taber + "<expressionList>\n"
        self.taber = self.taber + "  "
        if self.tokens.getToken() == ")":
            self.taber = self.taber[0:-2]
            self.my_file_string = self.my_file_string + self.taber + "</expressionList>\n"
            return True
        if not self.compileExpression():
            return False
        while self.tokens.getToken() == ",":
            if self.tokens.getToken() == ",":
                self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                self.tokens.advance()
            if not self.compileExpression():
                return False
        self.taber = self.taber[0:-2]
        self.my_file_string = self.my_file_string + self.taber + "</expressionList>\n"
        return True


    def compileSubroutineCall(self):
        if self.tokens.getToken() == self.subRoutineName or self.tokens.tokenType() == "identifier" \
                and self.tokens.peek() != ".":
            self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
            self.tokens.advance()
            if self.tokens.getToken() == "(":
                self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                      self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                self.tokens.advance()
                if not self.compileExpressionList():
                    return False
                if self.tokens.getToken() == ")":
                    self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                          self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                    self.tokens.advance()
                else: return False
            else: return False
        elif self.tokens.getToken() == self.className or self.tokens.tokenType() == "identifier":
            self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
            self.tokens.advance()
            if self.tokens.getToken() == ".":
                self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                      self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                self.tokens.advance()
            else: return False
            if self.tokens.getToken() == self.subRoutineName or self.tokens.tokenType() == "identifier":
                self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                      self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                self.tokens.advance()
            else: return False
            if self.tokens.getToken() == "(":
                self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                      self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                self.tokens.advance()
                if not self.compileExpressionList():
                    return False
                if self.tokens.getToken() == ")":
                    self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                          self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                    self.tokens.advance()
                else: return False
            else: return False
        else: return True
        return True