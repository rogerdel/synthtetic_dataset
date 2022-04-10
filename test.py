import os
from re import I
import time
import concurrent.futures
import random
from PIL import Image

from transformations import rotate, resizeRandom, scale
from data import imgDir, backDir, saveDir, resizeProb, imagesperClass
from utils import randomFilename, loadClasses, convertYolo


def associate():
    backImgPaths = [f'{backDir}/{i}' for i in os.listdir(backDir)] 
    classdirs = [f'{imgDir}/{i}' for i in os.listdir(imgDir)]
    backImgs = []
    images = []
    for classdir in classdirs:
        imgPahts = [f'{classdir}/{img}' for img in os.listdir(classdir)]
        for i in imgPahts:
            images.append(i)
            backImgs.append(random.choice(backImgPaths))
    return backImgs, images

def joinImages(backImgPath, imgPath):
    # try:
    background = Image.open(backImgPath)
    bboxs = []
    allClasses = []
    for i in range(3):
        cls = classes[imgPath.split('/')[-2]]
        img = Image.open(imgPath)
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
        x = random.randint(0, bw - imgW)
        y = random.randint(0, bh - imgH)

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

    fileName = imgPath.split('/')[-1].split('.')[0]
    fileName = f'{saveDir}/{fileName}'
    while os.path.exists(f'{saveDir}/{fileName}.jpg'):
        fileName = randomFilename()
    if random.random() < resizeProb:
        background = scale(background, random.randint(5, 30))
    background.save(f'{fileName}.jpg')
    with open(f'{fileName}.txt', 'w') as f:
        for i in range(len(bboxs)):
            x, y, w, h = convertYolo(bboxs[i][0], bboxs[i][1], bboxs[i][2], bboxs[i][3], (bh,bw))
            f.write(f'{allClasses[i]} {x} {y} {w} {h}')
            if i != len(bboxs) -1:
                f.write('\n')
    # except Exception as e:
    #     print(e)



def main():
    if not os.path.exists(saveDir):
        os.mkdir(saveDir)
    backImgs, imgs = associate()
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(joinImages, backImgs, imgs)
    end = time.perf_counter()
    print(f'TOTAL TIME: {end -  start}')

if __name__ == '__main__':
    Image.MAX_IMAGE_PIXELS = None
    classes = loadClasses(imgDir)
    main()