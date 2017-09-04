from MemoryAccess import MemoryAccess

class FlowControl:

    def __init__(self):
        return

    @staticmethod
    def getLabelName(parser, label):
        return parser.vmName + \
               (parser.currentFunction if parser.currentFunction is not None else "") + \
               "$" + label

    @staticmethod
    def _label(parser, label):
        code = "(" + FlowControl.getLabelName(parser, label) + ")\n"
        return code

    @staticmethod
    def _if_goto(parser, label):

        # pop into D
        code = MemoryAccess._pop(parser, "", "0")

        code += "\t@" + FlowControl.getLabelName(parser, label) + "\n" \
                "\tD;JNE\n"

        return code

    @staticmethod
    def _goto(parser, label):
        code = "\t@" + FlowControl.getLabelName(parser, label) + "\n" \
               "\t0;JMP\n"

        return code
