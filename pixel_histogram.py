import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from skimage import exposure


def histogram(pilImg):
    """
    This function takes a PIL image and returns
    the histogram of the original PIL image as a new
    PIL image which can be displayed on the GUI.
    :param pilImg: PIL image data from the original or
    processed image, whichever is being displayed.
    :return: Histogram of desired image as a PIL image.
    """
    npImg = np.array(pilImg)
    hist, hist_centers = exposure.histogram(npImg)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(hist_centers, hist)
    ax.set_title('Histogram of Image')
    plt.savefig('temp.png')
    return Image.open('temp.png')


if __name__ == "__main__":
    filename = 'IMG_3979.jpg'
    pilImg = Image.open(filename)
    pilHist = histogram(pilImg)
    pilHist.show()
