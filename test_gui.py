import pytest

from skimage import data
import PIL
from PIL import Image
import numpy as np
from skimage import exposure


def PILtoNumpy(pilImg):
    """Helper function to convert a PIL image format to numpy.ndarray for
    processing.

    Args:
        pilImg (PIL Image format image): the image to be converted
    """
    return np.array(pilImg)


def NumpytoPIL(npImg):
    """Helper function to convert numpy.ndarray formatted image to PIL format
    for processing.

    Args:
        npImg (numpy.ndarray): the image to be converted
    """
    rescale_out = exposure.rescale_intensity(npImg, out_range=(0, 255))
    return Image.fromarray(rescale_out.astype('uint8'))


def test_NumpytoPIL_0():
    """First test for numpy to PIL conversion
    tests that type of output is PIL image
    """
    # ensure is numpy and not PIL
    assert type(im) == np.ndarray
    ans = NumpytoPIL(im)

    assert type(ans) == PIL.Image.Image


im = data.moon()
im0 = NumpytoPIL(im)


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


def test_is_email():
    """Test is_email with inputs expected to raise custom
    NotEmail error
    """
    from server import is_email, NotEmail

    with pytest.raises(NotEmail):
        is_email('is.this.an.email')

    with pytest.raises(NotEmail):
        is_email('how@about@this')

    with pytest.raises(NotEmail):
        is_email('or.maybe@this')


def run_test_is_email(self):
    """Test is_email using valid input
    """
    from server import is_email, NotEmail
    try:
        is_email('this.is.good@email.com')
    except NotEmail:
        self.fail('is_email raised an unexpected error.')
