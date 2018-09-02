# encoding: utf-8
'''
Monolog: Deep Learining Experiment Management and Monitoring Dashboard
Author: Yuya Jeremy Ong (yuyajeremyong@gmail.com)
'''
import os
from flask import request, jsonify, send_from_directory, g, render_template

from monolog import app, dotfile

@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def home(path):
    # Redirect for Default Index Page
    if path == 'index.html': return dashboard()
    return send_from_directory(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'static/',
            os.path.split(path)[0]
        ),
        os.path.split(path)[1]
    )

def dashboard():
    # Check for .monolog dot file (redirect to setup wizard if non-existant)
    if not dotfile.check_root(os.getcwd()):
        print('DOT FILE DOES NOT EXIST - REDIRECTING TO SETUP WIZARD')
        return setup()

    return render_template('dashboard.html', page='dashboard')


@app.route('/setup')
def setup():
    return render_template('setup.html', page='experiments')

@app.route('/experiments')
def experiments():
    return 'EXPERIMENTS'

@app.route('/hypertune')
def hypertune():
    return 'Experiments Page'
