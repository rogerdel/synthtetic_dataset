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
    print(name)
    # img = scale(img, 15)
    width, height, _ = img.shape
    # print(width, height)
    if width > 1200 or height > 1200:
        val = max(width, height)
        img = scale(img, (1200/val)*100)
    if width < 400 or height < 400:
        img = scale(img, 200)

    data = getData(f'{name}.txt')
    cv.putText(img, str(len(data)), (10, 50 ), cv.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (255, 255, 0))
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

def main(imags):
    dir = 'dataset'
    reve = getnames('obj.names')
    imgpahts = os.listdir(dir)
    c = 0
    while True:
        file = random.choice(imgpahts)
        name = file.split('.')[0]
        ext = file.split('.')[1]
        if ext == 'txt':
            readImage(f'{dir}/{name}', reve)
            c += 1
            if c == imags:
                break
def test():
    i = 0
    dir = 'dataset'
    reve = getnames('obj.names')
    imgpahts = os.listdir(dir)
    for file in imgpahts:
        name = file.split('.')[0]
        ext = file.split('.')[1]
        if ext == 'txt':
            readImage(f'{dir}/{name}', reve)
            i += 1 

if __name__ == '__main__':
    # test()
    main(100)