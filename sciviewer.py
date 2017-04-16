#!/usr/bin/python
from os import path
from sys import path as syp
syp.append(path.expanduser('~/lib'))
from SciDataBase import SciDataBase as SDB

def iround(num, decim_places):
    stringed_num = str(num)
    critical_position = stringed_num.index('.') + decim_places + 1
    to_round = stringed_num
    if critical_position < len(stringed_num):
        if stringed_num[critical_position] == '5':
            to_round = '{}6{}'.format(stringed_num[:critical_position + 1], stringed_num[critical_position + 2:])
    return str(round(float(to_round), decim_places)).ljust(critical_position, '0')

class SciViewer:
    def __init__(self, file_):
        self.file_ = file_
        self.db = SDB(file_)

    def print(self, raw_data, decim_places = None):
        if type(raw_data) == list:
            raw_data = set(raw_data)
            if None in raw_data:
                raw_data.remove(None)
            if len(raw_data) == 0:
                return ''
            raw_data = list(raw_data)
            keys = self.db.filter_tags(raw_data)
            if len(keys) == 0:
                return ''
            the_key = min(keys, key = lambda x: len(x))
            the_tags = self.db.extract(the_key)
            data = the_tags
        else:
            data = raw_data
        pre_raw = self.db.get(data)
        try:
            raw = self.db.get(data).value
        except:
            raw = self.db.get(data)
        try:
            if decim_places == None:
                decimal = self.db.find_cell(data).decimal
            else:
                decimal = decim_places
            return iround(raw, decimal)
        except:
            return str(raw)

    def build_table(self, common, top, left):
        height = max([len(series) for series in left])
        width = max([len(series) for series in top])
        lines = []

        class PreCell:
            def __init__(self):
                self.tags = []

            def collect_tags(self, index, matrix):
                for k in range(len(matrix)):
                    el = matrix[k][index]
                    self.tags.append(el)

        for i in range(height):
            line = []
            for j in range(width):
                precell = PreCell()
                precell.collect_tags(i, left)
                precell.collect_tags(j, top)

                line.append(self.print(precell.tags))
            lines.append(line)
        return Table(lines)

class Table:
    def __init__(self, data):
        self.data = data

    def to_TeX(self, file_var):
        fin2join = []
        for line in self.data:
            fin2join.append('&'.join([cell for cell in line]))
        file_var.write('\\\\\n'.join(fin2join) + '\\\\\n')
