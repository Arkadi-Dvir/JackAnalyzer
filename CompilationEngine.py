import JackTokenizer
import SymbolTable
import VMWriter
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
    cur_subRoutineType = str
    sym_table = SymbolTable
    vmWriter = VMWriter
    while_counter = int
    if_counter = int
    def __init__(self, tokens_type, vm_writer):
        self.while_counter = 0
        self.if_counter = 0
        self.tokens = tokens_type
        self.sym_table = SymbolTable.SymbolTable()
        self.vmWriter = vm_writer

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
            return True
        else: return False

    def compileSubroutineDec(self):
        if not self.tokens.getToken() == "constructor" and not self.tokens.getToken() == "function" \
                and not self.tokens.getToken() == "method":
            return False
        while self.tokens.getToken() == "constructor" or self.tokens.getToken() == "function" \
            or self.tokens.getToken() == "method":
            self.cur_subRoutineType = self.tokens.getToken()
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
        nVar = 0
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
                    nVar +=1
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
                        nVar +=1
                        self.tokens.advance()
                    else: return False
                self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                      self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                self.tokens.advance()
                self.taber = self.taber[0:-2]
                self.my_file_string = self.my_file_string + self.taber + "</varDec>\n"
            #####################################################
            name = self.className + "." + self.cur_scope
            self.vmWriter.writeFunction(name, str(nVar))
            if self.cur_subRoutineType == "constructor":
                self.vmWriter.writePush("constant", len(self.sym_table.class_table))
                self.vmWriter.writeCall("Memory.alloc",1)
                self.vmWriter.writePop("pointer",0)
            if self.cur_subRoutineType == "method":
                self.vmWriter.writePush("argument", 0)
                self.vmWriter.writePop("pointer",0)
            ####################################################
            return True
        else:
            #####################################################
            name = self.className + "." + self.cur_scope
            self.vmWriter.writeFunction(name, str(nVar))
            if self.cur_subRoutineType == "constructor":
                self.vmWriter.writePush("constant", len(self.sym_table.class_table))
                self.vmWriter.writeCall("Memory.alloc", 1)
                self.vmWriter.writePop("pointer", 0)
            if self.cur_subRoutineType == "method":
                self.vmWriter.writePush("argument", 0)
                self.vmWriter.writePop("pointer", 0)
                ####################################################
            return True


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
        cur_var = str
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
            ################################
            cur_var = self.tokens.getToken()
            #################################
            self.tokens.advance()
        else: return False
        if self.tokens.getToken() == "[":
            self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
            self.tokens.advance()
            if not self.compileExpression():
                return False
            #####################################
            if cur_var in self.sym_table.subroutine_table:
                self.vmWriter.writePop(self.sym_table.subroutine_table[cur_var]["kind"], self.sym_table.subroutine_table[cur_var]["idx"])
            else:
                self.vmWriter.writePop(self.sym_table.class_table[cur_var]["kind"], self.sym_table.class_table[cur_var]["idx"])
            #####################################
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
        #####################################
        if cur_var in self.sym_table.subroutine_table:
            self.vmWriter.writePop(self.sym_table.subroutine_table[cur_var]["kind"], self.sym_table.subroutine_table[cur_var]["idx"])
        else:
            self.vmWriter.writePop(self.sym_table.class_table[cur_var]["kind"], self.sym_table.class_table[cur_var]["idx"])
        #####################################
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
        ####################################
        self.vmWriter.writeIf("IF_TRUE" + str(self.if_counter))
        cur_idx = self.if_counter
        self.if_counter += 1
        self.vmWriter.writeGoto("IF_FALSE" + str(cur_idx))
        self.vmWriter.writeLabel("IF_TRUE"+str(cur_idx))
        ####################################
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
        #######################################
        self.vmWriter.writeGoto("IF_END" + str(cur_idx))
        self.vmWriter.writeLabel("IF_FALSE" + str(cur_idx))
        #######################################
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
            #############################################
            self.vmWriter.writeLabel("IF_END"+str(cur_idx))
            #############################################
            return True
        self.taber = self.taber[0:-2]
        self.my_file_string = self.my_file_string + self.taber + "</ifStatement>\n"
        #############################################
        self.vmWriter.writeLabel("IF_END" + str(cur_idx))
        #############################################
        return True

    def compileWhile(self):
        if self.tokens.getToken() == "while":
            self.my_file_string = self.my_file_string + self.taber + "<whileStatement>\n"
            self.taber = self.taber + "  "
            self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
            ######################################################################
            self.vmWriter.writeLabel("WHILE_LOOP" + str(self.while_counter))
            cur_idx = self.while_counter
            self.while_counter +=1
            #####################################################################
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
                #########################################
                self.vmWriter.writeArithmetic("not")
                self.vmWriter.writeIf("WHILE_END"+str(cur_idx))
                #########################################
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
            #############################################################
            self.vmWriter.writeGoto("WHILE_LOOP"+str(cur_idx))
            self.vmWriter.writeLabel("WHILE_END"+str(cur_idx))
            #############################################################
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
            ##########################################
            self.vmWriter.writePop("temp",0)
            #########################################
            return True
        else: return True

    def compileReturn(self):
        if self.tokens.getToken() == "return":
            self.my_file_string = self.my_file_string + self.taber + "<returnStatement>\n"
            self.taber = self.taber + "  "
            self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
            self.tokens.advance()
            if self.tokens.getToken() == ";":
                ############################################
                self.vmWriter.writePush("constant", 0)
                ###########################################
            if self.tokens.getToken() != ";" and not self.compileExpression():
                return False
            if self.tokens.getToken() == ";":
                self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                      self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                self.tokens.advance()
                ###################################
                self.vmWriter.writeReturn()
                ###################################
            else: return False
            self.taber = self.taber[0:-2]
            self.my_file_string = self.my_file_string + self.taber + "</returnStatement>\n"
            return True
        else: return True

    def compileExpression(self):
        op_array = []
        self.my_file_string = self.my_file_string + self.taber + "<expression>\n"
        self.taber = self.taber + "  "
        if self.tokens.getToken() == "~":
            op_array.append("~")
        if not self.compileTerm():
            return False
        while self.tokens.getToken() in OP:
            self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  OP[self.tokens.getToken()] + " </" + self.tokens.tokenType() + ">" + "\n"
            op_array.append(self.tokens.getToken())
            self.tokens.advance()
            if not self.compileTerm():
                return False
        ###################################
        for i in range(len(op_array)):
            if op_array[len(op_array) - i - 1] == "*":
                self.vmWriter.writeCall("Math.multiply", 2)
                continue
            self.vmWriter.writeArithmetic(op_array[len(op_array) - i - 1])
        ##################################
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
            ##################################################
            if self.tokens.getToken() == "false" or self.tokens.getToken() == "null":
                self.vmWriter.writePush("constant", 0)
            elif self.tokens.getToken() == "true":
                self.vmWriter.writePush("constant", 0)
                self.vmWriter.writeArithmetic("not")
            elif self.tokens.getToken() == "this":
                self.vmWriter.writePush("pointer", 0)
            else:self.vmWriter.writePush("constant",self.tokens.getToken()) # Need to modify for string
            #################################################
            self.tokens.advance()
        elif self.tokens.tokenType() == "identifier" and self.tokens.getToken() != self.subRoutineName and \
                self.tokens.peek() != ".":
            termIndicator = 1
            self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
            ###############################################
            if self.tokens.getToken() in self.sym_table.subroutine_table:
                segment = self.sym_table.subroutine_table[self.tokens.getToken()]["kind"]
                index = self.sym_table.subroutine_table[self.tokens.getToken()]["idx"]
                self.vmWriter.writePush(segment,index)
            else:
                segment = self.sym_table.class_table[self.tokens.getToken()]["kind"]
                index = self.sym_table.class_table[self.tokens.getToken()]["idx"]
                self.vmWriter.writePush(segment, index)
            ###############################################
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

    def compileExpressionList(self, nArgs):
        self.my_file_string = self.my_file_string + self.taber + "<expressionList>\n"
        self.taber = self.taber + "  "
        if self.tokens.getToken() == ")":
            self.taber = self.taber[0:-2]
            self.my_file_string = self.my_file_string + self.taber + "</expressionList>\n"
            return True
        if not self.compileExpression():
            return False
        nArgs[0] += 1
        while self.tokens.getToken() == ",":
            if self.tokens.getToken() == ",":
                nArgs[0] += 1
                self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                self.tokens.advance()
            if not self.compileExpression():
                return False
        self.taber = self.taber[0:-2]
        self.my_file_string = self.my_file_string + self.taber + "</expressionList>\n"
        return True


    def compileSubroutineCall(self):
        call_subroutine = str
        first_part = str
        inher_indicator = 0
        nArgs = [0]
        if self.tokens.getToken() == self.subRoutineName or self.tokens.tokenType() == "identifier" \
                and self.tokens.peek() != ".":
            self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                  self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
            call_subroutine = self.tokens.getToken()
            self.tokens.advance()
            if self.tokens.getToken() == "(":
                self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                      self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                self.tokens.advance()
                if not self.compileExpressionList(nArgs):
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
            call_subroutine = self.tokens.getToken()
            self.tokens.advance()
            if self.tokens.getToken() == ".":
                self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                      self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                ###############################
                if call_subroutine in self.sym_table.subroutine_table:
                    if self.sym_table.subroutine_table[call_subroutine]["type"] not in TYPE:
                        first_part = call_subroutine
                        call_subroutine = self.sym_table.subroutine_table[call_subroutine]["type"]\
                                          + self.tokens.getToken()
                        inher_indicator = 1
                    else: call_subroutine = call_subroutine + self.tokens.getToken()
                else:call_subroutine = call_subroutine + self.tokens.getToken()
                #################################
                self.tokens.advance()
            else: return False
            if self.tokens.getToken() == self.subRoutineName or self.tokens.tokenType() == "identifier":
                self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                      self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                call_subroutine = call_subroutine + self.tokens.getToken()
                self.tokens.advance()
            else: return False
            if self.tokens.getToken() == "(":
                self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                      self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                self.tokens.advance()
                if not self.compileExpressionList(nArgs):
                    return False
                if self.tokens.getToken() == ")":
                    self.my_file_string = self.my_file_string + self.taber + "<" + self.tokens.tokenType() + "> " + \
                                          self.tokens.getToken() + " </" + self.tokens.tokenType() + ">" + "\n"
                    self.tokens.advance()
                else: return False
            else: return False
            #########################################################
            if inher_indicator == 1:
                segment = self.sym_table.subroutine_table[first_part]["kind"]
                idx = self.sym_table.subroutine_table[first_part]["idx"]
                self.vmWriter.writePush(segment,idx)
                if call_subroutine[0] >= "A" and call_subroutine[0] <= "Z":
                    self.vmWriter.writeCall(call_subroutine, 1)
                else:self.vmWriter.writeCall(self.className+"."+call_subroutine, 1)
            else:
                if call_subroutine[0] >= "A" and call_subroutine[0] <= "Z":
                    self.vmWriter.writeCall(call_subroutine, nArgs[0])
                else:self.vmWriter.writeCall(self.className+"."+call_subroutine,nArgs[0])
            #############################################################
        else: return True

        return True