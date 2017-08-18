import numpy as np
from PIL import Image
import glob
import os
import image_slicer
import math

path = 'D:/Users/Jonathan/Desktop/cropped/*.jpg'
images = glob.glob(path)
colorpallette = []
for pic in images:
    img = Image.open(pic)
    arr = np.array(img)

    r = 0
    g = 0
    b = 0
    counter = 0
    for row in arr:
        for pixel in row:
            r += pixel[0]
            g += pixel[1]
            b += pixel[2]
            counter += 1

    ra = int(r/counter)
    ga = int(g/counter)
    ba = int(b/counter)
    thiscolor = []
    thiscolor.append(ra)
    thiscolor.append(ga)
    thiscolor.append(ba)
    colorpallette.append(thiscolor)


def average_image_color(filename):
    i = Image.open(filename)
    h = i.histogram()

    # split into red, green, blue
    r = h[0:256]
    g = h[256:256*2]
    b = h[256*2: 256*3]

    # perform the weighted average of each channel:
    # the *index* is the channel value, and the *value* is its weight
    return (
        sum(i*w for i, w in enumerate(r)) / sum(r),
        sum(i*w for i, w in enumerate(g)) / sum(g),
        sum(i*w for i, w in enumerate(b)) / sum(b)
    )

image_slicer.main.slice('D:/Users/Jonathan/Desktop/test_image/thecaptain.jpg', 32)

averages = []
for image in os.listdir('D:/Users/Jonathan/Desktop/test_image'):
    averages.append(average_image_color('D:/Users/Jonathan/Desktop/test_image/' + image))

for rgb in averages:
    closest = 196608
    for color in colorpallette:
        distance = math.sqrt(math.pow(rgb[0]-color[0], 2)+math.pow(rgb[1]-color[1], 2)+math.pow(rgb[2]-color[2], 2))
        if distance < closest:
            closest = distance
            match = [color[0], color[1], color[2]]
    print(rgb)
    print("matches")
    print(match)
    print("")

# We have the average color of each of the small images as well as the comic cover with the closes average color
# Need to figure out how to replace the small image with the comic cover and then use image_slicer to paste together

thecaptain = Image.open('D:/Users/Jonathan/Desktop/test_image/thecaptain_01_01.jpg')
width, height = thecaptain.size
tcarr = np.array(thecaptain)

img = Image.fromarray(tcarr, 'RGB')
img.save('my.png')
img.show()
