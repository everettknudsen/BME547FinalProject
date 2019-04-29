import pytest

from skimage import data
import image_encoding_tests as imEn
import numpy as np

im = data.moon()
im0 = imEn.encode_image_as_b64(im)


def test_encode_image_as_b64():
    """Tests numpy to string encoding
    """
    # ensure im is numpy
    assert type(im) == np.ndarray
    ans = imEn.encode_image_as_b64(im)

    assert type(ans) == str


def test_decode_image_from_b64_0():
    """First test for string to numpy decoding
    tests that image is the same before and after conversion
    """
    # ensure im0 is str
    assert type(im0) == str
    ans = imEn.decode_image_from_b64(im0)

    assert np.all(ans == im)


def test_decode_image_from_b64_1():
    """Second test for string to numpy decoding
    tests that type of output is numpy ndarray
    """
    # ensure im0 is str
    assert type(im0) == str
    ans = imEn.decode_image_from_b64(im0)

    assert type(ans) == np.ndarray
