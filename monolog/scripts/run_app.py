# encoding: utf-8
'''
Monolog: Deep Learining Experiment Management and Monitoring Dashboard
Author: Yuya Jeremy Ong (yuyajeremyong@gmail.com)
'''
import os
import sys
import argparse

def main():
    parse = argparse.ArgumentParser(description='Monolog: Deep Learining Experiment Management and Monitoring Dashboard')
    parse.add_argument('curr_dir')

    # Obtain Current Working Directory
    curr_dir = os.getcwd()
    print('Current Directory: ' + curr_dir)
