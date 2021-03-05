from PIL import Image, ImageOps

classError = None

def applyClassificationAux(image, number, direc):
    global classError

    try:
        if image.mode == 'RGBA':
            r, g, b, a = image.split()
            rgbImage = Image.merge('RGB', (r,g,b))
            equalizedImage = ImageOps.equalize(rgbImage, mask = None)
            r2,g2,b2 = equalizedImage.split()
            finalEqualizedImage = Image.merge('RGBA', (r2,g2,b2,a))
            finalEqualizedImage.save(direc + "/classification" + str(number) + ".png")
            return 1
        else:
            equalizedImage = ImageOps.equalize(image, mask = None)
            equalizedImage.save(direc + "/classification" + str(number) + ".png")
            return 1
    except:
        classError = "An error ocurred while classificating the images, exiting"
        print(classError)
        return 0

def applyClassification(imageList, imagesSizes, number, direc):
    for i in imagesSizes:
        if not applyClassificationAux(imageList[i[0]], number, direc):
            return 0, classError     
        number += 1

    return 1, classError