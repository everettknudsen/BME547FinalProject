import pytest

# from pymodm import connect
from flask import Flask, jsonify, request

from datetime import datetime
import logging

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from skimage import exposure, data

im = data.moon()
im_p_he = exposure.equalize_hist(im)

@pytest.mark.parametrize('x, expected', [
    ((im, 'moon', 'Histogram equalization'),
     (im_p_he, 'moon_he'))
])
def test_process_image(x, expected):
    # print('type of im: {}'.format(type(im)))
    # print('type of im_p_he: {}'.format(type(im_p_he)))

    from server import process_image
    ans = process_image(x[0], x[1], x[2])
    # print('type of ans0: {}'.format(type(ans[0])))
    # print('type of ans1: {}'.format(type(ans[1])))
    print(ans[1])
    # assert ans[0].all == expected[0].all
    assert ans[1] == expected[1]

# add test for email error: import error
