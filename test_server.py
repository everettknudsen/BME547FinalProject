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


# test PIL, numpy type

# add test for email error: import error
