from gui import PILtoNumpy, NumpytoPIL
import numpy as np
from PIL import Image, ImageTk
from skimage import exposure


def logCompression(pilImg):
    c = 255 / (np.log10(1 + np.amax(pilImg)))
    for all_pixels in np.nditer(pilImg, op_flags=['readwrite']):
        all_pixels[...] = c * np.log10(1 + all_pixels)
    return NumpytoPIL(pilImg)


def reverseVideo(pilImg):
    for all_pixels in np.nditer(pilImg, op_flags=['readwrite']):
        all_pixels[...] = 255 - all_pixels
    return NumpytoPIL(pilImg)
