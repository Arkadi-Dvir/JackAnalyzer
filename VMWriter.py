import os
import sys
class VMWriter:
    cur_file = str

    def __init__(self, file):
        self.cur_file = file

    def writePush(self, segment, idx):
        if segment == "constant":
            self.cur_file = self.cur_file + "push constant " + idx + "\n"
        elif segment == "argument":
            self.cur_file = self.cur_file + "push argument " + idx + "\n"
        elif segment == "local":
            self.cur_file = self.cur_file + "push local " + idx + "\n"
        elif segment == "static":
            self.cur_file = self.cur_file + "push static " + idx + "\n"
        elif segment == "this":
            self.cur_file = self.cur_file + "push this " + idx + "\n"
        elif segment == "that": #Might be problem with the index
            self.cur_file = self.cur_file + "push that " + idx + "\n"
        elif segment == "pointer":
            self.cur_file = self.cur_file + "push pointer " + idx + "\n"
        else: self.cur_file = self.cur_file + "push temp " + idx + "\n"

    def writePop(self, segment, idx):
        if segment == "argument":
            self.cur_file = self.cur_file + "pop argument " + idx + "\n"
        elif segment == "local":
            self.cur_file = self.cur_file + "pop local " + idx + "\n"
        elif segment == "static":
            self.cur_file = self.cur_file + "pop static " + idx + "\n"
        elif segment == "this":
            self.cur_file = self.cur_file + "pop this " + idx + "\n"
        elif segment == "that": #Might be problem with the index
            self.cur_file = self.cur_file + "pop that " + idx + "\n"
        elif segment == "pointer":
            self.cur_file = self.cur_file + "pop pointer " + idx + "\n"
        else: self.cur_file = self.cur_file + "pop temp " + idx + "\n"

    def writeArithmetic(self,cmd):
        if cmd == "add":
            self.cur_file = self.cur_file + "add" + "\n"
        elif cmd == "sub":
            self.cur_file = self.cur_file + "sub" + "\n"
        elif cmd == "neg":
            self.cur_file = self.cur_file + "neg" + "\n"
        elif cmd == "eq":
            self.cur_file = self.cur_file + "eq" + "\n"
        elif cmd == "gt":
            self.cur_file = self.cur_file + "gt" + "\n"
        elif cmd == "lt":
            self.cur_file = self.cur_file + "lt" + "\n"
        elif cmd == "and":
            self.cur_file = self.cur_file + "and" + "\n"
        elif cmd == "or":
            self.cur_file = self.cur_file + "or" + "\n"
        else: self.cur_file = self.cur_file + "not" + "\n"

    def writeLabel(self, label):
        self.cur_file = self.cur_file + "label " + label + "\n"

    def writeGoto(self, label):
        self.cur_file = self.cur_file + "goto " + label + "\n"

    def writeIf(self, label):
        self.cur_file = self.cur_file + "if-goto " + label + "\n"

    def writeCall(self, name, nArgs):
        self.cur_file = self.cur_file + "call " + name + " " + nArgs + "\n"

    def writeFunction(self, name, nLocals):
        self.cur_file = self.cur_file + "function " + name + " " + nLocals + "\n"

    def writeReturn(self):
        self.cur_file = self.cur_file + "return" + "\n"

    def close(self):
        return 0
