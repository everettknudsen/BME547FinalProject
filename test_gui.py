import pytest

from skimage import exposure, data
import PIL
from PIL import Image
import numpy as np
from gui import NumpytoPIL, PILtoNumpy

im = data.moon()
im0 = NumpytoPIL(im)


def test_NumpytoPIL_0():
    """First test of numpy to PIL conversion
    tests that type of output is PIL image

    Args:

    Returns:
    """
    ans = NumpytoPIL(im)
    # ensure is numpy and not PIL
    assert type(im) == np.ndarray

    assert type(ans) == PIL.Image.Image


def test_NumpytoPIL_1():
    """Second test of numpy to PIL conversion
    tests that the image is the same before and after conversion

    Args:

    Returns:
    """
    ans = NumpytoPIL(im)
    # ensure is numpy and not PIL
    assert type(im) == np.ndarray

    assert ans == im0


def test_PILtoNumpy():
    """Test PIL to numpy conversion
    tests that type of output is numpy ndarray

    Args:

    Returns:
    """
    ans = PILtoNumpy(im0)
    # ensure im0 is PIL and not numpy
    assert type(im0) == PIL.Image.Image

    assert type(ans) == np.ndarray
