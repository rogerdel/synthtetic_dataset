import time
from PIL import Image
import os
import random 
import concurrent.futures
from transformations import rotate, resizeRandom, scale

from data import imgDir, backDir, saveDir, probManyObjs, probAddObj, resizeProb, imagesperClass
from utils import randomFilename, chooseImage, loadClasses, convertYolo

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
                sw = False
                while True:
                    if imgW > bw or imgH > bh:
                        sw = True
                        imgW //= 2
                        imgH //= 2
                    else:
                        break
                if sw:
                    img = img.resize((imgW, imgH))
            elif imgW > bw or imgH > bh:
                continue

            x = random.randint(0, bw - int(imgW))
            y = random.randint(0, bh - int(imgH))

            if not b:
                for i in range(100):
                    b = True
                    for i in bboxs:
                        x1, y1, x2, y2 = i
                        b = b and (x1 >= x + imgW or x >= x2) and (y2 >= y or y + imgH >= y1)     
                    if b:
                        break
                    else: 
                        x = random.randint(0, bw - imgW)
                        y = random.randint(0, bh - imgH)
            if b:
                bboxs.append((x, y, x + imgW, y + imgH))
                background.paste(img, (x, y), img)
                allClasses.append(cls)

        fileName = randomFilename()
        while os.path.exists(f'{fileName}.jpg'):
            fileName = randomFilename()
        if random.random() < resizeProb:
            background = scale(background, random.randint(30, 50))
        background.save(f'{fileName}.jpg')
        with open(f'{fileName}.txt', 'w') as f:
            for i in range(len(bboxs)):
                x, y, w, h = convertYolo(bboxs[i][0], bboxs[i][1], bboxs[i][2], bboxs[i][3], (bh,bw))
                f.write(f'{allClasses[i]} {x} {y} {w} {h}')
                if i != len(bboxs) -1:
                    f.write('\n')
    except Exception as e:
        print(e)
        print(backImgPath, imgPaths)
        print(fileName)

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
            if random.random() < probManyObjs:
                for i in range(lnc):
                    if random.random() < probAddObj:
                        imgs.append(chooseImage(classdirs[i]))
            images.append(imgs)
            backImgs.append(random.choice(backImgPaths))
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

def setseed():
    seed = random.randint(0,10000)
    random.seed(seed)
    with open('seed.txt', 'w') as f:
        f.write(f'{seed}')

if __name__ == '__main__':
    Image.MAX_IMAGE_PIXELS = None
    setseed()
    # random.seed(9898)
    classes        = loadClasses(imgDir)
    main(imagesperClass)