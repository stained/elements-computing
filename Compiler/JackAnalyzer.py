import os
import sys
from JackTokenizer import JackTokenizer


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

        # folder passed in
        outputFilename = filePath + "/" + folderName + ".xml"

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
            outputFilename = filePath.replace(".jack", ".xml")
            outFile = open(outputFilename, 'w')

            tokenizer = JackTokenizer(filePath)
            outFile.write('<tokens>\n')

            while tokenizer.has_more_tokens():
                token = tokenizer.advance()
                outFile.write('<' + token.type + '>' + token.value + '</' + token.type + '>\n')

            outFile.write('</tokens>\n')
            outFile.close()


