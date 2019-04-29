import pytest

from skimage import exposure, data
import PIL
from PIL import Image
import numpy as np
from gui import NumpytoPIL, PILtoNumpy, \
    im2str, str2im

im = data.moon()
im0 = NumpytoPIL(im)
im1 = im2str(im)


def test_NumpytoPIL_0():
    ans = NumpytoPIL(im)
    # ensure is numpy and not PIL
    assert type(im) == np.ndarray

    assert type(ans) == PIL.Image.Image


def test_NumpytoPIL_1():
    ans = NumpytoPIL(im)
    # ensure is numpy and not PIL
    assert type(im) == np.ndarray

    assert ans == im0


def test_PILtoNumpy():
    ans = PILtoNumpy(im0)
    # ensure im0 is PIL and not numpy
    assert type(im0) == PIL.Image.Image

    assert type(ans) == np.ndarray


@pytest.mark.parametrize('x, expected', [
    (im, str),
    (im0, str),
])
def test_im2str(x, expected):
    ans = im2str(x)
    assert type(ans) == expected


def test_str2im():
    ans = str2im(im1)
    # ensure im1 is string
    assert type(im1) == str

    assert type(ans) == (
           np.ndarray or PIL.Image.Image
    )
