# encoding: utf-8
'''
Monolog: Deep Learining Experiment Management and Monitoring Dashboard
Author: Yuya Jeremy Ong (yuyajeremyong@gmail.com)
'''
import os
import configparser

import monolog.util as util

def check_root(dir):
    return os.path.isdir(dir + '/.monolog')

def check_config(dir):
    return os.path.isfile(dir + '/.monolog/config.yaml')

def make_dotfile(dir):
    if not os.path.exists(dir + '/.monolog'):
        os.makedirs(dir + '/.monolog')        # Main Directory
        os.makedirs(dir + '/.monolog/views')  # View Configuration
        os.makedirs(dir + '/logs')            # View Configuration

def check_dot(dir):
    return check_root(dir) and check_config(dir)

def make_config(dir, name, desc):
    out = open(dir + '/.monolog/config.yaml', 'w')
    out.write('[core]\n')
    out.write('name=' + name + '\n')
    out.write('desc="' + desc.replace("\r\n", "\\n") + '"\n')
    out.close()

def read_config(dir):
    config = configparser.ConfigParser()
    config.read(dir + '/.monolog/config.yaml')

    config_dict = {}

    # Set Parameter to Argument Attributes
    for k, v in config.items('core'):
        # Automatic Type Casting
        if util.is_int(v): v = int(v)
        elif util.is_float(v): v = float(v)

        config_dict[k] = v

    return config_dict
