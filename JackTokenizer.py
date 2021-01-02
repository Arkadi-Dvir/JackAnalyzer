import re

KEYWORDS = {"class":"class",  "constructor" : "constructor", "function" : "function",
            "method" : "method", "field" : "field", "static" : "static", "var" : "var", "int" : "int",
            "char" : "char", "boolean" : "boolean", "void" : "void", "true" : "true", "false" : "false",
            "null" : "null", "this" : "this", "let" : "let", "do" : "do", "if" : "if", "else" : "else",
           "while" : "while", "return" : "return"}
SYMBOLS = {"{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">",
           "=", "~"}

class JackTokenizer:
    my_file_line = str 
    cur_token = str
    text_arr = []
    token_counter = 0
    def __init__(self, file_path):
        my_file = open(file_path, "r")
        self.my_file_line = my_file.read() #Put all the code to one line file
        self.clearComments()
        self.tokenezation()
        self.cur_token = self.text_arr[0]


    def clearComments(self): # Removes all the comments
        string = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "", self.my_file_line)
        string = re.sub(re.compile("//.*?\n"), "", string)
        string = string.strip("\n")
        self.text_arr = string.split("\n")
        for i in range(len(self.text_arr)):
            self.text_arr[i] = self.text_arr[i].strip(" ")
            self.text_arr[i] = self.text_arr[i].strip("\t")
            self.text_arr[i] = re.sub(r"^\s+", "", self.text_arr[i])
        tmp_arr = []
        for i in self.text_arr:
            if re.match(r'^\s*$', i):
                continue
            else:
                tmp_arr.append(i)
        self.text_arr = tmp_arr

    def tokenezation(self): # Creating the tokens and put to our array
        tmp_arr = []
        str_indicator = 0
        for i in self.text_arr:
            in_line = 0
            cur_line = []
            while in_line < len(i):
                k = i[in_line]
                if re.match("[\W]", i[in_line]) and str_indicator == 0:
                    if len(cur_line) > 0:
                        tmp_arr.append(''.join(cur_line))
                        cur_line.clear()
                        if i[in_line] != ' ' and i[in_line] != '"':
                            tmp_arr.append(i[in_line])
                    elif i[in_line] != ' ' and i[in_line] != '"':
                        tmp_arr.append(i[in_line])
                    elif i[in_line] == '"':
                        str_indicator = not(str_indicator)
                        cur_line.append(i[in_line])
                    in_line += 1
                else:
                    if i[in_line] == '"' and str_indicator == 1:
                        cur_line.append(i[in_line])
                        tmp_arr.append(''.join(cur_line))
                        cur_line.clear()
                        in_line +=1
                        str_indicator = not(str_indicator)
                        continue
                    cur_line.append(i[in_line])
                    in_line += 1
        self.text_arr = tmp_arr


    def hasMoreTokens(self):
        if self.token_counter < len(self.text_arr) - 1:
            return True
        else: return False

    def advance(self):
        if self.hasMoreTokens():
            self.token_counter += 1
            self.cur_token = self.text_arr[self.token_counter]

    def tokenType(self):
        if self.cur_token in KEYWORDS:
            return "keyword"
        elif self.cur_token in SYMBOLS:
            return "symbol"
        elif self.text_arr[self.token_counter][0] == '"':
            return "stringConstant"
        elif self.text_arr[self.token_counter][0] >= "0" and self.text_arr[self.token_counter][0] <= "9":
            return "integerConstant"
        else: return "identifier"

    def keyWord(self):
            return KEYWORDS[self.cur_token]

    def symbol(self):
            return self.cur_token

    def identifier(self):
            return self.cur_token

    def intVal(self):
            return (self.cur_token)

    def stringVal(self):
            return self.cur_token[1:-1]

    def getToken(self):
        if self.tokenType() == "keyword":
            return self.keyWord()
        elif self.tokenType() == "symbol":
            return self.symbol()
        elif self.tokenType() == "stringConstant":
            return self.stringVal()
        elif self.tokenType() == "integerConstant":
            return self.intVal()
        else: return self.identifier()

    def peek(self): # Returns the next token if exists
        if self.hasMoreTokens():
            return self.text_arr[self.token_counter + 1]





