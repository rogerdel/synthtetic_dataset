import os
import string
from PIL import Image
import numpy as np
import random
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

if __name__ == '__main__':
    # CropTransparent('images/plastics')
    renameImages('images/plastics')
    # checkForground('images/plastics')