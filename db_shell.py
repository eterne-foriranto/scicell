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

def app(data):
    if type(data) == str:
        s.psl.append(data)
    else:
        for tag in data:
            s.psl.append(tag)
    print_filtered(s.psl)
    ud()
