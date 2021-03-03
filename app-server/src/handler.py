import sys
import json
import histogram
from datetime import datetime
import os

dirC = None
dirH = None
dirL = None
images = None
histNum = None
rHistNum = None
classNum = None
rClassNum = None
client = None
genError = None
op = None

def createStringAux2(message, status):
    message += "Status: " + status + ", "
    message += "Datetime: " + str(datetime.now()) + "\n"

    return message

def createStringAux(message):
        if genError is not None:
            return createStringAux2(message, genError)
        else:
            return createStringAux2(message, "Completed Successfuly")

def createString():
    global rHistNum
    global rClassNum

    message = ""
    files = "Null, "
    filesAux = ""

    if client is not None:
        message += "Client: " + client + ", "
    if str(op) == "0":
        if images is not None:
            for x in images:
                filesAux += "histogram" + str(rHistNum) + ".png, "
                rHistNum += 1
            files = filesAux

        message += "Files: " + files
        return createStringAux(message)
    else:
        if images is not None:
            for x in images:
                filesAux += "class" + str(rClassNum) + ".png, "
                rClassNum += 1
            files = filesAux

        message += "Files: " + files
        return createStringAux(message)

def writeLog():
    message = createString()

    try:
        with open("." + dirL + "/log.txt", "a") as f:
            f.write(message)
            f.close()
        return
    except:
        with open("." + dirL + "/log.txt", "w") as f:
            f.write(message)
            f.close()
        return

def readImages():
    global images
    global client
    global genError

    try:
        with open("images.json") as f:
            jsonData = json.load(f)
            f.close()

        if not (jsonData["images"]):
            genError = "Error, there are no images to handle"
            print(genError)
            writeLog()
            sys.exit()

        client = jsonData["client"]
        images = jsonData["images"]
        return
    except:
        genError = "Error, couldn't open images.json"
        print(genError)
        writeLog()
        sys.exit()

def setFilePaths(readData):
    global dirC
    global dirH
    global dirL
    global genError

    try:
        dirC = readData[0][12:]
        dirH = readData[1][10:]
        dirL = readData[2][8:]
        return
    except:
        genError = "Error, there was a problem while reading the directories"
        print(genError)
        sys.exit()

def readConfigFile():
    global genError

    readData = []
    linesToRead = [1, 2, 3]

    try:
        with open("config.conf") as f:
            for position, line in enumerate(f):
                if position in linesToRead:
                    readData.append(str.rstrip(line))
            f.close()

        return setFilePaths(readData)
    except:
        genError = "Error, couldn't open config.conf"
        print(genError)
        sys.exit()

def readData():
    global histNum
    global classNum
    global rHistNum
    global rClassNum

    try:
        with open("data.json") as f:
            jsonData = json.load(f)
            f.close()
        histNum = jsonData["histNum"]
        classNum = jsonData["classNum"]
        rHistNum = histNum
        rClassNum = classNum
        return
    except:
        histNum = 0
        classNum = 0
        data = {}
        data["histNum"] = histNum
        data["classNum"] = classNum
        with open("data.json", "w") as f:
            json.dump(data, f)
            f.close()
        return

def updateDataAux():
    data = {}
    data["histNum"] = histNum
    data["classNum"] = classNum
    with open("data.json", "w") as f:
        json.dump(data, f)
        f.close()
    return

def updateData():
    global histNum
    global classNum

    quantImages = len(images)

    if str(op) == "0":
        histNum += quantImages
        return updateDataAux()
    else:
        classNum += quantImages
        return updateDataAux()

def checkStatus(status):
    if status:
        updateData()
        writeLog()
        return
    else:
        writeLog()
        sys.exit()

def cleanFiles():
    os.remove("./images.json")
    return

def main():
    global genError
    global op

    readConfigFile()
    readImages()
    readData()
    #cleanFiles()

    op = sys.argv[1]

    if str(op) == "0":
        status, genError = histogram.applyHistogram(images, histNum, dirH)
        return checkStatus(status)
    else:
        print("ES 1")
        return

if __name__ == "__main__":
    main()
    sys.exit()