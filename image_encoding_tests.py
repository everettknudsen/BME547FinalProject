import base64
import io
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import sys
from PIL import Image
import numpy as np
from skimage import io as im


def encode_image_as_b64(img_NParray):
    img = Image.fromarray(img_NParray)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_bytes = buffer.getvalue()
    img_str = base64.b64encode(img_bytes).decode("utf-8")
    # print(sys.getsizeof(img_str))
    # print(img_str)
    return img_str


def decode_image_from_b64(base64_img_str):
    tp = open("tp.png", "wb")
    tp.write(base64.b64decode(base64_img_str))
    tp.close()
    decoded_img = im.imread("tp.png")
    return decoded_img  # type ndarray


if __name__ == '__main__':
    img = Image.open("C:/Users/wainw/Pictures/GroupMe/bo.jpeg")
    image_array = np.array(img)
    img_b64_string = encode_image_as_b64(image_array)
    img = decode_image_from_b64(img_b64_string)
    # print(type(img))
