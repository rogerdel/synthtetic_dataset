import glob
import random
import os

def move(file, newDir):
    anotationFile = file.split('.')[0]+".txt"
    name =  file.split('\\')[-1]
    anotation = anotationFile.split('\\')[-1]
    os.rename(file, f'{newDir}/{name}')
    os.rename(anotationFile, f'{newDir}/{anotation}')


def balance(dir):
    traindir = f'{dir}/obj'
    testdir = f'{dir}/test' 
    jpgFiles = glob.glob(f'{dir}/*.jpg')
    trainSplit = int(len(jpgFiles) * 0.8)
    random.shuffle(jpgFiles)
    train = jpgFiles[:trainSplit] 
    test = jpgFiles[trainSplit:]

    if not os.path.exists(traindir):
        os.mkdir(traindir)
    if not os.path.exists(testdir):
        os.mkdir(testdir)
    for i in train:
        move(i, traindir)
    for i in test:
        move(i, testdir)
if __name__ == '__main__':
    dir = 'dataset'
    balance(dir)