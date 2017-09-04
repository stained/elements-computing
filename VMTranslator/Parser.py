import os
from MemoryAccess import MemoryAccess
from Arithmetic import Arithmetic
from FlowControl import FlowControl


# remove any comments and additional white space
def clean_command(command):
    # check for comments
    position = command.find("//")

    if position > -1:
        command = command[:position]

    return command.strip()


class Parser:

    # map commands to code class
    commandMap = {"push": MemoryAccess, "pop": MemoryAccess,                            # memory
                  "add": Arithmetic, "sub": Arithmetic, "neg": Arithmetic,              # arithmetic
                  "eq": Arithmetic, "gt": Arithmetic, "lt": Arithmetic,
                  "and": Arithmetic, "or": Arithmetic, "not": Arithmetic,
                  "label": FlowControl, "if_goto": FlowControl, "goto": FlowControl     # flow control
                  }

    def __init__(self, vmFilePath):
        self.vmFilePath = vmFilePath
        self.filePath, self.fileName = os.path.split(vmFilePath)
        self.vmName, self.fileExtension = os.path.splitext(self.fileName)
        self.lineNumber = 0
        self.currentFunction = None

    def parse(self):
        self.lineNumber = 0

        outputFilename = self.vmFilePath.replace(".vm", ".asm")
        outFile = open(outputFilename, 'w')

        # open file and traverse commands
        with open(self.vmFilePath) as vmFile:
            for line in vmFile:
                # strip whitespace and check for comment
                line = line.strip()
                if line and not line.startswith("//"):
                    # remove comments
                    line = clean_command(line)

                    # real command, so split into components
                    commandLine = line.split(" ")

                    # call relevant command function in appropriate class
                    command = commandLine.pop(0)
                    command = command.replace("-", "_")
                    commandClass = Parser.commandMap[command]

                    if commandClass is not None:
                        # replace dash with underscore for function names
                        asmOutput = None

                        try:
                            # prepend _ because "not" (for example) is a reserved word
                            asmOutput = getattr(commandClass(), "_" + command)(self, *commandLine)
                        except AttributeError:
                            print("command " + command + " not implemented")
                            continue

                        print(asmOutput)
                        outFile.write(asmOutput)
                        self.lineNumber = self.lineNumber + 1

        outFile.close()



