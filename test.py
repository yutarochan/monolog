'''
Monolog: Deep Learining Experiment Management and Monitoring Dashboard
Author: Yuya Jeremy Ong (yuyajeremyong@gmail.com)
'''
from __future__ import absolute_import, print_function, division, unicode_literals
import os
import sys
from monolog import app

if __name__ == '__main__':
    port = 8080 if len(sys.argv) < 2 else sys.argv[1]
    app.run(debug=True, port=int(port), host='0.0.0.0')
