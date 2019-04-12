import numpy as np
from flask import Flask, jsonify, request
from datetime import datetime
from collections import OrderedDict as Od
import logging

app = Flask(__name__)


@app.route('/', methods=['GET'])
def server_on():
    return 'Image processing server is on'