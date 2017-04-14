#!/usr/bin/python
from os import path, environ as env
from sys import path as syp
syp.append(path.expanduser('~/lib'))
from SciDataBase import SciDataBase
from units import *
import sys
data_file = env['SCIDAT']
db = SciDataBase(data_file)

class State:
    def __init__(self):
        self.psl = []
        self.friendly_labels = {}
        self.vanilla_iface = {
                'gt':'get',
                'sp':'split'
                }

s = State()
def ud():
    sys.ps1 = '{} '.format(s.psl)
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

def label(label, tags = s.psl):
    if '|' in tags:
        tags = db.extract(tags)
    s.friendly_labels[label] = db.safe_label(tags)

def rc(obj, tags = s.psl):
    db.record(tags, obj)
    if type(obj) == SciDataBase.Lambdump:
        db.make_c(tags)
    db.save()

def sv():
    db.save()

def form():
    txt = input('Enter the formula...\n')
    for key in s.friendly_labels.keys():
        txt = txt.replace(key, 'self.get({})'.format(s.friendly_labels[key]))
    return SciDataBase.Lambdump({}, txt)

def rm(tags):
    db.remove_cell(tags)

def ll():
    print_filtered(s.psl)

def rl():
    db = SciDataBase(data_file)

def set_decimal(tags_unique, to_set):
    a=db.filter_tags(tags_unique)
    for key in a:
	    tags = db.extract(key)
	    cell = db.find_cell(tags)
	    cell.decimal = to_set
    sv()
    
for key in s.vanilla_iface.keys():
    exec('{} = db.{}'.format(key, s.vanilla_iface[key]))
