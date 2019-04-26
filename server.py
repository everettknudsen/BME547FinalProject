import numpy as np
from flask import Flask, jsonify, request
from datetime import datetime
from pymodm import connect
import logging

# global variables
email = []

app = Flask(__name__)

connect()

@app.route('/', methods=['GET'])
def server_on():
    return 'Image processing server is on'


@app.route('/api/login', methods=['POST'])
def post_login():
    """Queries user if email exists or
    creates new database for new user

    :return:
    """
    # user = email from GUI
    for user in User.objects.raw({}):
        pass
        # view database or upload new image


@app.route('/api/new_image', methods=['POST'])
def post_new_image():
    """

    :return:
    """
    for user in User.objects.raw({}):
        pass
        # determine processing type
