import pytest

from skimage import exposure, data
import PIL
import numpy as np

global ans0
im = data.moon()


def test_PILtoNumpy():
    from gui import PILtoNumpy

    ans0 = PILtoNumpy(im)
    return im
    assert type(ans0) == np.ndarray


def test_NumpytoPIL():
    from gui import NumpytoPIL

    ans = NumpytoPIL(im)
    assert type(ans) == PIL.Image.Image

'''

@pytest.mark.parametrize('x, expected', [
    (None, None),
    (None, None),
])
'''
