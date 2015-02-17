#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = 'Basil Grinko'

from spc.error import *
from spc.sym_table import *
from spc.scanner import *
from spc.token_type_gen import *

C_MAIN_TABLE = 'Main'
C_RECORD_TABLE = 'Record'
C_PARAM_TABLE = 'Param'
C_ARGS_TABLE = 'Args'
C_LOCAL_TABLE = 'Local'


class Parser:
    def __init__(self, scanner):
        self._scanner = scanner
        self._token_generator = TokenGenerator()
        self._sym_table = SymTableGlobal(C_MAIN_TABLE)

    def _is_type(self, token, type_name):
        return self._token_generator.is_type(token, type_name)

    def parse_statement(self):
        pass

    def parse_syntax_node(self):
        pass

    def parse_term(self):
        pass

    def parse_factor(self):
        pass

    def parse_record(self, var):
        pass

    def parse_function(self, var):
        pass

    def parse_array(self, var):
        pass

    def parse_raf(self, var):
        pass

    def parse_sym_table(self):
        pass

    def add_symbol(self, symbol, sym_table):
        pass

    def wait_semicolon(self):
        if self._is_type(self._scanner.get_token, 'ESSemicolon'):
            self._scanner.next()
            return
        self._scanner.next()
        if self._is_type(self._scanner.get_token, 'EKEnd'):
            return
        self.error(self._scanner.get_token, 'ER',
                   self._is_type(self._scanner.get_token, 'ESSemicolon'))
        self._scanner.next()

    def wait_dot(self):
        self._scanner.next()
        self.error(self._scanner.get_token, 'ER',
                   self._is_type(self._scanner.get_token, 'ESDot'))

    def parse_variable(self):
        pass

    def parse_const(self):
        pass

    def parse_type(self):
        pass

    def parse_variables(self):
        pass

    def parse_consts(self):
        pass

    def parse_types(self):
        pass

    def parse_procedure(self, is_function=False):
        pass

    def parse_declaration(self):
        pass

    def parse_block(self):
        pass

    @staticmethod
    def error(token, msg, ex=True):
        if ex:
            raise Error(token.get_line, token.get_position, msg)
        pass

    def parse(self):
        pass




