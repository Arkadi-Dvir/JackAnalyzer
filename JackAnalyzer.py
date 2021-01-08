import sys
import os
import JackTokenizer
import CompilationEngine
import VMWriter

if __name__ == '__main__':
    if len(sys.argv) == 2:
        file_path = os.path.normpath(sys.argv[1])
        if os.path.isdir(file_path):  # Directory
            fileName = os.path.basename(file_path)
            files = os.listdir(file_path)
            files = [file for file in files if file.endswith(".jack")]
            for file in files:
                fi = os.path.normpath(file_path + '/' + file)
                token = JackTokenizer.JackTokenizer(fi)
                vm_writer = VMWriter.VMWriter()
                compile = CompilationEngine.CompilationEngine(token, vm_writer)
                text_file = str(vm_writer.cur_file)
                fileName = (file_path + '/' + file).split(".")[0]
                fileName = fileName + ".vm"
                token_file = open(fileName, "w+")
                token_file.write(text_file)
                token_file.close()
        else:  # file path
            token = JackTokenizer.JackTokenizer(file_path)
            vm_writer = VMWriter.VMWriter()
            compile = CompilationEngine.CompilationEngine(token, vm_writer)
            compile.compileClass()
            text_file = str(vm_writer.cur_file)
            fileName = sys.argv[1].split(".")[0]
            fileName = fileName + ".vm"
            token_file = open(fileName, "w+")
            token_file.write(text_file)
            token_file.close()
