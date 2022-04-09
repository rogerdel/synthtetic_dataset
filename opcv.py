import os
import cv2 as cv
import random

def getPoints(x, y, w, h , shape):
    x1 = int((x - w / 2) * shape[1])
    y1 = int((y - h / 2) * shape[0])
    x2 = int((x + w / 2) * shape[1])
    y2 = int((y + h / 2) * shape[0])
    return x1,y1,x2,y2

def getData(name):
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
    width = int(img.shape[1] * scale / 100)
    height = int(img.shape[0] * scale / 100)
    dim = (width, height)
    return cv.resize(img, dim, interpolation = cv.INTER_AREA)

def readImage(name, revClass):
    img = cv.imread(f'{name}.jpg')
    # img = scale(img, 15)
    
    data = getData(f'{name}.txt')
    for i in data:
        c, x,y,w,h = i
        x1,y1,x2,y2 = getPoints(x,y,w,h, img.shape)
        cv.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv.putText(img, revClass[c], (x1 + 5, y1 - 10 ), cv.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0))
    cv.imshow('Image', img)
    cv.waitKey(0)

def getnames(file):
    with open(file, 'r') as f:
        return f.read().splitlines()

if __name__ == '__main__':
    dir = 'dataset'
    reve = getnames('obj.names')
    imgpahts = os.listdir(dir)
    imags = 10
    for i in range(imags):
        name = random.choice(imgpahts).split('.')[0]
        readImage(f'{dir}/{name}', reve)
        