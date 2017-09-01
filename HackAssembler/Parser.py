from AInstruction import AInstruction
from CInstruction import CInstruction
from Label import Label

# preset symbol table
symboltable = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4, "SCREEN": 16384, "KBD": 24576}

for i in range(0, 16):
    symboltable["R" + str(i)] = i


def print_parsed(parsedlines):
    for index, line in enumerate(parsedlines):
        print(line)


def print_symbol_table():
    for key, value in symboltable.items():
        print(key, value)


# remove any comments and additional white space
def clean_instruction(instruction):
    # check for comments
    position = instruction.find("//")

    if position > -1:
        instruction = instruction[:position]

    return instruction.strip()


# parse an A instruction
def parse_a_instruction(instruction, index):
    instruction = clean_instruction(instruction)
    return AInstruction(instruction, index)


# parse a C instruction
def parse_c_instruction(instruction, index):
    instruction = clean_instruction(instruction)
    return CInstruction(instruction, index)


def parse_label(label):
    label = clean_instruction(label)
    return Label(label)


def parse(sourcelines):
    parsedlines = []

    # base memory index for variables
    memoryindex = 16

    # parse lines into instructions / labels
    index = 0
    for line in sourcelines:
        if line.startswith("@"):
            parsedlines.append(parse_a_instruction(line, index))
            index = index + 1
        elif line.startswith("("):
            parsedlines.append(parse_label(line))
        else:
            parsedlines.append(parse_c_instruction(line, index))
            index = index + 1

    # map all label symbols
    for index, line in enumerate(parsedlines):
        if type(line) is Label and not line.label in symboltable:
            notlabel = False
            subindex = 1
            while not notlabel:
                # find next instruction that isn't a label
                nextinstruction = parsedlines[index + subindex]

                if nextinstruction and not type(nextinstruction) is Label:
                    symboltable[line.label] = str(nextinstruction.index)
                    notlabel = True
                else:
                    subindex = subindex + 1

    # remove all labels from array
    parsedlines = [line for line in parsedlines if type(line) is not Label]

    # second pass, replace all label values + variables with symbol value
    for line in parsedlines:
        if type(line) is AInstruction and not line.value.isdigit():
            if line.value in symboltable:
                line.value = str(symboltable[line.value])
            else:
                # set to current memory index
                symboltable[line.value] = memoryindex
                line.value = str(memoryindex)

                # increment memory index
                memoryindex = memoryindex + 1


    #print_parsed(parsedlines)
    #print_symbol_table()
    return parsedlines
