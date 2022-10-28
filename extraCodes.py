import cv2
import os
import numpy as np
import skimage.io as io
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
