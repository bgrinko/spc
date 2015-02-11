#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = 'Basil Grinko'

C_KEY_WORDS = [
    'integer', 'real', 'shl', 'and',  'shr', 'array', 'string', 'asm', 'for',
    'then', 'forward', 'not', 'to', 'begin', 'function', 'type', 'case', 'goto',
    'of', 'unit', 'const', 'if', 'or', 'until', 'uses', 'in', 'var',
    'procedure', 'do', 'program', 'while', 'downto', 'inline', 'with', 'else',
    'record', 'xor', 'end', 'repeat', 'div', 'mod']
C_OPERATIONS = {
    '+': 'EOAdd', '-': 'EOMinus', '*': 'EOMultiply',
    '/': 'EODivided', '<': 'EOLess', '>': 'EOMore',
    '<=': 'EOLessOrEqual', '>=': 'EOMoreOrEqual',
    '=': 'EOEqual', ':=': 'EOAssign', '<>': 'EONotEqual',
    '@': 'EOAt', '^': 'EOCap'
}
C_SEPARATORS = {
    ';': 'ESSemicolon', ',': 'ESComma', ':': 'ESColon',
    '[': 'ESOpenBracket', ']': 'ESCloseBracket',
    '(': 'ESOpenParenthesis', ')': 'ESCloseParenthesis',
    '..': 'ESTwoDots', '.': 'ESDot'
}

NONE = 0
KEYWORD = 1
OPERAT = 2
SEPARAT = 3
INTEGER = 4
REAL = 5
CHAR = 6
STRING = 7
IDENTIF = 8
EOF = 9


class TokenAllTypes(object):
    e_type = NONE
    type_string = 'NONE'

    def __init__(self):
        pass


def is_type(self, other):
    if self.e_type == other:
        return True
    else:
        return False


class TokenGenerator(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TokenGenerator, cls).__new__(cls, *args, **kwargs)
            cls._token_types = dict()
            for v in C_KEY_WORDS:
                cls._token_types[v] = type(
                    'EK' + v[0].upper() + v[1:], (TokenAllTypes, ), {'e_type': KEYWORD})
            for k, v in C_OPERATIONS.iteritems():
                cls._token_types[k] = type(v, (TokenAllTypes, ), {'e_type': OPERAT})
            for k, v in C_SEPARATORS.iteritems():
                cls._token_types[k] = type(v, (TokenAllTypes, ), {'e_type': SEPARAT})
            cls._token_types['t_integer'] = type('ETInteger', (TokenAllTypes, ), {'e_type': INTEGER})
            cls._token_types['t_real'] = type('ETReal', (TokenAllTypes, ), {'e_type': REAL})
            cls._token_types['t_char'] = type('ETChar', (TokenAllTypes, ), {'e_type': CHAR})
            cls._token_types['t_string'] = type('ETString', (TokenAllTypes, ), {'e_type': STRING})
            cls._token_types['t_id'] = type('EId', (TokenAllTypes, ), {'e_type': IDENTIF})
            cls._token_types['t_eof'] = type('EEoF', (TokenAllTypes, ), {'e_type': EOF})
        return cls._instance

    @staticmethod
    def key_word_exist(value):
        if value in C_KEY_WORDS:
            return True
        return False

    @staticmethod
    def operation_exist(value):
        if value in C_OPERATIONS.keys():
            return True
        return False

    @staticmethod
    def separator_exist(value):
        if value in C_SEPARATORS.keys():
            return True
        return False

    def get_token(self, value):
        if value in self._token_types.keys():
            return self._token_types[value]
        else:
            return False


