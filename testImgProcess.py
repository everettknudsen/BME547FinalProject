# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 19:45:01 2019

@author: nicwainwright
"""

import base64
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import sys
from PIL import Image, ImageTk
import tkinter as tk
from skimage import exposure
import os

filepath = 'C:/Users/wainw/Pictures/GroupMe/bo.jpeg'
savepath = 'C:/Users/wainw/Pictures/pass.jpg'

"""
filepath = 'C:/Users/wainw/Pictures/pass.jpg'
img1 = Image.open(filepath)
img1 = np.array(img1)
# Contrast stretching
p2, p98 = np.percentile(img1, (30, 70))
img_rescale = exposure.rescale_intensity(img1, in_range=(p2, p98))
img_rescale = exposure.rescale_intensity(img_rescale, out_range=(0, 255))
rePIL = Image.fromarray(img_rescale.astype('uint8'))
print(img_rescale.shape)

# Equalization
img_eq = exposure.equalize_hist(img1)
print(img_eq.shape)
img_eq = exposure.rescale_intensity(img_eq, out_range=(0, 255))
eqPIL = Image.fromarray(img_eq.astype('uint8'))

fig1 = plt.figure()
plt.imshow(np.asarray(rePIL))
fig2 = plt.figure()
plt.imshow(np.asarray(eqPIL))
fig3 = plt.figure()

logg = np.log(img1)
logc = exposure.rescale_intensity(logg, out_range=(0, 255))
plt.imshow(logg.astype('uint8'))
"""

print(os.path.splitext(filepath)[0])

