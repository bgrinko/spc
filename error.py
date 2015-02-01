# Copyright (C) Basil Grinko, 2015

import sys

__author__ = 'Basil Grinko'


class Error(Exception):
    def __init__(self, line, pos, value):
        self.__value = value
        self.__line = line
        self.__pos = pos

    def __str__(self):
        return "Error! Line: " + str(self.__line) + " Pos: " + str(self.__pos) + " Msg: " + self.__value