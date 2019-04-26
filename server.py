#from pymodm import connect
from flask import Flask, jsonify, request
from datetime import datetime
from PIL import Image
import imghdr
import numpy as np
import logging

# global variables

app = Flask(__name__)

# connect()


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

    #for user in User.objects.raw({}):
        # view database or upload new image
    return jsonify(email)


@app.route('/api/new_image', methods=['POST'])
def post_new_image():
    """

    :return:
    """
    im = request.get_json()
    # for user in User.objects.raw({}):
        # pass
        # assign image to user database


@app.route('/api/image_list', methods=['GET'])
def get_image_list():
    """Obtains list of image titles for dropdown menu

    :return: list of images
    """
    for user in User.objects.raw({}):
        image_list = []
        pass
    return jsonify(image_list)


@app.route('/api/process', methods=['POST'])
def post_process():
    """Choose processing type

    :return:
    """
    process =



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