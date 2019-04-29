import pytest

from skimage import exposure, data
import PIL
import numpy as np
from gui import PILtoNumpy, NumpytoPIL

im = data.moon()
im0 = PILtoNumpy(im)

def test_PILtoNumpy():
    ans = PILtoNumpy(im)
    assert type(ans) == np.ndarray


def test_NumpytoPIL():
    ans = NumpytoPIL(im0)

    # ensure im0 is numpy and not PIL
    assert type(im0) == np.ndarray
    assert type(ans) == PIL.Image.Image


'''
@pytest.mark.parametrize('x, expected', [
    (None, None),
    (None, None),
])
'''
