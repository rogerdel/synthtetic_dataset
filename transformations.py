import random as rnd
import math
from PIL import Image

def rotate(img):
    img = img.rotate(rnd.randint(0, 359), expand = True)
    img = img.crop(img.getbbox())
    return img
    
def scaleDown(img, bw, bh):
    minAspectRatio = 0.25
    scale = rnd.random()
    w, h = img.size 
    while True:
        wt = w * scale; ht = h * scale
        ratio = wt / bw + ht / bh
        if ratio < minAspectRatio:
            scale += rnd.random()
        else:
            break
    w = math.ceil(w * scale)
    h = math.ceil(h * scale)
    return img.resize((w, h))

def scaleUp(img, bw, bh):
    w, h = img.size 
    scale =  rnd.randint(2,10)
    while True:
        if w * scale > bw or h * scale >= bh:
            scale /= rnd.randint(1,4)
        else:
            break
    w = int(w * scale) 
    h = int(h * scale)    
    return img.resize((w, h))

def resizeRandom(backImg, img):
    bw, bh = backImg.size
    if rnd.random() < 0.5:
        if rnd.random() < 0.5:
            img = scaleDown(img, bw, bh)
        else:
            img = scaleUp(img, bw, bh)
    return img

def scale(img, factor):
    width, height = img.size
    width = int(width * factor / 100)
    height = int(height * factor / 100)
    return img.resize((width, height))

if __name__ == '__main__':
    pass
    # img = Image.open('images/cookies/oreo/oreo 1.png')
    # img = scale(img, 400)
    # img.save('images/cookies/oreo/oreo 1.png')