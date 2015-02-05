#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys

from spc.scanner import Scanner
from spc.error import Error


__author__ = 'Basil Grinko'

SPC_VERSION = "0.01"


def main():
    if len(sys.argv) < 3:
        print "Hello to Simple Pascal Compiler"
        print "Version: " + SPC_VERSION
        print "/l <file_name> -- lexical analysis"
        return
    try:
        if sys.argv[1].lower() == '/l':
            m_scanner = Scanner(sys.argv[2])
            for token in m_scanner:
                token.print_token()
    except Error as e:
        print e.__str__()


if __name__ == '__main__':
    main()
