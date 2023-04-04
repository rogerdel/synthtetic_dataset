import os
import cv2 as cv
import random

"""
Visualize generated images with opencv showign the image and bounding box
"""

def get_points(x, y, w, h , shape):
    """
    Return image coordenates from YOLO format
    """
    x1 = int((x - w / 2) * shape[1])
    y1 = int((y - h / 2) * shape[0])
    x2 = int((x + w / 2) * shape[1])
    y2 = int((y + h / 2) * shape[0])
    return x1,y1,x2,y2

def get_data(name):
    """
    name: File name of the text file that contains coordnates

    Read file with coordenates
    """
    lines = []
    with open (name, 'r') as f:
        lns = f.read().splitlines()
        for ln in lns:
            line = ln.split(' ')
            for i in range(len(line)):
                line[i] =int(line[i]) if  i == 0 else float(line[i])
            lines.append(line)
    return lines

def scale(img, scale):
    """
    img: Image 
    scale: New scale for the image
    """
    width = int(img.shape[1] * scale / 100)
    height = int(img.shape[0] * scale / 100)
    dim = (width, height)
    return cv.resize(img, dim, interpolation = cv.INTER_AREA)

def read_image(name, rev_class):
    img = cv.imread(f'{name}.jpg')
    print(name)
    # img = scale(img, 15)
    width, height, _ = img.shape
    # print(width, height)

    # Scale up image when its too big for the scren or its too small to be shown
    if width > 1200 or height > 1200:
        val = max(width, height)
        img = scale(img, (1200/val)*100)
    if width < 400 or height < 400:
        img = scale(img, 200)

    data = get_data(f'{name}.txt')
    cv.putText(img, str(len(data)), (10, 50 ), cv.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (255, 255, 0))
    # add bounding boxes in the image
    for i in data:
        c, x,y,w,h = i
        x1,y1,x2,y2 = get_points(x,y,w,h, img.shape)
        cv.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv.putText(img, rev_class[c], (x1 + 5, y1 - 10 ), cv.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0))
    cv.imshow('Image', img)
    cv.waitKey(0)

def get_names(file):
    with open(file, 'r') as f:
        return f.read().splitlines()

def main(imags):
    dir = 'dataset'
    reve = get_names('obj.names')
    img_paths = os.listdir(dir)
    c = 0
    while True:
        file = random.choice(img_paths)
        name = file.split('.')[0]
        ext = file.split('.')[1]
        if ext == 'txt':
            read_image(f'{dir}/{name}', reve)
            c += 1
            if c == imags:
                break
def test():
    i = 0
    dir = 'dataset'
    reve = get_names('obj.names')
    img_paths = os.listdir(dir)
    for file in img_paths:
        name = file.split('.')[0]
        ext = file.split('.')[1]
        if ext == 'txt':
            read_image(f'{dir}/{name}', reve)
            i += 1 

if __name__ == '__main__':
    # test()
    main(1)