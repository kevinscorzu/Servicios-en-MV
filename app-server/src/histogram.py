from PIL import Image, ImageOps

histError = None

# Función auxiliar de applyHistogram()
def applyHistogramAux(image, number, direc):
    global histError

    try:
        image = image.convert('RGB')
        equalizedImage = ImageOps.equalize(image, mask = None)
        equalizedImage.save(direc + "/histogram" + str(number) + ".png")
        return 1
    except:
        histError = "An error ocurred while applying the histogram equalization, exiting"
        print(histError)
        return 0

# Función encargada de aplicar la equalización de histograma a las imágenes enviadas por el cliente
def applyHistogram(imageList, imagesSizes, number, direc):
    for i in imagesSizes:
        if not applyHistogramAux(imageList[i[0]], number, direc):
            return 0, histError     
        number += 1

    return 1, histError