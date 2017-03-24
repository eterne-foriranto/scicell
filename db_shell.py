#!/usr/bin/python
from os import path, environ as env
from sys import path as syp
syp.append(path.expanduser('~/lib'))
from SciDataBase import SciDataBase
import sys
data_file = env['SCIDAT']
db = SciDataBase(data_file)

class State:
    def __init__(self):
        self.psl = []

s = State()
def ud():
    sys.ps1 = '{} '.format(s.psl)
    #exec('sys.ps1 = {} '.format(s.psl))
ud()
def print_filtered(tags):
    for i in db.filter_tags(tags):
        db.print_item(db.extract(i))

def ch(data):
    if type(data) == str:
        if data in s.psl:
            s.psl.remove(data)
        else:
            s.psl.append(data)
    else:
        if set(data).issubset(set(s.psl)):
            action = 'remove'
        else:
            action = 'append'
        for tag in data:
            exec('s.psl.{}(tag)'.format(action))
    print_filtered(s.psl)
    ud()
