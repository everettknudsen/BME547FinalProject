import cv2
import numpy as np
from PIL import Image
import io
from skimage import io as im
from matplotlib import pyplot as plt
from skimage import exposure
from gui import NumpytoPIL, PILtoNumpy


def pixel_histogram_RBG(filename):
    img = cv2.imread(filename)
    color = ('b', 'g', 'r')
    for i, col in enumerate(color):
        histr = cv2.calcHist([img], [i], None, [256], [0, 256])
        plt.plot(histr, color=col)
        plt.xlim([0, 256])
    plt.show()


def pixel_histogram_reg(filename):
    img = cv2.imread(filename, 0)
    print(type(img))
    print(type(img.ravel()))
    plt.figure(1)
    plt.subplot(111)
    plt.hist(img.ravel(), 256, [0, 256]);
    plt.show()


def histogram(pilImg):
    npImg = np.array(pilImg)
    return NumpytoPIL(exposure.histogram(npImg))


if __name__ == "__main__":
    filename = 'new-img.jpg'
    pilImg = Image.open(filename)
    hist = histogram(pilImg)
    im.show(hist)
