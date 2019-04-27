# from pymodm import connect
from flask import Flask, jsonify, request

from datetime import datetime
import logging

import numpy as np
import matplotlib
import matplotlib.pyplot as plt


# global variables
im = []

app = Flask(__name__)


# connect() to database


@app.route('/', methods=['GET'])
def server_on():
    return 'Image processing server is on'


@app.route('/api/login', methods=['POST'])
def post_login():
    """Queries user if email exists or
    creates new database for new user

    Args:

    Returns:
    """
    email = request.get_json()
    is_email(email)

    # for user in User.objects.raw({}):
    # view database or upload new image
    return jsonify(email)


@app.route('/api/<user>/post_new_image', methods=['POST'])
def post_new_image(user):
    """Uploads new image to database

    Args:
        user (str): user email (primary key)

    Returns:
    """
    user = []
    img = request.get_json()
    # decode image

    # for user in User.objects.raw({}):
    # assign image to user database
    # return jsonify(img)


@app.route('/api/<user>/get_image_list', methods=['GET'])
def get_image_list(user):
    """Obtains list of non-processed image titles from database
    for use in dropdown menu

    Args:
        user (str): user email (primary key)

    Returns:
        image_list (list): list of unprocessed image  titles
    """
    # for user in User.objects.raw({}):
    # image_dict = database['name']
    image_list = pull_image_list(image_dict)
    return jsonify(image_list)


def pull_image_list(image_dict):
    """MongoDB image dict for one user

    Args:
        image_dict (dict): dictionary of user images

    Returns:
        image_list (list): list of unprocessed image  titles
    """
    image_list = []
    return image_list


@app.route('/api/<user>/<img_name>/get_image', methods=['GET'])
def get_image(user, img_name):
    """Pulls up image name and data when chosen from dropdown menu

    Args:
        user (str): user email (primary key)
        img_name (str): name of desired image

    Returns:
    """
    img_data, metrics = pull_image(user, img_name)
    return jsonify(img_name, img_data, metrics)


def pull_image(img_name):
    """Obtains info for one image from database

    Args:
        img_name (str): name of desired image

    Returns:
        img_data
        metrics
    """
    # check database
    # counts length of 'time' list for each '*_process' image
    img_data = []
    metrics = []
    return img_data, metrics


@app.route('/api/<user>/<process>/get_process_type', methods=['GET'])
def get_process_count(user, process):
    count = process_count(user, process)
    return jsonify(count)


def process_count(user, process):
    """Determines how many times a user has applied a certain process

    Args:
        user (str): user email (primary key)
        process (str): desired processing types

    Returns:
        count (int): number of times
    """
    # check database
    # search for tag in string
    # counts length of 'time' list for each '*_process' image
    count = []
    return count


@app.route('/api/get_all_user_metrics/<user>', methods=['GET'])
def get_all_user_metrics(user):
    metrics = all_user_metrics(user)
    return jsonify(metrics)


def all_user_metrics(user):
    # check database
    # print list of timestamps/actions
    return metrics


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
