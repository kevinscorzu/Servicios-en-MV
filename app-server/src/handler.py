import sys
import json
import histogram

dirC = None
dirH = None
dirL = None
jsonData = None

def readJson():
    global jsonData

    with open("images.json") as f:
        jsonData = json.load(f)
        f.close()
    print(jsonData["client"])
    if not (jsonData["images"]):
        print("Error, there are no images to handle")
        sys.exit()

    return

def setFilePaths(readData):
    global dirC
    global dirH
    global dirL

    dirC = readData[0][12:]
    dirH = readData[1][10:]
    dirL = readData[2][8:]
    
    return

def readConfigFile():
    readData = []
    linesToRead = [1, 2, 3]

    with open("config.conf") as f:
        for position, line in enumerate(f):
            if position in linesToRead:
                readData.append(str.rstrip(line))
        f.close()

    return setFilePaths(readData)

def main():
    readJson()
    readConfigFile()

    if str(sys.argv[1]) == "0":
        histogram.applyHistogram(jsonData["images"], dirH)
        return
    else:
        print("ES 1")
        return

if __name__ == "__main__":
    main()
    sys.exit()