import os
import string
from tkinter import image_names
from PIL import Image
import numpy as np
import random
import glob
import subprocess
# Crop with tranlation
def cropTransparent2(image):
    shape = image.size
    reduce = 10
    rw = shape[0] - (shape[0] // reduce) * reduce
    rh = shape[1] - (shape[1] // reduce) * reduce
    print(rw, rh)

    maxX, maxY, minX, minY = 0, 0, shape[0],shape[1]
    img = image.resize((shape[0] // reduce, shape[1] // reduce))
    shape = img.size
    img = np.array(img)
    transparent = img[0][0]
    transparent2 = img[-1][-1]
    for i in range(shape[1]):
        b = False
        for j in range(shape[0]):
            if (img[i][j] != transparent).all() and (img[i][j] != transparent2).all():
                maxX = max(maxX, j)
                minX = min(minX, j)
                b = True
        if b:
            maxY = max(maxY, i)
            minY = min(minY, i)
    minX = minX * reduce + rw
    minY = minY * reduce + rh
    maxX = maxX * reduce + rw
    maxY = maxY * reduce + rh
    area = (minX, minY, maxX, maxY)
    return image.crop(area)

def cropTransparent(image):
    shape = image.size
    maxX, maxY, minX, minY = 0, 0, shape[0], shape[1]
    img = np.array(image)
    transparent = img[0][0]
    transparent2 = img[-1][-1]
    for i in range(shape[1]):
        b = False
        for j in range(shape[0]):
            if img[i][j][-1] < 100:
                maxX = max(maxX, j)
                minX = min(minX, j)
                b = True
        if b:
            maxY = max(maxY, i)
            minY = min(minY, i)     
    area = (minX, minY, maxX, maxY)
    return image.crop(area)
    # return image.crop(image.getbbox())


def CropTransparent(dir):
    paths = os.listdir(dir)
    for i in paths:
        path = os.path.join(dir, i)
        if os.path.isdir(path):
            CropTransparent(path)
        else:
            image = Image.open(path)
            croppedImg = cropTransparent(image)
            croppedImg.save(path)
            print(f'Cropped {path}')

def checkForground(dir):
    ls = os.listdir(dir)
    b = False
    for i in ls:
        path = os.path.join(dir, i)
        if os.path.isdir(path):
            b = b or  checkForground(path)
        else:            
            try:
                img = Image.open(path)
                img.paste(img, (0,0), img)
            except Exception as e:
                if str(e) == 'bad transparency mask':
                    print(e, path)
                    b = True
    return b

def randomFilename():
    letters = string.ascii_lowercase + string.ascii_uppercase
    return ''.join(random.choice(letters) for _ in range(10))


def renameImages(dir):
    ls = os.listdir(dir)
    for i in ls:
        path = f'{dir}/{i}'
        images = os.listdir(path)
        for j in range(len(images)):
            ext = images[j].split('.')[-1]
            os.rename(f'{path}/{images[j]}', f'{path}/{randomFilename()}.{ext}')
            # print(f'{path}/{images[j]}', f'{path}/{randomFilename()}.{ext}')
        
        images = os.listdir(path)
        for j in range(len(images)):
            ext = images[j].split('.')[-1]
            os.rename(f'{path}/{images[j]}', f'{path}/{i} {j + 1 }.{ext}')

def map_range(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def changeTransparency(imgPath, factor):
    img = Image.open(imgPath)
    # img.show()
    # factor = float(input('Factor de aumento de transparencia: '))
    nimg = np.array(img)
    width, height, _ = nimg.shape
    for i in range(width):
        for j in range(height):
            if nimg[i][j][3] != 0:
                nimg[i][j][3] = max(int(nimg[i][j][3] * factor), 0)
    nimg = Image.fromarray(nimg)
    # nimg.show()
    # if input('Save? y/n ')[0] == 'y':
    nimg.save(imgPath)
    #     return True
     
    return False
    


if __name__ == '__main__':
    pass
    # CropTransparent('images/plastics')
    # renameImages('images/plastics')
    # checkForground('images/plastics')
    # path = 'images\plastics\gloves'
    # imgPaths = [os.path.join(path, i) for i in os.listdir(path)]
    # for imgPath in imgPaths:
    #     # while True:
    #     rn = random.uniform(0.8, 0.9)
    #     print(rn)
    #     changeTransparency(imgPath, rn)
            


