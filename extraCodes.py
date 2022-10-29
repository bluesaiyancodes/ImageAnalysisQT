import cv2
import os
import numpy as np
import skimage.io as io
from PIL import Image, ImageOps
from datetime import datetime
import matplotlib.pyplot as plt 

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

def genL(imagePath):
    # Read Image
    image = cv2.imread(imagePath)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    # Flatten Image
    flat_l = image[:,:,0].reshape(image.shape[0]*image.shape[1])
    # Calculate Mean and Std. Dev
    mean = round(np.mean(flat_l),3)
    std_dev = round(np.std(flat_l),3)
    # plot 
    plt.clf()
    plt.plot(flat_l, 'k', label="Lightness")
    plt.plot([], [], ' ', label="stdDev-%s"%str(std_dev))
    plt.plot([], [], ' ', label="mean-%s"%str(mean))
    plt.legend()
    savePath = os.getcwd()+"/tmp/" + "L-%s.png"%datetime.now().strftime('%H-%M-%S')
    plt.savefig(savePath)

    return savePath

def genA(imagePath):
    # Read Image
    image = cv2.imread(imagePath)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    # Flatten Image
    flat_l = image[:,:,1].reshape(image.shape[0]*image.shape[1])
    # Calculate Mean and Std. Dev
    mean = round(np.mean(flat_l),3)
    std_dev = round(np.std(flat_l),3)
    # plot 
    plt.clf()
    plt.plot(flat_l, 'r', label="A-Red/Green")
    plt.plot([], [], ' ', label="stdDev-%s"%str(std_dev))
    plt.plot([], [], ' ', label="mean-%s"%str(mean))
    plt.legend()
    savePath = os.getcwd()+"/tmp/" + "A-%s.png"%datetime.now().strftime('%H-%M-%S')
    plt.savefig(savePath)

    return savePath


def genB(imagePath):
    # Read Image
    image = cv2.imread(imagePath)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    # Flatten Image
    flat_l = image[:,:,2].reshape(image.shape[0]*image.shape[1])
    # Calculate Mean and Std. Dev
    mean = round(np.mean(flat_l),3)
    std_dev = round(np.std(flat_l),3)
    # plot 
    plt.clf()
    plt.plot(flat_l, 'b', label="B-Blue/Yellow")
    plt.plot([], [], ' ', label="stdDev-%s"%str(std_dev))
    plt.plot([], [], ' ', label="mean-%s"%str(mean))
    plt.legend()
    savePath = os.getcwd()+"/tmp/" + "B-%s.png"%datetime.now().strftime('%H-%M-%S')
    plt.savefig(savePath)

    return savePath

def pixelDist(imagePath):
    # Read Image
    image = cv2.imread(imagePath)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    
    # tuple to select colors of each channel line
    colors = ("k", "r", "b")
    channel_ids = (0, 1, 2)

    # create the histogram plot, with three lines, one for
    # each color
    plt.clf()
    plt.figure()
    plt.xlim([0, 256])
    for channel_id, c in zip(channel_ids, colors):
        histogram, bin_edges = np.histogram(
            image[:, :, channel_id], bins=256, range=(0, 256)
        )
        plt.plot(bin_edges[0:-1], histogram, color=c)

    plt.title("Visualise LAB")
    plt.xlabel("Color value")
    plt.ylabel("Pixel count")
    plt.gca().legend(('Lightness','A-Red/Green','B-Blue/Yellow'))
    savePath = os.getcwd()+"/tmp/" + "PD-%s.png"%datetime.now().strftime('%H-%M-%S')
    plt.savefig(savePath)

    return savePath

