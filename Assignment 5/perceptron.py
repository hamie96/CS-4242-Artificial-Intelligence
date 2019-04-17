from PIL import Image

def checkIfBright():
    total_value = 0

    im = Image.open('checker.jpg')
    pix = im.load()
    size = im.size
    x_size = size[0]
    y_size = size[1]
    pixels = []

    for i in range(x_size):
        for j in range(y_size):
            pixels.append(pix[i,j])

    for i in pixels:
        if i[0] == 255:
            total_value = total_value + .25
        else:
            total_value = total_value + -.25 
    isImageBright(total_value)


def isImageBright(total_value):
    if total_value > -.1:
        print("The output is bright!")
    else:
        print("The output is dark!")
    print("Your total weight is " + str(total_value))

checkIfBright()
