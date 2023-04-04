import random as rnd 
from data import filename_size
import os
import string
from data import save_dir

def convert_yolo(x1,y1,x2,y2, shape):
    """
    Convert coordenates of images from x,y coordante of the image to 
    YOlO format
    """
    x = ((x1 + x2) / 2) / shape[1]
    y = ((y1 + y2) / 2) / shape[0]
    h = abs(y1 - y2) / shape[0]
    w = abs(x2 - x1) / shape[1]
    return x, y, w, h

def random_filename():
    """
    Genrate a sring of random letters
    """
    letters        = string.ascii_lowercase + string.ascii_uppercase
    name = ''.join(rnd.choice(letters) for _ in range(filename_size))
    return f'{save_dir}/{name}'


def load_classes(dir):
    """
    dir: Directory where the directores of the object images are stored
   
    Load the classes of the objects from the directories names and save it 
    in obj.names file
    """
    ls = os.listdir(dir)
    classes = {}
    reverse_classes = {}
    with open ('obj.names', 'w') as f:
        for i in range(len(ls)):
            classes[ls[i]] = i 
            reverse_classes[i] = ls[i] 
            f.write(ls[i])
            if i != len(ls) - 1:
                f.write('\n')
    return classes

def choose_image(class_dir):
    """
    Choose a random image from a directory
    """
    img_paths = [f'{class_dir}/{img}' for img in os.listdir(class_dir)]
    return rnd.choice(img_paths)