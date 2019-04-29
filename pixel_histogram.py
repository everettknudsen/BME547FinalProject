import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import cv2


def hist2(pilImg):
    pil_image = pilImg.convert('RGB')
    open_cv_image = np.array(pil_image)
    # Convert RGB to BGR
    img = open_cv_image[:, :, ::-1].copy()
    color = ('b', 'g', 'r')
    fig = plt.figure(frameon=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    for i, col in enumerate(color):
        histr = cv2.calcHist([img], [i], None, [256], [0, 256])
        plt.plot(histr, color=col)
        plt.xlim([0, 256])
    fig.show()
    canvas = plt.get_current_fig_manager().canvas
    canvas.draw()
    pil_image = Image.frombytes('RGB', canvas.get_width_height(),
                                canvas.tostring_rgb())
    pil_image.save('temp.png', 'PNG')
    plt.close()
    return pil_image
