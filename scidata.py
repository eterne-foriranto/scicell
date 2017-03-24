#!/usr/bin/python
from os import path
from sys import path as syp
syp.append(path.expanduser('~/lib'))
import pickle

class SciDataBase:
    def __init__(self, file_):
        self.file_ = file_
        self.f = None
        if path.exists(file_):
            with open(file_, 'rb') as f:
                self.__base = pickle.load(f)
        else:
            self.__base = {
                    'data':{},
                    'scripts':[]
                    }

    class Script:
        def __init__(self, description, file_):
            self.description = description
            with open(file_, 'r') as f:
                self.body = f.read()

    class Matrix:
        def __init__(self, data):
            self.data = data

        def filter_tag(self, tag):
            rest = []
            for line in self.data:
                if  '|' + tag + '|' in line:
                    rest.append(line)
            return self.__class__(rest)

    class Cell:
        def __init__(self, value):
            self.value = value
            self.simple = True
            self.label = None
            self.visible = True
            self.decimal = None
            self.extra = None

        def __repr__(self):
            if self.simple:
                return str(self.value)
            else:
                pass

    class Lambdump:
        def __init__(self, context, data):
            self.context = context
            self.text = data

    def wrap(self, smth):
        return '|' + smth + '|'

    def record(self, tags, value):
        print('recording...')
        tags.sort()
        key = '|' + '|'.join(tags) + '|'
        print(key in self.__base['data'].keys())
        if key in self.__base['data'].keys():
            self.__base['data'][key].value = value
        else:
            print('new')
            self.__base['data'][key] = self.Cell(value)

    def filter_tags(self, tags):
        matrix = self.Matrix([key for key in self.__base['data'].keys()])
        for tag in tags:
            matrix = matrix.filter_tag(tag)
        return matrix.data

    def make_c(self, data):
        cell = self.find_cell(data)
        cell.simple = False

    def add_script(self, description, file_):
        self.__base['scripts'].append(self.Script(description, file_))

    def get(self, data):
        cell = self.find_cell(data)
        if cell == None:
            print('cell not found')
            return None
        if cell.simple:
            return cell.value
        else:
            context = cell.value.context
            context['self'] = self
            exec('self.f = lambda: ' + cell.value.text, context)
            return self.f()

    def save(self):
        self.f = None
        with open(self.file_, 'wb') as f:
            pickle.dump(self.__base, f, 2)

    def hide_tag(self, tag):
        base = self.__base['data']
        for cell in [base[key] for key in base.keys() if self.wrap(tag) in key]:
            cell.visible = False

    def list_tags(self):
        return self.__base['data'].tags

    def print_item(self, tags):
        cell = self.find_cell(tags)
        value = self.get(tags)
        key = self.tags2key(tags)
        if cell.simple:
            x = ''
        else:
            x = '*'
        print('{}:{} {}{}'.format(key, value, cell.label, x))

    def show_table(self):
        for item in self.__base['data'].items():
            print(item, item[1].label)

    def find_cell(self, cell):
        try:
            if type(cell) == list:
                return self.__base['data'][self.tags2key(cell)]
            else:
                for value in self.__base['data'].values():
                    if value.label == cell:
                        return value
        except:
            return None

    def tags2key(self, tags):
        if type(tags) == str:
            return '|{}|'.format(tags)
        new = tags[:]
        new.sort()
        new = '|'.join(new)
        key = self.wrap(new)
        return key

    def safe_label(self, data):
        cell = self.find_cell(data)
        if cell.label != None:
            return cell.label
        else:
            label = 0
            while label in [cell.label for cell in self.__base['data'].values()]:
                label += 1
            cell.label = label
            return label

    def remove_script(self, num):
        del(self.__base['scripts'][num])

    def run_script(self, num):
        exec(self.__base['scripts'][num].body)

    def extract(self, key):
        return key[1:len(key) - 1].split('|')

    def split(self, olds, news):
        def complete(tags):
            tags = set(tags)
            if type(news) == list:
                for new in news:
                    tags.add(new)
            else:
                tags.add(news)
            tags = list(tags)
            return tags
        for key in self.__base['data'].keys():
            tags = self.extract(key)
            if type(olds) == list:
                if set(olds).issubset(set(tags)):
                    for old in olds:
                        tags.remove(old)
                    tags = complete(tags)
            elif olds in tags:
                tags.remove(olds)
                tags = complete(tags)
            cell = self.__base['data'][key]
            del(self.__base['data'][key])
            tags.sort()
            self.__base['data'][self.wrap('|'.join(tags))] = cell

    def remove_tag(self, tag):
        pass

    def remove_cell(self, tags):
        del(self.__base['data'][self.tags2key(tags)])
