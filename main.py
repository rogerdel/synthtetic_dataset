import time
from PIL import Image
import os
import random 
import concurrent.futures
from transformations import rotate, resizeRandom, scale

from data import imgDir, backDir, saveDir, probManyObjs, probAddObj, resizeProb, imagesperClass
from utils import randomFilename, chooseImage, loadClasses, convertYolo

def joinImages(backImgPath, imgPaths):
    """
    Generate a new image using using a background image and one or more object images,
    Saving a new image and a txt file with the coordenates and the type of objects in the image
    """
    try:
        background = Image.open(backImgPath)
        bboxs = []
        allClasses = []
        for i in range(len(imgPaths)):
            # load class number
            cls = classes[imgPaths[i].split('/')[-2]]
            img = Image.open(imgPaths[i])
            # Transformations for the object image for more diversity
            img = rotate(img)
            img = resizeRandom(background, img)
            imgW, imgH = img.size
            bw, bh = background.size
            b = i == 0
            # Given that adding many images is not guaranteed, at least one iamge has to be added 
            # in this case the first image will be added, if the first object image is too big for the background image 
            # the object image will be resized in half the resoltion until it fits
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
            # Skip the object image when it's not the first image and the object image is too big for the background image 
            elif imgW > bw or imgH > bh:
                continue
            # Random location in the background image
            x = random.randint(0, bw - int(imgW))
            y = random.randint(0, bh - int(imgH))
            
            # When it's not the first image generate coordantes that don't collide with previous ones
            if not b:
                # Cheek 100 times if the new image can be added in a random place with no collitions
                # Not using while True becuase some images can't be added since the background image isn't big enough for many images
                # or the added images already ocupy enough of the background image space, therefore a new image can't be added
                # and using while True can result in an infinite loop
                for i in range(100):
                    b = True
                    # check previous added coordenates of images
                    for i in bboxs:
                        x1, y1, x2, y2 = i
                        # check if the new coordenates are not inside or collide with previous coordenate
                        b = b and (x1 >= x + imgW or x >= x2) and (y2 >= y or y + imgH >= y1)     
                    # if there is no collition, then everythng is ok and the coordentaes can be used
                    if b:
                        break
                    # if the coordenates collide then use generate new ones
                    else: 
                        x = random.randint(0, bw - imgW)
                        y = random.randint(0, bh - imgH)
            # Add a new coordenate if the it's the first image or dosen't collide with other coordenates
            if b:
                bboxs.append((x, y, x + imgW, y + imgH))
                background.paste(img, (x, y), img)
                allClasses.append(cls)
        # Generaete a random name and ensure the name dosen't belong to an existing file
        fileName = randomFilename()
        while os.path.exists(f'{fileName}.jpg'):
            fileName = randomFilename()
        # Resize the generated image randomly just to add more variation
        if random.random() < resizeProb:
            background = scale(background, random.randint(30, 50))
        # save the generated image
        background.save(f'{fileName}.jpg')
        # save the file with the objects number and image coordenates
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
    """ 
    Returns an array of image paths
    Background image
    object images 
    """
    # List of all background image
    backImgPaths = [f'{backDir}/{i}' for i in os.listdir(backDir)] 
    # List of the directories names of the object images
    classdirs = [f'{imgDir}/{i}' for i in os.listdir(imgDir)]
    lnc = len(classdirs)
    backImgs = []
    images = []
    for _ in range(imgsperClass):
        for classdir in classdirs:
            # Add random image from a classdir
            imgs = [chooseImage(classdir)]
            # probManyObjs: Probabilty of use just one obejct image or use more than one
            if random.random() < probManyObjs:
                for i in range(lnc):
                    # probAddObj: probabilty of choosing a new image from a random type
                    if random.random() < probAddObj:
                        imgs.append(chooseImage(classdirs[i]))
            images.append(imgs)
            backImgs.append(random.choice(backImgPaths))
    return backImgs, images


def main(imgsperClass = 1):
    # Add 20% more of images for testing porpuses
    imgsperClass += int(imagesperClass * 0.2)
    if not os.path.exists(saveDir):
        os.mkdir(saveDir)
    backImgs, imgs = associate(imgsperClass)
    start = time.perf_counter()
    # Genrate new images using threads
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(joinImages, backImgs, imgs)
    end = time.perf_counter()
    print(f'TOTAL TIME: {end -  start}')

def setseed():
    """
    Sets a random seed and saves in seed.txt file,
    mainly for debugin porpuses in case a bug is spoted in a genrated image, the seed can 
    be used to run it again with using the seed
    """
    seed = random.randint(0,10000)
    random.seed(seed)
    with open('seed.txt', 'w') as f:
        f.write(f'{seed}')

if __name__ == '__main__':
    # To avoid DecompressionBombError from pillow library when images are too big, MAX_IMAGE_PIXELS is set to None
    Image.MAX_IMAGE_PIXELS = None
    setseed()
    classes        = loadClasses(imgDir)
    main(imagesperClass)