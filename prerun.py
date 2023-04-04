import os
import string
from tkinter import image_names
from PIL import Image
import numpy as np
import random
import glob
import subprocess
# Crop with tranlation
def crop_transparent2(image):
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

def crop_transparent(image):
    """
    image: Image loaded with pillow

    Crop just the part of the image needed by getting the bounds of an object 
    given its just a PNG file and object is all the parts that are not transparent 
    """
    shape = image.size
    maxX, maxY, minX, minY = 0, 0, shape[0], shape[1]
    img = np.array(image)
    transparent = img[0][0]
    transparent2 = img[-1][-1]

    # Get the minimum and maximum coordenates of an object
    for i in range(shape[1]):
        b = False
        for j in range(shape[0]):
            # check the pixel transparency if its not transparente then 
            # update the bound of the object
            if img[i][j][-1] < 100:
                maxX = max(maxX, j)
                minX = min(minX, j)
                b = True
        # if a new bound is found in the image matrix column then update the 
        # bounds in the rows
        if b:
            maxY = max(maxY, i)
            minY = min(minY, i)     
    area = (minX, minY, maxX, maxY)
    return image.crop(area)
    # return image.crop(image.getbbox())


def Crop_transparent(dir):
    """
    dir: Directory that contains the directories of the images

    Loop in all the directories and images and crop them
    """
    paths = os.listdir(dir)
    for i in paths:
        path = os.path.join(dir, i)
        # If its a derctory recurusively itself with the directory name
        if os.path.isdir(path):
            Crop_transparent(path)
        else:
            image = Image.open(path)
            croppedImg = crop_transparent(image)
            croppedImg.save(path)
            print(f'Cropped {path}')

def check_forground(dir):
    """
    dir: Directory where are the directories that contain images

    Check the if the image transparency background is good, some images include pixels that are 
    not fully transparent like shadows
    """
    ls = os.listdir(dir)
    b = False
    for i in ls:
        path = os.path.join(dir, i)
        # if its a directory make a recursive call with the new directory
        if os.path.isdir(path):
            b = b or  check_forground(path)
        else:            
            # check the trasnparecy if its not it will throw an error
            try:
                img = Image.open(path)
                img.paste(img, (0,0), img)
            except Exception as e:
                if str(e) == 'bad transparency mask':
                    print(e, path)
                    b = True
    return b

def random_filename():
    letters = string.ascii_lowercase + string.ascii_uppercase
    return ''.join(random.choice(letters) for _ in range(10))


def rename_images(dir):
    ls = os.listdir(dir)
    for i in ls:
        path = f'{dir}/{i}'
        images = os.listdir(path)
        for j in range(len(images)):
            ext = images[j].split('.')[-1]
            os.rename(f'{path}/{images[j]}', f'{path}/{random_filename()}.{ext}')
            # print(f'{path}/{images[j]}', f'{path}/{randomFilename()}.{ext}')
        
        images = os.listdir(path)
        for j in range(len(images)):
            ext = images[j].split('.')[-1]
            os.rename(f'{path}/{images[j]}', f'{path}/{i} {j + 1 }.{ext}')

def map_range(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def change_transparency(imgPath, factor):
    """
    factor: factor of transparency to be added 

    Some images do not have enough transparency like plastic bottles or cups 
    """
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
    Crop_transparent('images/plastics')
    rename_images('images/plastics')
    check_forground('images/plastics')

    # change transparency, this should be done carefully because 
    # not all images need to be transparent
    
    # path = 'images\plastics\gloves'
    # imgPaths = [os.path.join(path, i) for i in os.listdir(path)]
    # for imgPath in imgPaths:
    #     # while True:
    #     rn = random.uniform(0.8, 0.9)
    #     print(rn)
    #     change_transparency(imgPath, rn)