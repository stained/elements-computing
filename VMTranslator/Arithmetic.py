from MemoryAccess import MemoryAccess

class Arithmetic:

    def __init__(self):
        return

    @staticmethod
    def vm_add(parser):
        code = "\t// add\n"

        # decrement stack pointer
        code += MemoryAccess.decrement_stack_pointer()

        # get value from stack into D
        code += "\tA=M\n" + \
                "\tD=M\n"

        # decrement stack pointer
        code += MemoryAccess.decrement_stack_pointer()

        # add both values and push in-place
        code += "\tA=M\n" + \
                "\tM=D+M\n"

        code += MemoryAccess.increment_stack_pointer()

        return code

    @staticmethod
    def vm_sub(parser):
        code = "\t// sub\n"

        # decrement stack pointer
        code += MemoryAccess.decrement_stack_pointer()

        # get value from stack into D
        code += "\tA=M\n" + \
                "\tD=M\n"

        # decrement stack pointer
        code += MemoryAccess.decrement_stack_pointer()

        # subtract values and push in-place
        code += "\tA=M\n" + \
                "\tM=M-D\n"

        code += MemoryAccess.increment_stack_pointer()

        return code

    @staticmethod
    def vm_neg(parser):
        code = "\t// neg\n"

        # decrement stack pointer
        code += MemoryAccess.decrement_stack_pointer()

        # negate value and push in-place
        code += "\tA=M\n" + \
                "\tM=-M\n"

        code += MemoryAccess.increment_stack_pointer()

        return code

    @staticmethod
    def vm_eq(parser):
        code = "\t// eq\n"

        # decrement stack pointer
        code += MemoryAccess.decrement_stack_pointer()

        # get value from stack into D
        code += "\tA=M\n" + \
                "\tD=M\n"

        # decrement stack pointer
        code += MemoryAccess.decrement_stack_pointer()

        # compare values
        code += "\tA=M\n" + \
                "\tD=D-M\n"

        jmpLabel = "JMP." + str(parser.lineNumber)
        jneLabel = "JNE." + str(parser.lineNumber)

        # jump to JNE if not equal
        code += "\t@" + jneLabel + "\n" + \
                "\tD;JNE\n"

        # else set to true
        code += "\t@SP\n" + \
                "\tA=M\n" + \
                "\tM=-1\n"

        #  and jump to end of comparison
        code += "\t@" + jmpLabel + "\n" + \
                "\t0;JMP\n"

        # set to false and just continue till end
        code += "(" + jneLabel + ")\n"

        code += "\t@SP\n" + \
                "\tA=M\n" + \
                "\tM=0\n"

        # end of comparison
        code += "(" + jmpLabel + ")\n"

        # increment stack pointer again
        code += MemoryAccess.increment_stack_pointer()

        return code

    @staticmethod
    def vm_lt(parser):
        code = "\t// lt\n"

        # decrement stack pointer
        code += MemoryAccess.decrement_stack_pointer()

        # get value from stack into D
        code += "\tA=M\n" + \
                "\tD=M\n"

        # decrement stack pointer
        code += MemoryAccess.decrement_stack_pointer()

        # compare values
        code += "\tA=M\n" + \
                "\tD=M-D\n"

        jmpLabel = "JMP." + str(parser.lineNumber)
        jltLabel = "JLT." + str(parser.lineNumber)

        # jump to JLT if D-M > 0
        code += "\t@" + jltLabel + "\n" + \
                "\tD;JLT\n"

        # else set to false
        code += "\t@SP\n" + \
                "\tA=M\n" + \
                "\tM=0\n"

        #  and jump to end of comparison
        code += "\t@" + jmpLabel + "\n" + \
                "\t0;JMP\n"

        # set to true and just continue till end
        code += "(" + jltLabel + ")\n"

        code += "\t@SP\n" + \
                "\tA=M\n" + \
                "\tM=-1\n"

        # end of comparison
        code += "(" + jmpLabel + ")\n"

        # increment stack pointer again
        code += MemoryAccess.increment_stack_pointer()

        return code

    @staticmethod
    def vm_gt(parser):
        code = "\t// gt\n"

        # decrement stack pointer
        code += MemoryAccess.decrement_stack_pointer()

        # get value from stack into D
        code += "\tA=M\n" + \
                "\tD=M\n"

        # decrement stack pointer
        code += MemoryAccess.decrement_stack_pointer()

        # compare values
        code += "\tA=M\n" + \
                "\tD=M-D\n"

        jmpLabel = "JMP." + str(parser.lineNumber)
        jgtLabel = "JGT." + str(parser.lineNumber)

        # jump to JLT if D-M > 0
        code += "\t@" + jgtLabel + "\n" + \
                "\tD;JGT\n"

        # else set to false
        code += "\t@SP\n" + \
                "\tA=M\n" + \
                "\tM=0\n"

        #  and jump to end of comparison
        code += "\t@" + jmpLabel + "\n" + \
                "\t0;JMP\n"

        # set to true and just continue till end
        code += "(" + jgtLabel + ")\n"

        code += "\t@SP\n" + \
                "\tA=M\n" + \
                "\tM=-1\n"

        # end of comparison
        code += "(" + jmpLabel + ")\n"

        # increment stack pointer again
        code += MemoryAccess.increment_stack_pointer()

        return code

    @staticmethod
    def vm_not(parser):
        code = "\t// not\n"

        # decrement stack pointer
        code += MemoryAccess.decrement_stack_pointer()

        # not value and push in-place
        code += "\tA=M\n" + \
                "\tM=!M\n"

        code += MemoryAccess.increment_stack_pointer()

        return code

    @staticmethod
    def vm_and(parser):
        code = "\t// and\n"

        # decrement stack pointer
        code += MemoryAccess.decrement_stack_pointer()

        # get value from stack into D
        code += "\tA=M\n" + \
                "\tD=M\n"

        # decrement stack pointer
        code += MemoryAccess.decrement_stack_pointer()

        # and values and push in-place
        code += "\tA=M\n" + \
                "\tM=M&D\n"

        code += MemoryAccess.increment_stack_pointer()

        return code

    @staticmethod
    def vm_or(parser):
        code = "\t// or\n"

        # decrement stack pointer
        code += MemoryAccess.decrement_stack_pointer()

        # get value from stack into D
        code += "\tA=M\n" + \
                "\tD=M\n"

        # decrement stack pointer
        code += MemoryAccess.decrement_stack_pointer()

        # or values and push in-place
        code += "\tA=M\n" + \
                "\tM=M|D\n"

        code += MemoryAccess.increment_stack_pointer()

        return code