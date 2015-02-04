#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = 'Basil Grinko'

C_ERROR_MESSAGE = {
    'UnknownChar': 'Illegal character in input file',
    'WrongInteger': 'Syntax error in Integer number',
    'WrongReal': 'Syntax error in Real number',
    'WrongStr': 'Unterminated String',
    'UoF': 'Unexpected End of File',
    'ExprEx': 'Expression expected'
}


class Error(Exception):
    def __init__(self, line, pos, value):
        self.__value = value
        self.__line = line
        self.__pos = pos

    def __str__(self):
        return "Error! Line: " + str(self.__line) + " Pos: " + str(self.__pos) + " Msg: " + self.__value