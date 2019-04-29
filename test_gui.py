import pytest

from skimage import exposure, data
import PIL
from PIL import Image
import numpy as np
from gui import NumpytoPIL, PILtoNumpy

im = data.moon()
im0 = NumpytoPIL(im)


def test_NumpytoPIL_0():
    """First test for numpy to PIL conversion
    tests that type of output is PIL image
    """
    # ensure is numpy and not PIL
    assert type(im) == np.ndarray
    ans = NumpytoPIL(im)

    assert type(ans) == PIL.Image.Image


def test_NumpytoPIL_1():
    """Second test for numpy to PIL conversion
    tests that the image is the same before and after conversion
    """
    # ensure im is numpy and not PIL
    assert type(im) == np.ndarray

    ans = NumpytoPIL(im)
    assert ans == im0


def test_PILtoNumpy():
    """Test for PIL to numpy conversion
    tests that type of output is numpy ndarray
    """
    # ensure im0 is PIL and not numpy
    assert type(im0) == PIL.Image.Image
    ans = PILtoNumpy(im0)

    assert type(ans) == np.ndarray
