#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
from scanner import Scanner
from error import Error

__author__ = 'Basil Grinko'

SPC_VERSION = "0.01"


def main():
    if len(sys.argv) < 3:
        print "Hello to Simple Pascal Compiler use Python"
        print "Version: " + SPC_VERSION
        print "/P FileName -- Parser Test"
        return
    try:
        if sys.argv[1] == '/P':
            m_scanner = Scanner(sys.argv[2])
            for token in m_scanner:
                print str(token.get_line) + ' ' + str(token.get_position) + ' ' + str(token.get_value) + ' --> ' + str(token.get_type_name)
    except Error as e:
        print e.__str__()


if __name__ == '__main__':
    main()
