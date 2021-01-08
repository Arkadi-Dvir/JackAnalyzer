import os
import sys
class VMWriter:
    cur_file = str

    def __init__(self):
        self.cur_file = ""

    def writePush(self, segment, idx):
        if segment == "constant":
            self.cur_file = self.cur_file + "push constant " + str(idx) + "\n"
        elif segment == "argument":
            self.cur_file = self.cur_file + "push argument " + str(idx) + "\n"
        elif segment == "var":
            self.cur_file = self.cur_file + "push local " + str(idx) + "\n"
        elif segment == "static":
            self.cur_file = self.cur_file + "push static " + str(idx) + "\n"
        elif segment == "this":
            self.cur_file = self.cur_file + "push this " + str(idx) + "\n"
        elif segment == "that": #Might be problem with the index
            self.cur_file = self.cur_file + "push that " + str(idx) + "\n"
        elif segment == "pointer":
            self.cur_file = self.cur_file + "push pointer " + str(idx) + "\n"
        else: self.cur_file = self.cur_file + "push temp " + str(idx) + "\n"

    def writePop(self, segment, idx):
        if segment == "argument":
            self.cur_file = self.cur_file + "pop argument " + str(idx) + "\n"
        elif segment == "var":
            self.cur_file = self.cur_file + "pop local " + str(idx) + "\n"
        elif segment == "static":
            self.cur_file = self.cur_file + "pop static " + str(idx) + "\n"
        elif segment == "this":
            self.cur_file = self.cur_file + "pop this " + str(idx) + "\n"
        elif segment == "that": #Might be problem with the index
            self.cur_file = self.cur_file + "pop that " + str(idx) + "\n"
        elif segment == "pointer":
            self.cur_file = self.cur_file + "pop pointer " + str(idx) + "\n"
        else: self.cur_file = self.cur_file + "pop temp " + str(idx) + "\n"

    def writeArithmetic(self,cmd):
        if cmd == "+":
            self.cur_file = self.cur_file + "add" + "\n"
        elif cmd == "-":
            self.cur_file = self.cur_file + "sub" + "\n"
        elif cmd == "neg":
            self.cur_file = self.cur_file + "neg" + "\n"
        elif cmd == "=":
            self.cur_file = self.cur_file + "eq" + "\n"
        elif cmd == ">":
            self.cur_file = self.cur_file + "gt" + "\n"
        elif cmd == "<":
            self.cur_file = self.cur_file + "lt" + "\n"
        elif cmd == "&":
            self.cur_file = self.cur_file + "and" + "\n"
        elif cmd == "|":
            self.cur_file = self.cur_file + "or" + "\n"
        else: self.cur_file = self.cur_file + "not" + "\n"

    def writeLabel(self, label):
        self.cur_file = self.cur_file + "label " + label + "\n"

    def writeGoto(self, label):
        self.cur_file = self.cur_file + "goto " + label + "\n"

    def writeIf(self, label):
        self.cur_file = self.cur_file + "if-goto " + label + "\n"

    def writeCall(self, name, nArgs):
        self.cur_file = self.cur_file + "call " + name + " " + str(nArgs) + "\n"

    def writeFunction(self, name, nLocals):
        self.cur_file = self.cur_file + "function " + str(name) + " " + str(nLocals) + "\n"

    def writeReturn(self):
        self.cur_file = self.cur_file + "return" + "\n"

    def close(self):
        return 0
