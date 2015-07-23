import os
import sys
#sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from noggin.lexer.tokens import *

from noggin.parser.parser_code import Parser

class Number(PrimaryExpression):
    number = None

    def __init__(self, number):
        self.number = number
