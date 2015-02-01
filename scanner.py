# Copyright (C) Basil Grinko, 2015

import sys
from error import Error

__author__ = 'Basil Grinko'

C_ERROR_MESSAGE = {
    'UnknownChar': 'Illegal character in input file',
    'WrongInteger': 'Syntax error in Integer number',
    'WrongReal': 'Syntax error in real number',
    'WrongStr': 'Unterminated string',
    'UoF': 'Unexpected end of file',
    'ExprEx': 'Expression expected'
}
C_KEY_WORDS = [
    'integer', 'real', 'shl', 'and',  'shr', 'array', 'string', 'asm', 'for',
    'then', 'forward', 'not', 'to', 'begin', 'function', 'type', 'case', 'goto',
    'of', 'unit', 'const', 'if', 'or', 'until', 'uses', 'in', 'var',
    'procedure', 'do', 'program', 'while', 'downto', 'inline', 'with', 'else',
    'record', 'xor', 'end', 'repeat', 'div', 'mod']
C_OPERATIONS = {
    '+': 'EAdd', '-': 'EMinus', '*': 'EMultiply',
    '/': 'EDivided', '<': 'ELess', '>': 'EMore',
    '<=': 'ELessOrEqual', '>=': 'EMoreOrEqual',
    '=': 'EEqual', ':=': 'EAssign', '<>': 'ENotEqual',
    '@': 'EAt', '^': 'ECap'
}
C_SEPARATORS = {
    ';': 'ESemicolon', ',': 'EComma', ':': 'EColon',
    '[': 'EOpenBracket', ']': 'ECloseBracket',
    '(': 'EOpenParenthesis', ')': 'ECloseParenthesis',
    '..': 'ETwoDots', '.': 'EDot'
}


class TokenAllTypes(object):
    def __init__(self):
        pass


class Token:
    def __init__(self, token_type, line, pos, value):
        self.__token_type = token_type
        self.__line = line
        self.__position = pos
        self.__value = value

    @property
    def get_line(self):
        return self.__line

    @property
    def get_position(self):
        return self.__position

    @property
    def get_token_type(self):
        return self.__token_type

    @property
    def get_value(self):
        return self.__value

    @property
    def get_type_name(self):
        return self.__token_type.__name__


class ReadBuffer:
    __buffer_chars = []

    def __init__(self, file_name):
        self.__file = open(file_name, 'r')
        self.__buffer_read = False
        self.__buffer_position = -1
        self.__buffer_read_position = 0
        self.__end_of_file = False

    def step_back(self):
        result = True
        if self.__buffer_read:
            self.__buffer_position -= 1
            result = False
        self.__buffer_read = True
        return result

    def read(self):
        if not self.__buffer_read:
            result = self.__file.read(1)
            self.__buffer_position += 1
            if result == '':
                self.__end_of_file = True
            self.__buffer_chars.append(result)
        else:
            result = self.__buffer_chars[self.__buffer_position]
            self.__buffer_position += 1
            if self.__buffer_chars.__len__() - 1 < self.__buffer_position:
                self.__buffer_position -= 1
                self.__buffer_read = False
        return result

    @property
    def eof(self):
        return self.__end_of_file


