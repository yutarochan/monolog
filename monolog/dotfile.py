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

def make_dotfile(dir):
    if not os.path.exists(dir + '/.monolog'):
        os.makedirs(dir + '/.monolog')

def check_dot(dir):
    return check_root(dir) and check_config(dir)

def make_config(dir, name, desc):
    out = open(dir + '/.monolog/config', 'w')
    out.write('[core]\n')
    out.write('name=' + name + '\n')
    out.write('desc="' + desc.replace("\r\n", "\\n") + '"\n')
    out.close()
