from skimage import data
from gui import NumpytoPIL
from PIL import Image


def save_im_as(img, ft, fn, fp):
    ft = ft.lower()
    if ft == 'jpg' or ft == 'jpeg':
        ext = '.jpeg'
        EXT = 'JPEG'
    elif ft == 'tiff' or ft == 'tif':
        ext = '.tiff'
        EXT = 'TIFF'
    elif ft == 'png':
        ext = '.png'
        EXT = 'PNG'
    else:
        print('Not a valid file type')
        return
    img.save(fp + '/' + fn + ext, EXT)
    return


if __name__ == '__main__':
    img = data.moon()
    img = NumpytoPIL(img)

    ft = 'tif'
    fp = 'C:/Users/Kendall/repos/BME547FinalProject'
    fn = 'moon'

    save_im_as(img, ft, fn, fp)