class Scanner:
    __char = ''
    __token_types = dict()

    def __init__(self, file_name):
        self.__file_name = file_name
        self.__line = 1
        self.__position = 0
        self.__buffer = ReadBuffer(file_name)
        for v in C_KEY_WORDS:
            self.__token_types[v] = type('EK' + v[0].upper() + v[1:], (TokenAllTypes, ), {})
        for k, v in C_OPERATIONS.iteritems():
            self.__token_types[k] = type(v, (TokenAllTypes, ), {})
        for k, v in C_SEPARATORS.iteritems():
            self.__token_types[k] = type(v, (TokenAllTypes, ), {})
        self.__token_types['t_integer'] = type('EInteger', (TokenAllTypes, ), {})
        self.__token_types['t_real'] = type('EReal', (TokenAllTypes, ), {})
        self.__token_types['t_char'] = type('EReal', (TokenAllTypes, ), {})

    def __iter__(self):
        return self

    def __read(self):
        self.__char = self.__buffer.read()
        self.__position += 1
        if self.__char == chr(10):
            self.__line += 1
            self.__position = 0
        return self.__char

    def __step_back(self, count=1):
        for i in xrange(count):
            if not self.__buffer.step_back():
                return
            else:
                self.__position -= 1

    def __big_step_back(self):
        self.__step_back(2)
        self.__read()

    def __is_latter(self):
        return (self.__char.lower() <= 'z') and (self.__char.lower() >= 'a')

    def __is_num(self):
        return (self.__char <= '9') and (self.__char >= '0')

    def __is_underscore(self):
        return self.__char == '_'

    def __is_dot(self):
        return self.__char == '.'

    def __is_e(self):
        return self.__char.lower() == 'e'

    def __is_char(self, c):
        return self.__char == c

    def __is_single_quote(self):
        return self.__char == "'"

    def __is_double_quote(self):
        result = self.__is_single_quote and self.__read() == "'"
        if not result:
            self.__big_step_back()
        return result

    def __is_operation(self):
        return self.__char in ['+', '-', '*', '/', '<', '>', '=', ':', '@', '^']

    def __is_separator(self):
        return self.__char in [';', ',', ':', '.', '(', '[', ')', ']']

    def __is_open_bracket(self):
        return self.__char in ['(', '[']

    def __is_close_bracket(self):
        return self.__char in [')', ']']

    def __is_space(self):
        return self.__char in [' ', chr(13), chr(10), chr(9)]

    def __is_end_of_file(self):
        return self.__buffer.eof

    class TokenValue(object):
        _instance = None
        value = ''

        def __new__(cls, *args, **kwargs):
            if not cls._instance:
                cls._instance = super(TokenValue, cls).__new__(cls, *args, **kwargs)
            return cls._instance

    def __read_operation_token(self):
        value = ''
        value += self.__char
        if self.__is_operation():
            self.__read()
            if self.__is_operation():
                if value + self.__char in C_OPERATIONS.keys():
                    return Token(self.__token_types[value + self.__char], self.__line, self.__position, value + self.__char)
                else:
                    self.__step_back(2)
                    self.__read()
            else:
                self.__step_back(2)
                self.__read()
                if value in C_OPERATIONS.keys():
                    return Token(self.__token_types[value], self.__line, self.__position, value)
        if self.__is_separator():
            self.__read()
            if self.__is_separator():
                if value + self.__char in C_SEPARATORS.keys():
                    return Token(self.__token_types[value + self.__char], self.__line, self.__position, value + self.__char)
            else:
                self.__step_back()
                if value in C_SEPARATORS.keys():
                    return Token(self.__token_types[value], self.__line, self.__position, value)
        raise Error(self.__line, self.__position, C_ERROR_MESSAGE['ExprEx'])

    def __read_identifier_token(self):
        value = ''
        while self.__is_latter() or self.__is_underscore() or self.__is_num():
            value += self.__char
            if self.__is_latter() or self.__is_underscore() or self.__is_num():
                if value.lower() in C_KEY_WORDS:
                    const_type = type('E' + value[0].upper() + value[1:], (TokenAllTypes, ), {})
                else:
                    const_type = type('EId', (TokenAllTypes, ), {})
                result = Token(const_type, self.__line, self.__position, value)
            self.__read()
        self.__step_back()
        return result

    def __read_number_token(self):
        const_type = self.__token_types['t_integer']
        value = self.TokenValue
        value.value = ''

        def read_nums():
            res = False
            rv = self.TokenValue
            while self.__is_num():
                res = True
                rv.value += self.__char
                self.__read()
            return res

        read_nums()
        if self.__is_dot():
            self.__read()
            self.__step_back(2)
            if self.__is_dot():
                return Token(const_type, self.__line, self.__position, value.value)
            const_type = self.__token_types['t_real']
            value.value += self.__read()
            self.__read()
            if not read_nums():
                raise Error(self.__line, self.__position, C_ERROR_MESSAGE['WrongInteger'])
        if self.__is_e():
            const_type = self.__token_types['t_real']
            value.value += self.__char
            self.__read()
            if self.__is_char('+') or self.__is_char('-'):
                value.value += self.__char
                self.__read()
            if not read_nums():
                raise Error(self.__line, self.__position, C_ERROR_MESSAGE['WrongReal'])
        if not (self.__is_operation() or self.__is_separator() or self.__is_space()):
            if const_type == self.__token_types['t_real']:
                raise Error(self.__line, self.__position, C_ERROR_MESSAGE['WrongReal'])
            else:
                raise Error(self.__line, self.__position, C_ERROR_MESSAGE['WrongInteger'])
        result = Token(const_type, self.__line, self.__position, value.value)
        self.__step_back()
        return result

    def __read_string_token(self):
        const_type = type('EChar', (TokenAllTypes, ), {})
        read_count_char = 0
        value = self.TokenValue
        value.value = ''

        def read_chars():
            result = 0
            rv = self.TokenValue
            while not (self.__is_single_quote() and not self.__is_double_quote()) and not self.__is_space():
                result += 1
                rv.value += self.__char
                self.__read()
                if self.__is_space():
                    result = -1
            return result

        self.__read()
        read_count_char = read_chars()
        if read_count_char == -1:
            raise Error(self.__line, self.__position, C_ERROR_MESSAGE['WrongStr'])
        if read_count_char > 1 or read_count_char == 0:
            const_type = type('EString', (TokenAllTypes, ), {})
        return Token(const_type, self.__line, self.__position, value.value)

    def __read_token(self):
        self.__read()
        const_type = type('EEoF', (TokenAllTypes, ), {})
        if self.__is_end_of_file():
            self.__current_token = Token(const_type, self.__line, self.__position, 'End of File')
            return False
        elif self.__is_space():
            result = self.__read_token()
        elif self.__is_num():
            self.__current_token = self.__read_number_token()
        elif self.__is_single_quote():
            self.__current_token = self.__read_string_token()
        elif self.__is_latter() or self.__is_underscore():
            self.__current_token = self.__read_identifier_token()
        elif self.__is_operation() or self.__is_separator():
            self.__current_token = self.__read_operation_token()
        else:
            raise Error(self.__line, self.__position, C_ERROR_MESSAGE['UnknownChar'])
        return True

    def next(self):
        if self.__read_token():
            return self.__current_token
        else:
            raise StopIteration
