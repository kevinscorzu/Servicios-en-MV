from PIL import Image, ImageOps
import base64
import io

histError = None

def applyHistogramAux(image, number, direc):
    global histError

    try:
        if image.mode == 'RGBA':
            r, g, b, a = image.split()
            rgbImage = Image.merge('RGB', (r,g,b))
            equalizedImage = ImageOps.equalize(rgbImage, mask = None)
            r2,g2,b2 = equalizedImage.split()
            finalEqualizedImage = Image.merge('RGBA', (r2,g2,b2,a))
            finalEqualizedImage.save("." + direc + "/histogram" + str(number) + ".png")
            return 1
        else:
            equalizedImage = ImageOps.equalize(image, mask = None)
            equalizedImage.save("." + direc + "/histogram" + str(number) + ".png")
            return 1
    except:
        histError = "An error ocurred while applying the histogram equalization, exiting"
        print(histError)
        return 0

def applyHistogram(b64ImageList, number, direc):
    imageList = {}
    imagesSizes = {}
    index = 0
 
    for x in b64ImageList:
        image = base64.b64decode(str(x))       
        image = Image.open(io.BytesIO(image))
        w, h = image.size
        imageSize = w * h
        imagesSizes[index] = imageSize
        imageList[index] = image
        index += 1
    
    imagesSizes = sorted(imagesSizes.items(), key=lambda x: x[1])

    for i in imagesSizes:
        if not applyHistogramAux(imageList[i[0]], number, direc):
            return 0, histError     
        number += 1

    return 1, histError