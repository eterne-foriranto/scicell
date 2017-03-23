#!/usr/bin/python
from os import path, environ as env
from sys import path as syp
syp.append(path.expanduser('~/lib'))
from SciDataBase import SciDataBase
data_file = env['SCIDAT']
db = SciDataBase(data_file)

def print_filtered(tags):
    for i in db.filter_tags(list(tags)):
        print(i)

#cur_tags = []
#cmd = ''
#while cmd != 'exit':
#    cmd = input(cur_tags.sort())
#    try:
#        exec(cmd)
#        print('here')
#    except:
#        fcmd = 'db.{}'.format(cmd)
#        exec(fcmd)
