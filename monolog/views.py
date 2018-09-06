# encoding: utf-8
'''
Monolog: Deep Learining Experiment Management and Monitoring Dashboard
Author: Yuya Jeremy Ong (yuyajeremyong@gmail.com)
'''
import os
from flask import request, jsonify, send_from_directory, g, render_template, redirect

from monolog import app, dotfile

def check_dot():
    # Check for .monolog dot file (redirect to setup wizard if non-existant)
    if not dotfile.check_dot(os.getcwd()):
        dotfile.make_dotfile(os.getcwd())   # Generate Monolog Dotfolder
        return True
    return False

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
    if check_dot(): return redirect('/setup')           # Redirect to Setup Page

    app = dotfile.read_config(os.getcwd())

    return render_template('dashboard.html', page='dashboard', app=app)

@app.route('/setup')
def setup():
    return render_template('setup.html', page='setup')

@app.route('/setup_submit', methods=['POST', 'GET'])
def setup_submit():
    if request.method == 'POST':
        dotfile.make_config(os.getcwd(), request.form['project_name'], request.form['project_desc'])
        return redirect("/")

@app.route('/experiments')
def experiments():
    if check_dot(): return redirect('/setup')           # Redirect to Setup Page
    return 'EXPERIMENTS'

@app.route('/hypertune')
def hypertune():
    if check_dot(): return redirect('/setup')           # Redirect to Setup Page
    return 'Experiments Page'
