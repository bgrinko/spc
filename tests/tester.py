#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import subprocess

__author__ = 'Basil Grinko'

MAX_TESTS_COUNT = 99


def main():
    tests_dir = ''
    if sys.argv.__len__() < 4:
        print "Hello to tester for SPC"
        print "/l start_test_num end_test_num -- lexical analysis tests"
        print "/s start_test_num end_test_num -- syntax analysis tests"
        return
    if sys.argv[1].lower() == '/l':
        tests_dir = 'scanner'
    if sys.argv[1].lower() == '/s':
        tests_dir = 'parser'
    try:
        start_test = int(sys.argv[2])
        end_test = int(sys.argv[3])
        if end_test > MAX_TESTS_COUNT:
            print "Sorry, but you cat use " + str(MAX_TESTS_COUNT) + " tests maximum!"
            return
    except ValueError:
        print "Test position must be integer"
        return
    for i in xrange(start_test, end_test + 1):
        try:
            print 'Run ' + tests_dir + ' test number: ' + ('{:0' + str(len(str(MAX_TESTS_COUNT))) + '}').format(i)
            ans = subprocess.check_output(['python', '../main.py', sys.argv[1].lower(),
                                          tests_dir + '/' + ('{:0' + str(len(str(
                                              MAX_TESTS_COUNT))) + '}').format(i) + '.in'])
            open('scanner/' + ('{:0' + str(len(str(MAX_TESTS_COUNT))) + '}').format(i) + '.out', 'w').write(ans)
            print 'OK'
        except Exception as e:
            print e.__str__()
            return

if __name__ == '__main__':
    main()
