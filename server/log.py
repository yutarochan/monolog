'''
monoglog - Log File Manager
Author: Yuya Jeremy Ong (yuyajeremyong@gmail.com)
'''
from __future__ import print_function
import os
import json

def get_explist(dir):
    models = os.listdir(dir)

    model_list = []
    for m in models:
        for x in os.listdir(dir + '/' + m):
            meta = parse_metaexp(dir+'/'+m+'/'+ x)
            model_list.append((m, x, meta['created_at'], meta['exp_hash']))
    return model_list

def parse_metaexp(dir):
    data = json.loads(open(dir + '/meta.experiment', 'r').read())
    return data
