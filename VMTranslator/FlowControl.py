from MemoryAccess import MemoryAccess

class FlowControl:

    def __init__(self):
        return

    @staticmethod
    def getLabelName(parser, label):
        if parser.currentFunction is None:
            return parser.vmName + "$" + label
        else:
            return parser.currentFunction + "$" + label

    @staticmethod
    def _call(parser, _function, argCount):
        # call comment
        code = "\t// call " + _function + " " + argCount + "\n"

        # put return address onto stack
        returnLabel = _function + "$ret"
        code += MemoryAccess._push(parser, "constant", returnLabel)

        # PUSH LCL
        code += MemoryAccess._push(parser, "memory", "LCL")

        # PUSH ARG
        code += MemoryAccess._push(parser, "memory", "ARG")

        # PUSH THIS
        code += MemoryAccess._push(parser, "memory", "THIS")

        # PUSH THAT
        code += MemoryAccess._push(parser, "memory", "THAT")

        # ARG = SP - n - 5
        code += "\t@SP\n" + \
                "\tD=M\n" + \
                "\t@" + str(int(argCount) + 5) + "\n" + \
                "\tD=D-A\n" + \
                "\t@ARG\n" + \
                "\tM=D\n"

        # LCL = SP
        code += "\t@SP\n" + \
                "\tD=M\n" + \
                "\t@LCL\n" + \
                "\tM=D\n"

        # GOTO f
        code += "\t@" + _function + "\n" + \
                "\t0;JMP\n"

        # return label
        code += "(" + returnLabel + ")\n"

        return code

    @staticmethod
    def _function(parser, _function, localCount):
        # function comment
        code = "// " + _function + " " + localCount + "\n"

        # set current function
        parser.currentFunction = _function

        # declare function label
        code += "(" + _function + ")\n"

        # push 0 for each local variable
        code += "\t// push empty local variables (" + localCount + ")\n"
        for i in range(0, int(localCount)):
            code += MemoryAccess._push(parser, "constant", "0")

        return code

    @staticmethod
    def _return(parser):
        # return comment
        code = "\t// return\n"

        # FRAME = LCL
        # load LCL into FRAME
        code += "\t@LCL\n" + \
                "\tD=M\n" +\
                "\t@FRAME\n" + \
                "\tM=D\n"

        # RET = *(FRAME-5)
        # put RET into RET
        code += "\t@FRAME\n" + \
                "\tD=M\n" + \
                "\t@5\n" + \
                "\tA=D-A\n" + \
                "\tD=M\n" + \
                "\t@RET\n" + \
                "\tM=D\n"

        # *ARG = POP()
        code += MemoryAccess._pop(parser, "argument", "0")

        # SP = ARG + 1
        code += "\t@ARG\n" + \
                "\tD=M\n" + \
                "\t@SP\n" + \
                "\tM=D+1\n"

        # THAT = *(FRAME - 1)
        code += "\t@FRAME\n" + \
                "\tD=M\n" + \
                "\t@1\n" + \
                "\tA=D-A\n" + \
                "\tD=M\n" + \
                "\t@THAT\n" + \
                "\tM=D\n"

        # THIS = *(FRAME - 2)
        code += "\t@FRAME\n" + \
                "\tD=M\n" + \
                "\t@2\n" + \
                "\tA=D-A\n" + \
                "\tD=M\n" + \
                "\t@THIS\n" + \
                "\tM=D\n"

        # ARG = *(FRAME - 3)
        code += "\t@FRAME\n" + \
                "\tD=M\n" + \
                "\t@3\n" + \
                "\tA=D-A\n" + \
                "\tD=M\n" + \
                "\t@ARG\n" + \
                "\tM=D\n"

        # LCL = *(FRAME - 4)
        code += "\t@FRAME\n" + \
                "\tD=M\n" + \
                "\t@4\n" + \
                "\tA=D-A\n" + \
                "\tD=M\n" + \
                "\t@LCL\n" + \
                "\tM=D\n"

        # GOTO RET
        code += "\t@RET\n" + \
                "\tA=M\n" + \
                "\tD=A\n" + \
                "\t0;JMP\n"

        return code

    @staticmethod
    def _label(parser, label):
        # label comment
        code = "// label " + label + "\n"

        code += "(" + FlowControl.getLabelName(parser, label) + ")\n"
        return code

    @staticmethod
    def _if_goto(parser, label):
        # if-goto comment
        code = "\t// if-goto " + label + "\n"

        # pop into D
        code += MemoryAccess._pop(parser, "", "0")

        code += "\t@" + FlowControl.getLabelName(parser, label) + "\n" \
                "\tD;JNE\n"

        return code

    @staticmethod
    def _goto(parser, label):
        # goto comment
        code = "\t// goto " + label + "\n"

        code += "\t@" + FlowControl.getLabelName(parser, label) + "\n" \
                "\t0;JMP\n"

        return code
