import base64
import io
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import sys
from PIL import Image
import numpy as np
from skimage import io as im


def encode_image_as_b64(img_NParray):
    """
    A function which takes an image as a np array
    and encdes it into a base64 string which can then
    be passed to the server as a json.
    :param img_NParray: An image as a np array.
    :return img_str: A base64 encouded image string.
    """
    img = Image.fromarray(img_NParray)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_bytes = buffer.getvalue()
    img_str = base64.b64encode(img_bytes).decode("utf-8")
    return img_str


def decode_image_from_b64(base64_img_str):
    """
    This function decodes a base64 image string back into
    a PIL image usable with TKinter and GUI display.
    :param base64_img_str: A base64 string containing encouded
    image data.
    :return decoded_img: PIL image file ready to use with GUI
    or processing or download.
    """
    tp = open("tp.png", "wb")
    tp.write(base64.b64decode(base64_img_str))
    tp.close()
    decoded_img = im.imread("tp.png")
    return decoded_img


if __name__ == '__main__':
    img = Image.open("C:/Users/wainw/Pictures/GroupMe/bo.jpeg")
    image_array = np.array(img)
    img_b64_string = encode_image_as_b64(image_array)
    img = decode_image_from_b64(img_b64_string)
