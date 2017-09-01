import os
import sys
from Parser import Parser

if __name__ == "__main__":
    vmFiles = []

    filePath, fileName = os.path.split(sys.argv[1])

    if fileName is "":
        # folder passed in
        for root, dirs, files in os.walk(filePath):
            path = root.split(os.sep)
            for file in files:
                if file.endswith(".vm"):
                    vmFiles.append(filePath + "/" + file)

    else:
        # file passed in
        vmFiles.append(filePath + "/" + fileName)

    if len(vmFiles) > 0:
        for filePath in vmFiles:
            parser = Parser(filePath)
            parser.parse()


