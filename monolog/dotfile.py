# encoding: utf-8
'''
Monolog: Deep Learining Experiment Management and Monitoring Dashboard
Author: Yuya Jeremy Ong (yuyajeremyong@gmail.com)
'''
import os

def check_root(dir):
    return os.path.isdir(dir + '/.monolog')

def check_config(dir):
    return os.path.isfile(dir + '/.monolog/config')

def check_dotfile(dir):
    return check_root(dir) and check_config(dir)

def make_dotfile(dir):
    if not os.path.exists(dir + '/.monolog'):
        print('> MADE NEW DOTFOLDER')
        os.makedirs(dir + '/.monolog')
