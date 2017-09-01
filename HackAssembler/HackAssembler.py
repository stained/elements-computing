import sys
import Parser


def open_file(filename):
    sourcelines = []

    with open(filename) as sourcefile:
        for line in sourcefile:
            line = line.strip()
            if line and not line.startswith("//"):
                sourcelines.append(line)

    return sourcelines


if __name__ == "__main__":
    # open file and get source code lines without whitespace + line comments
    sourcelines = open_file(sys.argv[1])

    # parse into instructions
    parsed = Parser.parse(sourcelines)

    # create output file, replacing .asm with .hack
    outputfilename = sys.argv[1][:-3] + "hack"

    # we have a parsed object, so now run through each instruction,
    # convert to machine code binary, and write to file
    f = open(outputfilename, 'w')

    for line in parsed:
#        print(line.to_binary())
        f.write(line.to_binary() + "\n")

    f.close()
