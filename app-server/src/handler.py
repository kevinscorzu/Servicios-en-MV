import sys
import json
import histogram
import classification
from datetime import datetime
import os
from pathlib import Path
import base64
import io
from PIL import Image

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
root = None

def projectRoot() -> Path:
    return Path(__file__).parent.parent

def createStringAux2(message, status):
    message += "Status: " + status + ", "
    message += "Datetime: " + str(datetime.now()) + "\n"

    return message

def createStringAux(message):
        if genError is not None:
            return createStringAux2(message, genError)
        else:
            if str(op) == "0":
                return createStringAux2(message, "Histogram Completed Successfuly")
            else:
                return createStringAux2(message, "Classification Completed Successfuly")

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
                filesAux += "classification" + str(rClassNum) + ".png, "
                rClassNum += 1
            files = filesAux

        message += "Files: " + files
        return createStringAux(message)

def writeLog():
    message = createString()

    try:
        with open(root + dirL + "/log.txt", "a") as f:
            f.write(message)
            f.close()
        return
    except:
        with open(root + dirL + "/log.txt", "w") as f:
            f.write(message)
            f.close()
        return

def readImages():
    global images
    global client
    global genError

    try:
        with open(root + "/images.json") as f:
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
        with open(root + "/config.conf") as f:
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
        with open(root + "/data.json") as f:
            jsonData = json.load(f)
            f.close()
        histNum = jsonData["histNum"]
        classNum = jsonData["classNum"]
        rHistNum = histNum
        rClassNum = classNum
        return
    except:
        data = {}
        histNum = 0
        classNum = 0
        rHistNum = 0
        rClassNum = 0
        data["histNum"] = 0
        data["classNum"] = 0
        with open(root + "/data.json", "w") as f:
            json.dump(data, f)
            f.close()
        return

def updateDataAux():
    data = {}
    data["histNum"] = histNum
    data["classNum"] = classNum
    with open(root + "/data.json", "w") as f:
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
    if status == 1:
        updateData()
        writeLog()
        return
    else:
        writeLog()
        sys.exit()

def cleanFiles():
    os.remove(root + "/images.json")
    return

def decryptAndSortImages():
    imageList = {}
    imagesSizes = {}
    index = 0
 
    for x in images:
        image = base64.b64decode(str(x))       
        image = Image.open(io.BytesIO(image))
        w, h = image.size
        imageSize = w * h
        imagesSizes[index] = imageSize
        imageList[index] = image
        index += 1
    
    imagesSizes = sorted(imagesSizes.items(), key=lambda x: x[1])

    return imageList, imagesSizes

def createDirs():
    try:
        os.mkdir(root + dirC + "/Rojo")
        os.mkdir(root + dirC + "/Verde")
        os.mkdir(root + dirC + "/Azul")
        return
    except:
        return

def main():
    global genError
    global op
    global root

    root = str(projectRoot())
    readConfigFile()
    readImages()
    readData()
    createDirs()
    #cleanFiles()

    op = sys.argv[1]

    imageList, imagesSizes = decryptAndSortImages()

    if str(op) == "0":
        status, genError = histogram.applyHistogram(imageList, imagesSizes, histNum, root + dirH)
        return checkStatus(status)
    else:
        status, genError = classification.applyClassification(imageList, imagesSizes, classNum, root + dirC)
        return checkStatus(status)

if __name__ == "__main__":
    main()
    sys.exit()