#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = 'Basil Grinko'

from spc.error import *
from spc.token_type_gen import TokenGenerator


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
    def get_type(self):
        return self.__token_type

    @property
    def get_value(self):
        return self.__value

    @property
    def get_type_name(self):
        return self.__token_type.__name__

    def print_token(self):
        print \
            str(self.__line) + '\t' + str(self.__position) \
            + '\t' + self.get_type.type_string + '\t\t' + str(self.__value)


class ReadBuffer:
    def __init__(self, file_name):
        self.__file = open(file_name, 'r')
        self.__buffer_chars = []
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
            if self.__end_of_file:
                return ''
            result = self.__file.read(1)
            self.__buffer_position += 1
            if result == '':
                self.__end_of_file = True
                self.__file.close()
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
    def __init__(self, file_name):
        self.__file_name = file_name
        self.__line = 1
        self.__position = 0
        self.__char = ''
        self.__token_types = TokenGenerator()
        self.__buffer = ReadBuffer(file_name)

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
        value = ''

    def __read_operation_token(self):
        value = ''
        value += self.__char
        if self.__is_operation():
            self.__read()
            if self.__is_operation():
                if self.__token_types.operation_exist(value + self.__char):
                    return Token(self.__token_types.get_token(value + self.__char),
                                 self.__line, self.__position, value + self.__char)
                else:
                    self.__step_back(2)
                    self.__read()
            else:
                self.__step_back(2)
                self.__read()
                if self.__token_types.operation_exist(value):
                    return Token(self.__token_types.get_token(value), self.__line, self.__position, value)
        if self.__is_separator():
            self.__read()
            if self.__is_separator():
                if self.__token_types.separator_exist(value + self.__char):
                    return Token(self.__token_types.get_token(value + self.__char),
                                 self.__line, self.__position, value + self.__char)
            else:
                self.__step_back()
                if self.__token_types.separator_exist(value):
                    return Token(self.__token_types.get_token(value), self.__line, self.__position, value)
        raise Error(self.__line, self.__position, C_ERROR_MESSAGE['ExprEx'])

    def __read_identifier_token(self):
        value = ''
        result = None
        while self.__is_latter() or self.__is_underscore() or self.__is_num():
            value += self.__char
            if self.__is_latter() or self.__is_underscore() or self.__is_num():
                if self.__token_types.key_word_exist(value.lower()):
                    const_type = self.__token_types.get_token(value.lower())
                else:
                    const_type = self.__token_types.get_token('t_id')
                result = Token(const_type, self.__line, self.__position, value)
            self.__read()
        self.__step_back()
        return result

    def __read_number_token(self):
        const_type = self.__token_types.get_token('t_integer')
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
            const_type = self.__token_types.get_token('t_real')
            value.value += self.__read()
            self.__read()
            if not read_nums():
                raise Error(self.__line, self.__position, C_ERROR_MESSAGE['WrongInteger'])
        if self.__is_e():
            const_type = self.__token_types.get_token('t_real')
            value.value += self.__char
            self.__read()
            if self.__is_char('+') or self.__is_char('-'):
                value.value += self.__char
                self.__read()
            if not read_nums():
                raise Error(self.__line, self.__position, C_ERROR_MESSAGE['WrongReal'])
        if not (self.__is_operation() or self.__is_separator() or self.__is_space() or self.__is_end_of_file()):
            if const_type == self.__token_types.get_token('t_real'):
                raise Error(self.__line, self.__position, C_ERROR_MESSAGE['WrongReal'])
            else:
                raise Error(self.__line, self.__position, C_ERROR_MESSAGE['WrongInteger'])
        result = Token(const_type, self.__line, self.__position, value.value)
        self.__step_back()
        return result

    def __read_string_token(self):
        const_type = self.__token_types.get_token('t_char')
        value = self.TokenValue
        value.value = ''

        def read_chars():
            result = 0
            rv = self.TokenValue
            while not (self.__is_single_quote() and not self.__is_double_quote()) \
                    and not self.__is_space() and not self.__is_end_of_file():
                result += 1
                rv.value += self.__char
                self.__read()
                if self.__is_space() or self.__is_end_of_file():
                    result = -1
            return result

        self.__read()
        read_count_char = read_chars()
        if read_count_char == -1:
            raise Error(self.__line, self.__position, C_ERROR_MESSAGE['WrongStr'])
        if read_count_char > 1 or read_count_char == 0:
            const_type = self.__token_types.get_token('t_string')
        return Token(const_type, self.__line, self.__position, value.value)

    def __read_token(self):
        self.__read()
        const_type = self.__token_types.get_token('t_eof')
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
