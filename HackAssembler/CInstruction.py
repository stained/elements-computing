class CInstruction:
    comptable = {"0": "0101010", "1": "0111111", "-1": "0111010", "D": "0001100", "A": "0110000", "!D": "0001101",
                 "!A": "0110001", "-D": "0001111", "-A": "0110011", "D+1": "0011111", "A+1": "0110111", "D-1": "0001110",
                 "A-1": "0110010", "D+A": "0000010", "D-A": "0010011", "A-D": "0000111", "D&A": "0000000",
                 "D|A": "0010101", "M": "1110000", "!M": "1110001", "-M": "1110011", "M+1": "1110111", "M-1": "1110010",
                 "D+M": "1000010", "D-M": "1010011", "M-D": "1000111", "D&M": "1000000", "D|M": "1010101"
                 }

    desttable = {"null": "000", "M": "001", "D": "010", "MD": "011", "A": "100", "AM": "101", "AD": "110", "AMD": "111"}

    jmptable = {"null": "000", "JGT": "001", "JEQ": "010", "JGE": "011", "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}

    def __init__(self, instruction, index):
        self.index = str(index)

        # check whether we have a dest
        destpos = instruction.find("=")

        # check whether there's a jump
        jumppos = instruction.find(";")

        # replace all delimiters so we can split it easily
        instruction = instruction.replace("=", ";")

        # split instruction
        # dest=comp;jmp
        instruction = instruction.split(";")

        self.dest = instruction[0] if destpos > -1 else "null"
        self.comp = instruction[1] if destpos > -1 else instruction[0]

        if jumppos > -1:
            if destpos > -1:
                self.jmp = instruction[2]
            else:
                self.jmp = instruction[1]
        else:
            self.jmp = "null"

    def __str__(self):
        return self.index + ":[C] Dest: " + self.dest + ", Comp: " + self.comp + ", Jump: " + self.jmp

    def to_binary(self):
        # FORMAT = 111 (C instruction) + COMP[a, c1, c2, c3, c4, c5, c6] + DESC[d1, d2, d3] + JMP[j1, j2, j3]
        return "111" + CInstruction.comptable[self.comp] + CInstruction.desttable[self.dest] + CInstruction.jmptable[self.jmp];
