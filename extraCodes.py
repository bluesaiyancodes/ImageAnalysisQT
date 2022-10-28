import cv2
import os
import numpy as np
import skimage.io as io
from PIL import Image as im
from PIL import Image, ImageOps
from datetime import datetime

def cropImage(imagePath, x, y, h, w):
    img = cv2.imread(imagePath)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    croppedImg = img[y:y+h, x:x+w]
    #croppedImg = croppedImg / 255.
    croppedImg = croppedImg.astype(np.uint8)
    savePath = os.getcwd()+"/tmp/" + "%s.png"%datetime.now().strftime('%H-%M-%S')
    io.imsave(os.path.join(savePath), croppedImg)
    return savePath

def resizeImage(imagePath, size=(28,28)):

    img = cv2.imread(imagePath)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    h, w = img.shape[:2]
    c = img.shape[2] if len(img.shape)>2 else 1

    if h == w: 
        return cv2.resize(img, size, cv2.INTER_AREA)

    dif = h if h > w else w

    interpolation = cv2.INTER_AREA if dif > (size[0]+size[1])//2 else cv2.INTER_CUBIC

    x_pos = (dif - w)//2
    y_pos = (dif - h)//2

    if len(img.shape) == 2:
        mask = np.zeros((dif, dif), dtype=img.dtype)
        mask[y_pos:y_pos+h, x_pos:x_pos+w] = img[:h, :w]
    else:
        mask = np.zeros((dif, dif, c), dtype=img.dtype)
        mask[y_pos:y_pos+h, x_pos:x_pos+w, :] = img[:h, :w, :]

    imgC =  cv2.resize(mask, size, interpolation)
    imgC = imgC.astype(np.uint8)

    data = im.fromarray(imgC)

    savePath = os.getcwd()+"/tmp/" + "%s.jpg"%datetime.now().strftime('%H-%M-%S')
    data.save(savePath)
    return savePath


def padding(img, expected_size):
    desired_size = expected_size
    delta_width = desired_size - img.size[0]
    delta_height = desired_size - img.size[1]
    pad_width = delta_width // 2
    pad_height = delta_height // 2
    padding = (pad_width, pad_height, delta_width - pad_width, delta_height - pad_height)
    return ImageOps.expand(img, padding)


def resize_with_padding(imagePath, expected_size):

    img = Image.open(imagePath)


    img.thumbnail((expected_size[0], expected_size[1]))
    # print(img.size)
    delta_width = expected_size[0] - img.size[0]
    delta_height = expected_size[1] - img.size[1]
    pad_width = delta_width // 2
    pad_height = delta_height // 2
    padding = (pad_width, pad_height, delta_width - pad_width, delta_height - pad_height)
    resizedImg = ImageOps.expand(img, padding)

    savePath = os.getcwd()+"/tmp/" + "ScaledImage-%s.png"%datetime.now().strftime('%H-%M-%S')
    resizedImg.save(savePath)
    return savePath


def genLAB(imagePath):
    image = cv2.imread(imagePath)
    image = image.astype("float32")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    image = image.astype(np.uint8)

    savePath = os.getcwd()+"/tmp/" + "lab_%s.png"%datetime.now().strftime('%H-%M-%S')
    io.imsave(os.path.join(savePath), image)
    return savePath