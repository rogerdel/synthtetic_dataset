import time
from PIL import Image
import numpy as np
import os
import random as rnd
import string
import concurrent.futures
from transformations import rotate, resizeRandom, scale

def loadClasses(dir):
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

def randomFilename():
    name = ''.join(rnd.choice(letters) for _ in range(filenameSize))
    return f'{saveDir}/{name}'

def convertYolo(x1,y1,x2,y2, shape):
    x = ((x1 + x2) / 2) / shape[1]
    y = ((y1 + y2) / 2) / shape[0]
    h = abs(y1 - y2) / shape[0]
    w = abs(x2 - x1) / shape[1]
    return x, y, w, h

def joinImages(backImgPath, imgPaths):
    try:
        background = Image.open(backImgPath)
        bboxs = []
        allClasses = []
        for i in range(len(imgPaths)):
            cls = classes[imgPaths[i].split('/')[-2]]
            img = Image.open(imgPaths[i])
            img = rotate(img)
            img = resizeRandom(background, img)
            imgW, imgH = img.size
            bw, bh = background.size
            b = i == 0
            if b:
                while True:
                    sw = False
                    if imgW > bw or imgH > bh:
                        sw = True
                        imgW /= 2
                        imgH /= 2
                    else:
                        break  
                if sw:
                    img = img.resize((imgW, imgH))
            elif imgW > bw or imgH > bh:
                continue 
            x = rnd.randint(0, bw - imgW)
            y = rnd.randint(0, bh - imgH)

            if not b:
                for i in range(100):
                    b = True
                    for i in bboxs:
                        x1, y1, x2, y2 = i
                        # consider changing for something like this
                        
                        # rect1.x < rect2.x + rect2.width &&
                        # rect1.x + rect1.width > rect2.x &&
                        # rect1.y < rect2.y + rect2.height &&
                        # rect1.height + rect1.y > rect2.y

                        b = b and (x1 >= x + imgW or x >= x2) and (y2 >= y or y + imgH >= y1)     
                    if b:
                        break
                    else: 
                        x = rnd.randint(0, bw - imgW)
                        y = rnd.randint(0, bh - imgH)
            if b:
                bboxs.append((x, y, x + imgW, y + imgH))
                background.paste(img, (x, y), img)
                allClasses.append(cls)

        fileName = randomFilename()
        while os.path.exists(f'{fileName}.jpg'):
            fileName = randomFilename()    
        if rnd.random() < resizeProb:
            background = scale(background, rnd.randint(5, 30))
        background.save(f'{fileName}.jpg')
        with open(f'{fileName}.txt', 'w') as f:
            for i in range(len(bboxs)):
                x, y, w, h = convertYolo(bboxs[i][0], bboxs[i][1], bboxs[i][2], bboxs[i][3], (bh,bw))
                f.write(f'{allClasses[i]} {x} {y} {w} {h}')
                if i != len(bboxs) -1:
                    f.write('\n')
    except Exception as e:
        print(e)
def chooseImage(classdir):
    imgPahts = [f'{classdir}/{img}' for img in os.listdir(classdir)]
    return rnd.choice(imgPahts)

def associate(imgsperClass):
    backImgPaths = [f'{backDir}/{i}' for i in os.listdir(backDir)] 
    classdirs = [f'{imgDir}/{i}' for i in os.listdir(imgDir)]
    lnc = len(classdirs)
    backImgs = []
    images = []
    for _ in range(imgsperClass):
        for classdir in classdirs:
            imgs = [chooseImage(classdir)]
            # Add random images
            if rnd.random() > addImgProb:
                distribution = np.random.random((1, lnc))[0]
                for i in range(lnc):
                    if distribution[i] > 0.5:
                        imgs.append(chooseImage(classdirs[i]))
            images.append(imgs)
            backImgs.append(rnd.choice(backImgPaths))
    return backImgs, images


def main(imgsperClass = 1):
    imgsperClass += int(imagesperClass * 0.2)
    if not os.path.exists(saveDir):
        os.mkdir(saveDir)
    backImgs, imgs = associate(imgsperClass)
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(joinImages, backImgs, imgs)
    end = time.perf_counter()
    print(f'TOTAL TIME: {end -  start}')


if __name__ == '__main__':
    letters        = string.ascii_lowercase + string.ascii_uppercase
    imgDir         = 'images/plastics'
    backDir        = 'images/background'
    saveDir        = 'dataset'
    classes        = loadClasses(imgDir)
    addImgProb     = 0.6
    resizeProb     = 0.96
    filenameSize   = 10
    imagesperClass = 2
    main(imagesperClass)