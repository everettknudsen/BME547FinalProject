# from pymodm import connect
from flask import Flask, jsonify, request
from PIL import Image
from datetime import datetime
import logging

import base64
import pickle
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import mongo_database as mdb


app = Flask(__name__)
mdb.global_init()  # connect to mongoDB

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
        email
    """
    email = request.get_json()
    is_email(email)

    is_user = mdb.check_if_user_registered(email)

    if is_user:
        message = 'user exists'
    else:
        message = mdb.add_new_user(email)
        logging.info('New user added: {}'.format(email))

    # return jsonify(r)
    print(message)
    return message


@app.route('/api/logConfirm', methods=['POST'])
def post_logConfirm():
    """Queries user if email exists or
    creates new database for new user

    Args:

    Returns:
        email
    """
    mdb.print_users()
    return 'tried to print'


@app.route('/api/<email>/post_new_image', methods=['POST'])
def post_new_image(email):
    """Uploads normal image

    Args:
        email (str): user email (primary key)

    Returns:
    """
    print("submitting image to " + email)
    upload_package = request.get_json()
    message = mdb.new_image_added(email, upload_package)

    print(message)
    return message


@app.route('/api/<email>/post_new_image_pro', methods=['POST'])
def post_new_image_pro(email):
    """Uploads processed image with latency

    Args:
        email (str): user email (primary key)

    Returns:
    """
    print("submitting image to " + email)
    upload_package_processed = request.get_json()
    message = mdb.new_image_added_pro(email, upload_package_processed)

    print(message)
    return message


@app.route('/api/<email>/get_image_list', methods=['GET'])
def get_image_list(email):
    """Obtains list of non-processed image titles from database
    for use in dropdown menu

    Args:
        email (str): user email (primary key)

    Returns:
        image_list (list): list of unprocessed image  titles
    """
    # for user in User.objects.raw({}):
    # image_dict = database['name']
    mongo_image_list = mdb.normal_images(email)
    return jsonify(mongo_image_list)


@app.route('/api/<email>/get_image_list_pro_<image_name>', methods=['GET'])
def get_image_list_pro(email, image_name):
    """Obtains list of processed image titles from database based on non-
    processed image name for use in compare dropdown menu

    Args:
        email (str): user email (primary key)
        image_name (str): image name for which to load processed versions for

    Returns:
        image_list (list): list of unprocessed image  titles
    """
    # for user in User.objects.raw({}):
    # image_dict = database['name']
    mongo_image_list_pro = mdb.processed_images(email, image_name)
    return jsonify(mongo_image_list_pro)


def pull_image_list(image_dict):
    """MongoDB image dict for one user

    Args:
        image_dict (dict): dictionary of user images

    Returns:
        image_list (list): list of unprocessed image  titles
    """
    image_list = []
    return image_list


@app.route('/api/<email>/<img_name>/get_image', methods=['GET'])
def get_image(email, img_name):
    """Pulls up image data when chosen from dropdown menu

    Args:
        user (str): user email (primary key)
        img_name (str): name of desired image

    Returns:
        img_data (str): encoded image
    """
    img_data = mdb.download_normal_img(email, img_name)
    return jsonify(img_data)


@app.route('/api/<email>/<img_name>/get_image_pro_<processType>',
           methods=['GET'])
def get_image_pro(email, img_name, processType):
    """Pulls up image data when chosen from dropdown menu

    Args:
        user (str): user email (primary key)
        img_name (str): name of desired image
        processType (str): process type of image to load

    Returns:
        img_data (str): encoded processed image
    """
    img_data = mdb.download_processed_img(email, img_name, processType)
    return jsonify(img_data)


@app.route('/api/<email>/<img_name>/get_time', methods=['GET'])
def get_time(email, img_name):
    """Pulls up timestamp when image chosen from dropdown menu

    Args:
        user (str): user email (primary key)
        img_name (str): name of desired image

    Returns:
        timestamp (datetime.datetime): datetime object of time when photo was
        uploaded
    """
    time = mdb.get_time(email, img_name)
    return jsonify(time)


@app.route('/api/<email>/<img_name>/get_time_pro_<processType>',
           methods=['GET'])
def get_time_pro(email, img_name, processType):
    """Pulls up timestamp when process chosen from dropdown menu

    Args:
        user (str): user email (primary key)
        img_name (str): name of desired image
        processType (str): process of image to load

    Returns:
        timestamp (datetime.datetime): datetime object of time when photo was
        uploaded
    """
    time = mdb.get_time_pro(email, img_name, processType)
    return jsonify(time)


@app.route('/api/<email>/<img_name>/get_latency_<processType>',
           methods=['GET'])
def get_latency(email, img_name, processType):
    """Pulls up latency of img after chosen

    Args:
        user (str): user email (primary key)
        img_name (str): name of desired image
        processType (str): process type of image to load

    Returns:
        latency (float): latency value
    """
    latency = mdb.get_latency(email, img_name, processType)
    return jsonify(latency)


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


@app.route('/api/<email>/<process>/get_process_type', methods=['GET'])
def get_process_count(email, process):
    count = calc_process_count(email, process)
    return jsonify(count)


def calc_process_count(email, process):
    """Determines how many times a user has applied a certain process

    Args:
        email (str): user email (primary key)
        process (str): desired processing types

    Returns:
        count (int): number of times
    """
    # check database
    # search for tag in string
    # counts length of 'time' list for each '*_process' image
    count = []
    return count


@app.route('/api/<email>/get_all_user_metrics', methods=['GET'])
def get_all_user_metrics(user):
    all_metrics = pull_all_metrics(user)
    return jsonify(all_metrics)


def pull_all_metrics(email):
    """Obtains list of timestamps/corresponding
    processes for a user

    Args:
        email (str): user email (primary key)

    Returns:
        all_metrics
    """
    # check database
    # print list of timestamps/actions
    all_metrics = []
    return all_metrics


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
            logging.warning('Invalid email entered: {}'.format(x))
            raise NotEmail(message_400, status_code=400)
    else:
        message_400 = 'Please enter a valid email address.'
        logging.warning('Invalid email entered: {}'.format(x))
        raise NotEmail(message_400, status_code=400)


if __name__ == '__main__':
    logging.basicConfig(filename='image_processor.log', level=logging.INFO)
    # app.run()
    app.run(host='0.0.0.0')
