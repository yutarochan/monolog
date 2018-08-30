# encoding: utf-8
'''
Monolog: Deep Learining Experiment Management and Monitoring Dashboard
Author: Yuya Jeremy Ong (yuyajeremyong@gmail.com)
'''
import os
from flask import request, jsonify, send_from_directory, g

from monolog import app

@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def home(path):
    return send_from_directory(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'static/',
            os.path.split(path)[0]
        ),
        os.path.split(path)[1]
    )
