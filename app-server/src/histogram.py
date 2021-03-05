from PIL import Image, ImageOps

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
            finalEqualizedImage.save(direc + "/histogram" + str(number) + ".png")
            return 1
        else:
            equalizedImage = ImageOps.equalize(image, mask = None)
            equalizedImage.save(direc + "/histogram" + str(number) + ".png")
            return 1
    except:
        histError = "An error ocurred while applying the histogram equalization, exiting"
        print(histError)
        return 0

def applyHistogram(imageList, imagesSizes, number, direc):
    for i in imagesSizes:
        if not applyHistogramAux(imageList[i[0]], number, direc):
            return 0, histError     
        number += 1

    return 1, histError