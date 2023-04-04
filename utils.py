import random as rnd 
from data import filenameSize
import os
import string
from data import saveDir

def convertYolo(x1,y1,x2,y2, shape):
    """
    Convert coordenates of images from x,y coordante of the image to 
    YOlO format
    """
    x = ((x1 + x2) / 2) / shape[1]
    y = ((y1 + y2) / 2) / shape[0]
    h = abs(y1 - y2) / shape[0]
    w = abs(x2 - x1) / shape[1]
    return x, y, w, h

def randomFilename():
    """
    Genrate a sring of random letters
    """
    letters        = string.ascii_lowercase + string.ascii_uppercase
    name = ''.join(rnd.choice(letters) for _ in range(filenameSize))
    return f'{saveDir}/{name}'


def loadClasses(dir):
    """
    dir: Directory where the directores of the object images are stored
   
    Load the classes of the objects from the directories names and save it 
    in obj.names file
    """
    ls = os.listdir(dir)
    classes = {}
    reverseClasses = {}
    with open ('obj.names', 'w') as f:
        for i in range(len(ls)):
            classes[ls[i]] = i 
            reverseClasses[i] = ls[i] 
            f.write(ls[i])
            if i != len(ls) - 1:
                f.write('\n')
    return classes

def chooseImage(classdir):
    """
    Choose a random image from a directory
    """
    imgPahts = [f'{classdir}/{img}' for img in os.listdir(classdir)]
    return rnd.choice(imgPahts)