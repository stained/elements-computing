import os
import sys
from Parser import Parser
from FlowControl import FlowControl


if __name__ == "__main__":
    vmFiles = []

    completePath = sys.argv[1]

    if os.path.isdir(completePath) and not completePath.endswith("/"):
        completePath = completePath + "/"

    filePath, fileName = os.path.split(completePath)
    outputFilename = None
    writeInit = False

    if os.path.isdir(completePath):
        writeInit = True
        folderName = os.path.basename(filePath)

        # folder passed in
        outputFilename = filePath + "/" + folderName + ".asm"

        for root, dirs, files in os.walk(completePath):
            path = root.split(os.sep)
            for file in files:
                if file.endswith(".vm"):
                    vmFiles.append(filePath + "/" + file)

    else:
        filePath = filePath + "/" + fileName
        outputFilename = filePath.replace(".vm", ".asm")

        # file passed in
        vmFiles.append(filePath)

    if len(vmFiles) > 0:
        outFile = open(outputFilename, 'w')

        for filePath in vmFiles:
            parser = Parser(filePath, outFile)
            parser.parse(writeInit)
            writeInit = not writeInit

        outFile.close()


