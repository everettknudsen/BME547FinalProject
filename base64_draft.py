import base64
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import pickle


def im2str(img):
    img = np.array(img)
    img = pickle.dumps(img)
    img = base64.b64encode(img)
    img = str(img, 'utf-8')
    return img


def str2im(img):
    img = base64.b64decode(img)
    img = pickle.loads(img)
    return img


if __name__ == '__main__':
    filepath = 'C:/Users/Kendall/Pictures/Proteinogenic Amino Acids.png'
    img0 = Image.open(filepath)

    img0 = im2str(img0)
    img0 = str2im(img0)
    figure1 = plt.figure()
    plt.interactive(True)
    plt.imshow(img0)
    plt.show()
