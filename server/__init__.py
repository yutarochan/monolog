# encoding: utf-8
'''
Monolog: Deep Learining Experiment Management and Monitoring Dashboard
Author: Yuya Jeremy Ong (yuyajeremyong@gmail.com)
'''
from __future__ import absolute_import, print_function, division, unicode_literals
from flask import Flask

__version__ = '0.0.1'

app = Flask(__name__, static_url_path='/static', static_folder='/static/')
# app.config.from_object('monolog.config')

import server.views
