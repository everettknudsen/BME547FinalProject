# from pymodm import connect
from flask import Flask, jsonify, request

from datetime import datetime
import logging

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from skimage import exposure

# global variables
im =[]

app = Flask(__name__)

# connect() to database


@app.route('/', methods=['GET'])
def server_on():
    return 'Image processing server is on'


@app.route('/api/login', methods=['POST'])
def post_login():
    """Queries user if email exists or
    creates new database for new user

    :return:
    """
    email = request.get_json()
    is_email(email)

    # for user in User.objects.raw({}):
    # view database or upload new image
    return jsonify(email)


@app.route('/api/new_image', methods=['POST'])
def post_new_image():
    """

    :return:
    """
    im = request.get_json()
    # decode image

    # for user in User.objects.raw({}):
    # assign image to user database
    # return jsonify(im)


@app.route('/api/image_list', methods=['GET'])
def get_image_list():
    """Obtains list of image titles from database
    for use in dropdown menu

    :return: list of images
    """
    # for user in User.objects.raw({}):
    image_list = []
    return jsonify(image_list)


@app.route('/api/choose_method', methods=['POST'])
def post_choose_method():
    """Choose processing type

    :return:
    """
    im, im_name, method = request.get_json()
    im_p, im_name_p = process_image(
        im_name, im,
        method='Histogram equalization'
    )
    return jsonify(im_p)


def process_image(im, im_name, method):
    """Processes image according to chosen method

    :param im_name: title of image to be processed
    :param im: image to be processed
    :param method: desired method of image processing
    :return:
    """
    if method is 'Contrast stretching':
        tag = 'cs'
        p2, p98 = np.percentile(im, (2, 98))
        im_p = exposure.rescale_intensity(im)
    elif method is 'Log compression':
        tag = 'lc'
        im_p = []
    elif method is 'Reverse video':
        tag = 'rv'
        im_p = []
    else:
        tag = 'he'
        im_p = exposure.equalize_hist(im)
    im_name_p = im_name + '_' + tag # image name tagged with processing method
    return im_p, im_name_p


class NotEmail(Exception):
    # adapted from http://flask.pocoo.org/docs/1.0
    # patterns/apierrors/
    status_code = 400

    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        if status_code is not None:
            self.status_code = status_code
        self.message = message

    def to_dict(self):
        rv = dict()
        rv['message'] = self.message
        return rv


@app.errorhandler(NotEmail)
def handle_not_email(error):
    resp = jsonify(error.to_dict())
    resp.status_code = error.status_code
    return resp


def is_email(x):
    """Tests if input is an email

        :param x: user email
        :return:
        """
    if '@' in x:
        x = x.split('@')
        if len(x) == 2 and '.' in x[1]:
            pass
        else:
            message_400 = 'Please enter a valid email address.'
            raise NotEmail(message_400, status_code=400)
    else:
        message_400 = 'Please enter a valid email address.'
        raise NotEmail(message_400, status_code=400)


if __name__ == '__main__':
    app.run()
