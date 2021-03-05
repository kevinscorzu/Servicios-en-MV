from PIL import Image, ImageOps, ImageColor

classError = None
rCount = None
gCount = None
bCount = None

# Función encargada de convertir un pixel rgb en hsv
# Con el propósito de facilitar su clasificación
def rgbToHsv(r, g, b):
    r, g, b = r/255, g/255, b/255
    maximo = max(r, g, b)
    minimo = min(r, g, b)
    dif = maximo - minimo

    if dif == 0:
        h = 0
    elif maximo == r:
        h = (60 * ((g - b) / dif) + 360) % 360
    elif maximo == g:
        h = (60 * ((b - r) / dif) + 120) % 360
    elif maximo == b:
        h = (60 * ((r - g) / dif) + 240) % 360
    if maximo == 0:
        s = 0
    else:
        s = (dif / maximo) * 100
    v = maximo * 100

    return round(h), round(s), round(v)

# Función auxiliar secundaria de applyClassification()
def applyClassificationAux2(h, s, v):
    global rCount
    global gCount
    global bCount

    if v < 50:
        return
    elif s < 15:
        return
    elif h < 10:
        rCount += 1
        return
    elif 80 < h < 100:
        gCount += 1
        return
    elif 210 < h < 230:
        bCount += 1
        return
    else:
        return

# Función auxiliar de applyClassification()
def applyClassificationAux(image, number, direc):
    global classError
    global rCount
    global gCount
    global bCount

    try:
        image.convert('RGB')
        width, height = image.size
        i = 0
        j = 0
        rCount = 0
        bCount = 0
        gCount = 0

        while (i != width):
            while (j != height):
                r, g, b = image.getpixel((i, j))
                h, s, v = rgbToHsv(r, g, b)
                applyClassificationAux2(h, s, v)
                j += 1
            i += 1
            j = 0
            
        values = {"r": rCount, "g": gCount, "b": bCount}
        color = max(values.items(), key=lambda i: i[1])[0]

        if (color == "r"):
            image.save(direc + "/Rojo/classification" + str(number) + ".png")
            return 1
        elif (color == "g"):
            image.save(direc + "/Verde/classification" + str(number) + ".png")
            return 1
        elif (color == "b"):
            image.save(direc + "/Azul/classification" + str(number) + ".png")
            return 1
        else:
            image.save(direc + "/Desconocido/classification" + str(number) + ".png")
            return 1
    except:
        classError = "An error ocurred while classificating the image, exiting"
        print(classError)
        return 0

# Función encargada de clasificar las imágenes por color que fueron enviadas por el cliente
def applyClassification(imageList, imagesSizes, number, direc):
    for i in imagesSizes:
        if not applyClassificationAux(imageList[i[0]], number, direc):
            return 0, classError     
        number += 1

    return 1, classError