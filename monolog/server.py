# encoding: utf-8
'''
Monolog: Deep Learining Experiment Management and Monitoring Dashboard
Author: Yuya Jeremy Ong (yuyajeremyong@gmail.com)
'''
from __future__ import absolute_import, print_function, division, unicode_literals
from gevent.wsgi import WSGIServer
import webbrowser

def launch(app):
    '''
    http_server = WSGIServer(('', app.config['PORT']), app)
    webbrowser.open_new('http://localhost:' + str(app.config['PORT']))
    http_server.serve_forever()
    '''

    # Temp Execution
    port = 8080 if len(sys.argv) < 2 else sys.argv[1]
    app.run(debug=True, port=int(port), host='0.0.0.0')
