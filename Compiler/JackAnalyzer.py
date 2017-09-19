import os
import sys
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

if __name__ == "__main__":
    jackFiles = []

    completePath = sys.argv[1]

    if os.path.isdir(completePath) and not completePath.endswith("/"):
        completePath = completePath + "/"

    filePath, fileName = os.path.split(completePath)
    outputFilename = None
    writeInit = False

    if os.path.isdir(completePath):
        writeInit = True
        folderName = os.path.basename(filePath)

        for root, dirs, files in os.walk(completePath):
            path = root.split(os.sep)
            for file in files:
                if file.endswith(".jack"):
                    jackFiles.append(filePath + "/" + file)

    else:
        filePath = filePath + "/" + fileName

        # file passed in
        jackFiles.append(filePath)

    if len(jackFiles) > 0:
        for filePath in jackFiles:
            # tokenize
            tokenizer = JackTokenizer(filePath)

            # compile
            outputFilename = filePath.replace(".jack", ".tok.xml")
            CompilationEngine(tokenizer, outputFilename)


