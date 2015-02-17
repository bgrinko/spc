#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = 'Basil Grinko'


class Symbol:
    _name = ''
    lengthL, lengthR = 0, 0

    def __init__(self):
        pass

    @property
    def name(self):
        return self._name

    def write_format(self, s1, s2, l, r, shift):
        pass

    def get_shift_string(self, l, r, shift):
        pass

    def __str__(self):
        raise NotImplementedError("Method Symbol.__str__ is pure virtual")


class SymTable:
    _lengthL, _lengthR = 0, 0
    _symbols = dict()
    _name = ''

    def __init__(self, name):
        self._name = name

    def find(self, name):
        return self._symbols.get(name, None)

    def add(self, symbol):
        if self.find(symbol.name) is None:
            return False
        self._symbols[symbol.name] = symbol
        self._lengthR = max(self._lengthR, symbol.lengthR)
        self._lengthL = max(self._lengthL, symbol.lengthL)
        return True

    @property
    def length_l(self):
        return self._lengthL

    @property
    def length_r(self):
        return self._lengthR

    @property
    def name(self):
        return self._name

    @property
    def symbols(self):
        return self._symbols

    def __str__(self):
        pass


class SymInfo:
    _symbol = Symbol()
    _table = SymTable()

    def __init__(self):
        pass

    @property
    def symbol(self):
        return self._symbol

    @property
    def table(self):
        return self._table


class SymNull(SymInfo):
    pass


class SymTableStack:
    _tables = []

    def __init__(self):
        pass

    def push(self, item):
        self._tables.append(item)

    def pop(self):
        return self._tables.pop()

    def get(self):
        return self._tables[len(self._tables)]


class SymTableGlobal(SymTable):
    pass


class SymTableLocal(SymTable):
    pass


class SymTableParam(SymTable):
    pass


class SymType(Symbol):
    pass


"""
    Продолжить ад...
"""