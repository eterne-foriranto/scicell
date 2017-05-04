#!/usr/bin/python
from os import path
from sys import path as syp
syp.append(path.expanduser('~/lib'))
from uncertainties import ufloat as uf

PLANCK = 6.626070040e-34
LIGHTSPEED = 299792458
AVOGADRO = 6.022140857e23
CHARGE = 1.6021766208e-19

coefs = {}
coefs['Joule'] = {
        'Diopter':1 / PLANCK / LIGHTSPEED,
        'Joule_rMole':AVOGADRO
        }
coefs['Diopter'] = {
        'Joule':PLANCK * LIGHTSPEED,
        'Joule_rMole':AVOGADRO * PLANCK * LIGHTSPEED
        }
coefs['Joule_rMole'] = {
        'Joule':1 / AVOGADRO
        }

def hub(from_, to):
    if from_ == to:
        return 1
    else:
        return coefs[from_][to]

class Unit():
    def __init__(self, value = 1, error = None):
        value = float(value)
        if value.is_integer():
            value = int(value)

        if error == None:
            self.value = value
        else:
            self.value = uf(value, error)

    def __lt__(self, unit_obj):
        if type(unit_obj) != self.__class__:
            unit_obj = unit_obj.convert(self.__class__())
        return self.value < unit_obj.value

    def __gt__(self, unit_obj):
        if type(unit_obj) != self.__class__:
            unit_obj = unit_obj.convert(self.__class__())
        return self.value > unit_obj.value

    def __add__(self, unit_obj):
        if type(unit_obj) != self.__class__:
            unit_obj = unit_obj.convert(self.__class__())
        return self.__class__(self.value + unit_obj.value)

    def __sub__(self, unit_obj):
        if type(unit_obj) != self.__class__:
            unit_obj = unit_obj.convert(self.__class__())
        return self.__class__(self.value - unit_obj.value)

    def __mul__(self, comul):
        t = type(comul)
        if t == int or t == float:
            return self.__class__(comul * self.value)

    def __truediv__(self, divider):
        t = type(divider)
        if t == int or t == float:
            return self.__class__(self.value / divider)

    def __repr__(self):
        class_ = str(self.__class__)
        raw_name = class_[class_.index('.') + 1:]
        name = raw_name[:raw_name.index('\'')]
        return '{} {}'.format(str(self.value), name)

    def convert(self, obj):
        k0, from_ = self.to_base()
        k1, to = obj.to_base()
        return type(obj)(self.value * k0 * hub(from_, to) / k1)

class Number(float):
    def __init__(self, value):
        self.value = value

    def __mul__(self, comul):
        return type(comul)(self.value * comul.value)

class Hartree(Unit):
    def to_base(self):
        return 4.359744650e-18, 'Joule'

class Rcm(Unit):
    def to_base(self):
        return 1e2, 'Diopter'

class Angstrom(Unit):
    pass

class Joule(Unit):
    pass

class Joule_rMole(Unit):
    pass

class Degree(Unit):
    pass

class kJoule_rMole(Unit):
    def to_base(self):
        return 1e3, 'Joule_rMole'

class kCalorie_rMole(Unit):
    def to_base(self):
        return 4184, 'Joule_rMole'

class eV(Unit):
    def to_base(self):
        return CHARGE, 'Joule'
