class MemoryAccess:

    segmentRegisterMap = {"stack": "SP", "local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}

    def __init__(self):
        return

    @staticmethod
    def increment_stack_pointer():
        # increment stack pointer
        code = "\t@" + MemoryAccess.segmentRegisterMap["stack"] + "\n" + \
               "\tM=M+1\n"

        return code

    @staticmethod
    def push_to_stack_and_increment():
        # push to stack
        code = "\t@" + MemoryAccess.segmentRegisterMap["stack"] + "\n" + \
               "\tA=M\n" + \
               "\tM=D\n"

        code += MemoryAccess.increment_stack_pointer()

        return code

    @staticmethod
    def decrement_stack_pointer():
        # decrement stack pointer
        code = "\t@" + MemoryAccess.segmentRegisterMap["stack"] + "\n" + \
               "\tM=M-1\n"

        return code

    @staticmethod
    def vm_push(parser, segment, index):
        # add comment for command
        code = "\t// push " + segment + " " + index + "\n"

        if segment in MemoryAccess.segmentRegisterMap:
            # load index into D
            code += "\t@" + index + "\n" + \
                    "\tD=A\n"

            # get value at segment [memory location + index] into D register
            code += "\t@" + MemoryAccess.segmentRegisterMap[segment] + "\n" + \
                    "\tA=D+M\n" + \
                    "\tD=M\n"

            code += MemoryAccess.push_to_stack_and_increment()

        elif segment == "temp":
            # load from index 5
            code += "\t@" + str(int(index) + 5) + "\n" + \
                    "\tD=M\n"

            code += MemoryAccess.push_to_stack_and_increment()
        elif segment == "pointer":
            # load from index 3 [this/that]
            code += "\t@" + str(int(index) + 3) + "\n" + \
                    "\tD=M\n"

            code += MemoryAccess.push_to_stack_and_increment()
        elif segment == "static":
            code += "\t@" + parser.vmName + "." + index + "\n" + \
                    "\tD=M\n"

            code += MemoryAccess.push_to_stack_and_increment()
        elif segment == "memory":
            # load mem value at index
            code += "\t@" + index + "\n" + \
                    "\tD=M\n"

            code += MemoryAccess.push_to_stack_and_increment()
        else:
            # load index into D -- constant
            code += "\t@" + index + "\n" + \
                    "\tD=A\n"

            code += MemoryAccess.push_to_stack_and_increment()

        return code

    @staticmethod
    def vm_pop(parser, segment, index):
        code = "\t// pop " + segment + " " + index + "\n"

        if segment in MemoryAccess.segmentRegisterMap:
            # load memory segment + index and set value to D
            code += "\t@" + index + "\n" + \
                    "\tD=A\n"

            # A contains pointer to memory location segment + i
            code += "\t@" + MemoryAccess.segmentRegisterMap[segment] + "\n" + \
                    "\tD=D+M\n" + \
                    "\t@TMP\n" + \
                    "\tM=D\n"

            # decrement stack pointer
            code += MemoryAccess.decrement_stack_pointer()

            # get value into D from stack
            code += "\tA=M\n" + \
                    "\tD=M\n"

            # load pointer from TMP and set to value D
            code += "\t@TMP\n" + \
                    "\tA=M\n" + \
                    "\tM=D\n"

        elif segment == "temp":
            # decrement stack pointer
            code += MemoryAccess.decrement_stack_pointer()

            # get value into D from stack
            code += "\tA=M\n" + \
                    "\tD=M\n"

            # load from index 5
            code += "\t@" + str(int(index) + 5) + "\n" + \
                    "\tM=D\n"
        elif segment == "pointer":
            # decrement stack pointer
            code += MemoryAccess.decrement_stack_pointer()

            # get value into D from stack
            code += "\tA=M\n" + \
                    "\tD=M\n"

            # load from index 3
            code += "\t@" + str(int(index) + 3) + "\n" + \
                    "\tM=D\n"
        elif segment == "static":
           # decrement stack pointer
            code += MemoryAccess.decrement_stack_pointer()

            # get value into D from stack
            code += "\tA=M\n" + \
                    "\tD=M\n"

            code += "\t@" + parser.vmName + "." + index + "\n" + \
                    "\tM=D\n"
        else:
            # decrement stack pointer
            code += MemoryAccess.decrement_stack_pointer()

            # get value into D from stack
            code += "\tA=M\n" + \
                    "\tD=M\n"

        return code
