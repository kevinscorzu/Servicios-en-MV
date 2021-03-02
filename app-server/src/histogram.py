from PIL import Image, ImageOps
import base64
import io

def applyHistogramAux(image, dir):
    try:
        if image.mode == 'RGBA':
            r, g, b, a = image.split()
            rgbImage = Image.merge('RGB', (r,g,b))
            equalizedImage = ImageOps.equalize(rgbImage, mask = None)
            r2,g2,b2 = equalizedImage.split()
            finalEqualizedImage = Image.merge('RGBA', (r2,g2,b2,a))
            finalEqualizedImage.save("." + dir + "/" + "test1" + ".png")
            return 1
        else:
            equalizedImage = ImageOps.equalize(image, mask = None)
            equalizedImage.save("." + dir + "/" + "test2" + ".png")
            return 1
    except:
        print("An error ocurred while applying the histogram equalization, exiting")
        return 0

def applyHistogram(imageList, dir):
    for x in imageList:
        image = base64.b64decode(str(x))       
        image = Image.open(io.BytesIO(image))
        if not applyHistogramAux(image, dir):
            return 0
    
    return 1