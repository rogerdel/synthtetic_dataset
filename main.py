import time
from PIL import Image
import os
import random 
import concurrent.futures
from transformations import rotate, resize_random, scale

from data import images_dir, background_dir, save_dir, prob_many_objs, prob_add_obj, resize_prob, images_per_class
from utils import random_filename, choose_image, load_classes, convert_yolo

def join_images(backImgPath, imgPaths):
    """
    Generate a new image using using a background image and one or more object images,
    Saving a new image and a txt file with the coordenates and the type of objects in the image
    """
    try:
        background = Image.open(backImgPath)
        bboxs = []
        all_classes = []
        for i in range(len(imgPaths)):
            # load class number
            cls = classes[imgPaths[i].split('/')[-2]]
            img = Image.open(imgPaths[i])
            # Transformations for the object image for more diversity
            img = rotate(img)
            img = resize_random(background, img)
            img_width, img_height = img.size
            background_width, background_height = background.size
            b = i == 0
            # Given that adding many images is not guaranteed, at least one iamge has to be added 
            # in this case the first image will be added, if the first object image is too big for the background image 
            # the object image will be resized in half the resoltion until it fits
            if b:
                sw = False
                while True:
                    if img_width > background_width or img_height > background_height:
                        sw = True
                        img_width //= 2
                        img_height //= 2
                    else:
                        break
                if sw:
                    img = img.resize((img_width, img_height))
            # Skip the object image when it's not the first image and the object image is too big for the background image 
            elif img_width > background_width or img_height > background_height:
                continue
            # Random location in the background image
            x = random.randint(0, background_width - int(img_width))
            y = random.randint(0, background_height - int(img_height))
            
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
                        b = b and (x1 >= x + img_width or x >= x2) and (y2 >= y or y + img_height >= y1)     
                    # if there is no collition, then everythng is ok and the coordentaes can be used
                    if b:
                        break
                    # if the coordenates collide then use generate new ones
                    else: 
                        x = random.randint(0, background_width - img_width)
                        y = random.randint(0, background_height - img_height)
            # Add a new coordenate if the it's the first image or dosen't collide with other coordenates
            if b:
                bboxs.append((x, y, x + img_width, y + img_height))
                background.paste(img, (x, y), img)
                all_classes.append(cls)
        # Generaete a random name and ensure the name dosen't belong to an existing file
        file_name = random_filename()
        while os.path.exists(f'{file_name}.jpg'):
            file_name = random_filename()
        # Resize the generated image randomly just to add more variation
        if random.random() < resize_prob:
            background = scale(background, random.randint(30, 50))
        # save the generated image
        background.save(f'{file_name}.jpg')
        # save the file with the objects number and image coordenates
        with open(f'{file_name}.txt', 'w') as f:
            for i in range(len(bboxs)):
                x, y, w, h = convert_yolo(bboxs[i][0], bboxs[i][1], bboxs[i][2], bboxs[i][3], (background_height,background_width))
                f.write(f'{all_classes[i]} {x} {y} {w} {h}')
                if i != len(bboxs) -1:
                    f.write('\n')
    except Exception as e:
        print(e)
        print(backImgPath, imgPaths)
        print(file_name)

def associate(imgsperClass):
    """ 
    Returns an array of image paths
    Background image
    object images 
    """
    # List of all background image
    background_img_paths = [f'{background_dir}/{i}' for i in os.listdir(background_dir)] 
    # List of the directories names of the object images
    class_dirs = [f'{images_dir}/{i}' for i in os.listdir(images_dir)]
    lnc = len(class_dirs)
    background_imgs = []
    images = []
    for _ in range(imgsperClass):
        for classdir in class_dirs:
            # Add random image from a classdir
            imgs = [choose_image(classdir)]
            # probManyObjs: Probabilty of use just one obejct image or use more than one
            if random.random() < prob_many_objs:
                for i in range(lnc):
                    # probAddObj: probabilty of choosing a new image from a random type
                    if random.random() < prob_add_obj:
                        imgs.append(choose_image(class_dirs[i]))
            images.append(imgs)
            background_imgs.append(random.choice(background_img_paths))
    return background_imgs, images


def main(imgs_per_class = 1):
    # Add 20% more of images for testing porpuses
    imgs_per_class += int(imgs_per_class * 0.2)
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    background_imgs, imgs = associate(imgs_per_class)
    start = time.perf_counter()
    # Genrate new images using threads
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(join_images, background_imgs, imgs)
    end = time.perf_counter()
    print(f'TOTAL TIME: {end -  start}')

def set_seed():
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
    set_seed()
    classes = load_classes(images_dir)
    main(images_per_class)