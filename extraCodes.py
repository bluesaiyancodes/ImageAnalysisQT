import cv2
import os
import numpy as np
import skimage.io as io
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